from mlffbrew.typing import ScriptData
from mlffbrew.programs.scripter import modify

GEN_CODE = {
    "gen_plm": "gen_plm all plumed plumedfile in.plumed outfile out.plumed",
    "gen_npt": "gen_npt all npt temp ${TEMP} ${TEMP} ${TAU_T} iso ${PRES} ${PRES} ${TAU_P}",
    "gen_nvt": "gen_nvt all nvt temp ${TEMP} ${TEMP} ${TAU_T}",
    "dump": "gen_dump all custom %d traj/*.lammpstrj id type x y z",
    "velocity": "all create ${TEMP} ${SEED} mom yes rot yes dist gaussian",
}

PAIRS = {
    "gen_deepmd": "deepmd ../graph.000.pb ../graph.001.pb ../graph.002.pb ../graph.003.pb  out_freq ${THERMO_FREQ} out_file model_devi.out "
}

FOMATTERS = {
    "variable": lambda name, value: f"variable{' '*8}{name:<16s}equal {value if value is not None else f'TMP_{name}'}",
    "mass": lambda name, value: f"mass{' '*12}{name:<4s}{value}",
    "fix": lambda name, value: f"fix{' '*13}{value if value is not None else GEN_CODE[name]}",
    "dump": lambda _, value: f"dump{' '*12}{value if 'gen_dump' in value else GEN_CODE['dump']}",
    "velocity": lambda _, value: f"velocity{' '*8}{value if 'gen_velocity' in value else GEN_CODE['velocity']}",
    "pair_style": lambda _, value: f"pair_style{' '*6}{value if value not in PAIRS else PAIRS[value]}",
}


def join(data: ScriptData) -> list[str]:
    script_lines = []
    for key, val in data.items():
        if key in FOMATTERS:
            if isinstance(val, dict):
                script_lines.extend(FOMATTERS[key](name, value) for name, value in val.items())
            else:
                script_lines.append(FOMATTERS[key](None, val))
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


def modify_variables(data: ScriptData, *nonargs, add: bool = False, **what) -> ScriptData:
    assert len(nonargs) == 0, f"{nonargs} is not keywords arguments"
    return modify(data=data, what=what, head="variable", add=add)
