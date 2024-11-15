from typing import List
from atombrew import chemistry
from mlffbrew.typing import ScriptData, Ensemble, Element
from mlffbrew.programs.scripter import modify


GEN_CODE = {
    "gen_plm": f"fix{' '*13}" + "gen_plm all plumed plumedfile in.plumed outfile out.plumed",
    "gen_npt": f"fix{' '*13}" + "gen_npt all npt temp ${TEMP} ${TEMP} ${TAU_T} iso ${PRES} ${PRES} ${TAU_P}",
    "gen_nvt": f"fix{' '*13}" + "gen_nvt all nvt temp ${TEMP} ${TEMP} ${TAU_T}",
    "gen_nve": "",
    "gen_dump": f"dump{' '*12}" + "gen_dump all custom ${DUMP_FREQ} traj/*.lammpstrj id type x y z",
    "gen_velocity": f"velocity{' '*8}" + "all create ${TEMP} ${SEED} mom yes rot yes dist gaussian",
}
PAIRS = {
    "gen_deepmd": "deepmd ../graph.000.pb ../graph.001.pb ../graph.002.pb ../graph.003.pb  out_freq ${THERMO_FREQ} out_file model_devi.out "
}
FOMATTERS = {
    "fix": lambda name, value: value if value is not None else GEN_CODE[name],
    "mass": lambda name, value: f"mass{' '*12}{name:<4s}{value}",
    "variable": lambda name, value: f"variable{' '*8}{name:<16s}equal {value if value is not None else f'TMP_{name}'}",
    "dump": lambda _, value: value if "gen_dump" not in value else GEN_CODE["gen_dump"],
    "velocity": lambda _, value: value if "gen_velocity" not in value else GEN_CODE["gen_velocity"],
    "pair_style": lambda _, value: f"pair_style{' '*6}{value if value not in PAIRS else PAIRS[value]}",
}
READ_HANDLER = {
    "fix": lambda val: (val[0], " ".join(val)),
    "mass": lambda val: (val[0], val[1]),
    "variable": lambda val: (val[0], val[2]),
}


def join(data: ScriptData) -> str:
    script_lines = []
    for key, val in data.items():
        if key not in FOMATTERS:
            script_lines.append(f"{key:<16s}{val}")
            continue
        formatter = FOMATTERS[key]
        if isinstance(val, dict):
            script_lines.extend(formatter(name, value) for name, value in val.items())
        else:
            script_lines.append(formatter(None, val))
    return "\n".join(script_lines)


def write(file: str, data: ScriptData, *, mode: str = "w") -> None:
    with open(file=file, mode=mode) as f:
        f.writelines(join(data=data))


def read(file: str) -> ScriptData:
    script_info: ScriptData = {}
    with open(file) as f:
        for line in f:
            data = line.strip().split()
            if not data:
                continue
            key, *val = data
            if key in READ_HANDLER:
                name, value = READ_HANDLER[key](val)
                script_info.setdefault(key, {})[name] = value
            else:
                script_info[key] = " ".join(val)
    return script_info


def modify_variables(data: ScriptData, *, add: bool = False, **what) -> ScriptData:
    return modify(data=data, what=what, head="variable", add=add)


def modify_ensemble(data: ScriptData, ensemble: Ensemble, *, add: bool = True) -> ScriptData:
    fix = data.get("fix", {})
    if "gen_ensemble" not in fix:
        return data
    fix = data.setdefault("fix", {})
    fix.pop("gen_ensemble", None)
    return modify(data=data, head="fix", add=add, what={f"gen_{ensemble}": None})


def modify_mass(data: ScriptData, elements: List[Element]) -> ScriptData:
    data["mass"] = {str(i): str(chemistry.elements.get_mass(e)) for i, e in enumerate(elements, start=1)}
    return data
