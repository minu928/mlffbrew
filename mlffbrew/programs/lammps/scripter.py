from copy import deepcopy
from mlffbrew.typing import ScriptData, Dict, Any


__BASE_SCRIPT_INFO = {
    "variable": {
        "NSTEPS": None,
        "TEMP": None,
        "PRES": None,
        "THERMO_FREQ": None,
        "DUMP_FREQ": None,
        "TIME_STEP": None,
        "TAU_T": None,
        "TAU_P": None,
        "SEED": None,
    },
    "units": "metal",
    "boundary": "p p p",
    "atom_style": "atomic",
    "neighbor": "1.0 bin",
    "mass": {"1": "1.008000", "2": "15.999000"},
    "pair_style": "gen_deepmd",
    "pair_coeff": "* *",
    "thermo_style": "custom step temp pe ke etotal press vol lx ly lz xy xz yz",
    "thermo": "${THERMO_FREQ}",
    "dump": "gen_dump",
    "velocity": "gen_velocity",
    "fix": {"gen_npt": None},
    "timestep": "${V_TIME_STEP}",
    "run": "${NSTEPS} upto",
}
base_scipt_data = deepcopy(__BASE_SCRIPT_INFO)
del deepcopy


DEFAULTS = {
    "gen_plm": "gen_plm all plumed plumedfile in.plumed outfile out.plumed",
    "gen_npt": "gen_npt all npt temp ${TEMP} ${TEMP} ${TAU_T} iso ${PRES} ${PRES} ${TAU_P}",
    "gen_nvt": "gen_nvt all nvt temp ${TEMP} ${TEMP} ${TAU_T}",
    "dump": "gen_dump all custom %d traj/*.lammpstrj id type x y z",
    "velocity": "all create ${TEMP} ${SEED} mom yes rot yes dist gaussian",
}

PAIR_DEFAULTS = {
    "gen_deepmd": "deepmd ../graph.000.pb ../graph.001.pb ../graph.002.pb ../graph.003.pb  out_freq ${THERMO_FREQ} out_file model_devi.out "
}

formatters = {
    "variable": lambda name, value: f"variable{' '*8}{name:<16s}equal {value if value is not None else f'TMP_{name}'}",
    "mass": lambda name, value: f"mass{' '*12}{name:<4s}{value}",
    "fix": lambda name, value: f"fix{' '*13}{value if value is not None else DEFAULTS[name]}",
    "dump": lambda _, value: f"dump{' '*12}{value if 'gen_dump' in value else DEFAULTS['dump']}",
    "velocity": lambda _, value: f"velocity{' '*8}{value if 'gen_velocity' in value else DEFAULTS['velocity']}",
    "pair_style": lambda _, value: f"pair_style{' '*6}{value if value not in PAIR_DEFAULTS else PAIR_DEFAULTS[value]}",
}


def join(data: ScriptData) -> list[str]:
    script_lines = []
    for key, val in data.items():
        if key in formatters:
            if isinstance(val, dict):
                script_lines.extend(formatters[key](name, value) for name, value in val.items())
            else:
                script_lines.append(formatters[key](None, val))
        else:
            script_lines.append(f"{key:<16s}{val}")
    return "\n".join(script_lines)


def write(file: str, data: ScriptData, *, mode: str = "w") -> None:
    with open(file=file, mode=mode) as f:
        f.writelines(join(data=data))


def read(file: str) -> ScriptData:
    script_info: ScriptData = {}
    with open(file, "r") as f:
        while line := f.readline():
            data = line.rstrip().split()
            if not len(data):
                continue
            key, *val = data
            if key == "variable":
                name, _, value = val
                if key not in script_info:
                    script_info[key] = {}
                script_info[key][name] = value
            elif key == "mass":
                name, value = val
                if key not in script_info:
                    script_info[key] = {}
                script_info[key][name] = value
            elif key == "fix":
                name = val[0]
                value = " ".join(val)
                if key not in script_info:
                    script_info[key] = {}
                script_info[key][name] = value
            else:
                script_info[key] = " ".join(val)
    return script_info


def modify(
    data: ScriptData,
    what: Dict[str, Any],
    *,
    add: bool = False,
    head: str = None,
    sep: str = "/",
) -> ScriptData:
    headlist = head.split(sep=sep)
    sub_data = data
    for this_head in headlist:
        sub_data = sub_data[this_head]
    for key, val in what.items():
        if key not in sub_data and not add:
            raise KeyError(f"Can not moify data, Key({key}) absent")
        sub_data[key] = val
    return data


def modify_variables(data: ScriptData, *nonargs, **what) -> ScriptData:
    assert len(nonargs) == 0, f"{nonargs} is not keywords arguments"
    return modify(data=data, what=what, head="variable")
