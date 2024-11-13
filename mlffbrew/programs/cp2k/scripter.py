from copy import deepcopy
from mlffbrew.typing import Box

__all__ = ["write", "read", "modify", "modify_box", "modify_coord", "baselines"]


__BASE_SCRIPT_INFO = {
    "GLOBAL": {
        "PROJECT": "RUN",
        "RUN_TYPE": "ENEGY_FORCE",
    },
    "FORCE_EVAL": {
        "METHOD": "Quickstep",
        "STRESS_TENSOR": "ANALYTICAL",
        "DFT": {
            "BASIS_SET_FILE_NAME": "BASIS_MOLOPT_SCAN",
            "POTENTIAL_FILE_NAME": "GTH_POTENTIALS_SCAN",
            "CHARGE": 0,
            "MULTIPLICITY": 1,
            "MGRID": {
                "CUTOFF": 1200,
                "REL_CUTOFF": 60,
                "NGRIDS": 5,
            },
            "QS": {
                "METHOD": "GPW",
                "EPS_DEFAULT": 1.0e-14,
                "EXTRAPOLATION": "ASPC",
            },
            "POISSON": {
                "PERIODIC": "XYZ",
            },
            "SCF": {
                "SCF_GUESS": "RESTART",
                "MAX_SCF": 50,
                "EPS_SCF": 1.0e-7,
                "OUTER_SCF": {
                    "EPS_SCF": 1.0e-7,
                    "MAX_SCF": 10,
                },
                "OT": {"PRECONDITIONER": "FULL_SINGLE_INVERSE", "MINIMIZER": "CG"},
            },
            "XC": {
                "XC_FUNCTIONAL": {
                    "MGGA_X_R2SCAN": {},
                    "MGGA_C_R2SCAN": {},
                }
            },
        },
        "SUBSYS": {
            "CELL": {
                "A": "12.6 0.0 0.0",
                "B": "0.0 12.6 0.0",
                "C": "0.0 0.0 12.6",
            },
            "TOPOLOGY": {"COORD_FILE_NAME": "./run.xyz", "COORD_FILE_FORMAT": "XYZ"},
            "KIND H": {
                "BASIS_SET": "TZV2P-MOLOPT-SCAN-GTH-q1",
                "POTENTIAL": "GTH-SCAN-1",
            },
            "KIND O": {
                "BASIS_SET": "TZV2P-MOLOPT-SCAN-GTH-q6",
                "POTENTIAL": "GTH-SCAN-6",
            },
        },
    },
}
baselines = deepcopy(__BASE_SCRIPT_INFO)
del deepcopy


def write(data: dict[str], *, indent_level=0) -> str:
    script = ""
    indent = "\t" * indent_level
    for key, val in data.items():
        if isinstance(val, dict):
            script += f"{indent}&{key}\n"
            script += write(data=val, indent_level=indent_level + 1)
            script += f"{indent}&END {key}\n"
        else:
            script += f"{indent}{key} {val}\n"
    return script


def read(file: str, *, head_word: str = "&", tail_word: str = "&END") -> dict:
    script_info = {}
    stack = [script_info]
    with open(file, "r") as f:
        while line := f.readline():
            line = line.strip()
            if line.startswith(tail_word):
                stack.pop()
            elif line.startswith(head_word):
                section = line[1:]
                new_section = {}
                stack[-1][section] = new_section
                stack.append(new_section)
            else:
                if line:
                    key, value = line.split(maxsplit=1)
                    stack[-1][key] = value
    return script_info


def modify(
    data: dict[str],
    what: dict[str, any],
    *,
    add: bool = False,
    head: str = None,
    sep: str = "/",
) -> dict:
    headlist = head.split(sep=sep)
    sub_data = data
    for this_head in headlist:
        sub_data = sub_data[this_head]
    for key, val in what.items():
        if key not in sub_data and not add:
            raise KeyError(f"Can not moify data, Key({key}) absent")
        sub_data[key] = val
    return data


def modify_box(data: dict, box: Box):
    box = box.astype(str)
    what = {abc: " ".join(box[i]) for i, abc in enumerate(["A", "B", "C"])}
    data = modify(data=data, what={"CELL": what}, head="FORCE_EVAL/SUBSYS")
    return data


def modify_coord(data: dict):
    subsys_data = data["FORCE_EVAL"]["SUBSYS"]
    if "COORD" in subsys_data:
        subsys_data.pop("COORD")
    subsys_data["TOPOLOGY"] = {"COORD_FILE_NAME": "run.xyz", "COORD_FILE_FORMAT": "xyz"}
    return data