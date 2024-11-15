from numpy.random import randint
from typing import Dict, Union, List, Literal, Tuple, Any
from mlffbrew.typing import ScriptFileOrScriptData, ScriptData, ScriptFile, Ensemble

SimulationParams = Dict[str, Union[List, str]]
Param = str
Init = str
Condition = Dict[Literal["TEMP", "PRES", "NSTEPS", "TAU_T", "TAU_P", "DUMP_FREQ", "THERMO_FREQ", "TIME_STEP"], Param]


DEFAULT_CONDITION_PARAMS: Dict[Literal["TAU_T", "TAU_P", "DUMP_FREQ", "THERMO_FREQ", "TIME_STEP"], Any] = {
    "tau_t": "0.05",
    "tau_p": "0.5",
    "dump_freq": "20",
    "thermo_freq": "20",
    "time_step": "0.0005",
}


def get_params(simulation_params: SimulationParams, param: str, default=None) -> List[Param]:
    value = simulation_params.get(param, default)
    assert value, f"Condition does not have {param}."
    return [str(value)] if not isinstance(value, list) else [str(p) for p in value]


def generate_conditioniteration(
    simulation_params: SimulationParams,
    *,
    defaults=DEFAULT_CONDITION_PARAMS,
) -> List[Tuple[Init, Ensemble, Condition]]:

    ensemble = get_params(simulation_params, "ensemble")[0]
    nsteps = get_params(simulation_params, "nsteps")[0]
    params = {key: get_params(simulation_params, key, default=val) for key, val in defaults.items()}

    init_list = get_params(simulation_params, "init")
    temp_list = get_params(simulation_params, "temp") if "t" in ensemble else ["-1"]
    pres_list = get_params(simulation_params, "pres") if "p" in ensemble else ["-1"]
    return [
        (
            init,
            ensemble,
            {
                "TEMP": temp,
                "PRES": pres,
                "NSTEPS": nsteps,
                **{k.upper(): v[0] for k, v in params.items()},
                "SEED": str(randint(1, int(1e8))),
            },
        )
        for init in init_list
        for temp in temp_list
        for pres in pres_list
    ]


def build(
    script: ScriptFileOrScriptData,
    simulation_params: SimulationParams,
    elements: List[str],
    *,
    workspace: str = "./",
    folderhead: str = "lammps",
    exist_ok: bool = False,
    maxint: int = 4,
):
    try:
        import os
        from atombrew import Home
        from copy import deepcopy
        from mlffbrew.programs import lammps
    except Exception as e:
        raise ImportError(f"Can Not Import, {e}")

    script_data: ScriptData = lammps.scripter.read(script) if isinstance(script, ScriptFile) else script
    abs_workpath = os.path.abspath(workspace)

    for i, (init, ensemble, condition) in enumerate(generate_conditioniteration(simulation_params=simulation_params)):

        this_folderpath = os.path.join(abs_workpath, f"{folderhead}.{str(i).zfill(maxint)}")
        os.makedirs(this_folderpath, exist_ok=exist_ok)

        # * Write the Initial
        this_init_path = os.path.join(this_folderpath, "in.lmps")
        home = Home(init)
        home.write(this_init_path, stop=1, verbose=False, fmt="lmps", mode="w+")

        # * Write the script
        this_script_data = deepcopy(script_data)
        this_script_data = lammps.scripter.modify_variables(data=this_script_data, add=True, **condition)
        this_script_data = lammps.scripter.modify_ensemble(data=this_script_data, ensemble=ensemble)
        this_script_data = lammps.scripter.modify_mass(data=this_script_data, elements=elements)
        this_script_path = os.path.join(this_folderpath, "in.lammps")
        lammps.scripter.write(this_script_path, data=this_script_data)
