import numpy as np
from mlffbrew.typing import Box, npstr, npf64, ScriptData
from mlffbrew.programs.scripter import modify


__all__ = ["write", "read", "modify", "modify_box", "modify_coord", "base_scipt_data"]


def join(data: ScriptData, *, indent_level=0) -> str:
    script = ""
    indent = "\t" * indent_level
    for key, val in data.items():
        if isinstance(val, dict):
            script += f"{indent}&{key}\n"
            script += join(data=val, indent_level=indent_level + 1)
            script += f"{indent}&END {key.split()[0]}\n"
        else:
            script += f"{indent}{key} {val}\n"
    return script


def write(file: str, data: ScriptData, *, mode: str = "w") -> None:
    with open(file=file, mode=mode) as f:
        f.writelines(join(data=data))


def read(file: str, *, head_word: str = "&", tail_word: str = "&END") -> ScriptData:
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


def modify_box(data: ScriptData, box: Box, *, dim: int = 3) -> ScriptData:
    box = np.array(box, dtype=npf64)
    ndim = box.ndim
    if ndim == 0:
        box = np.eye(3) * box
    elif ndim == 1 and box.shape[0] == dim:
        box = np.diag(box)
    elif ndim == 2 and box.shape == (dim, dim):
        box = box
    else:
        raise ValueError(f"Box shape is not acceptable, {box.shape}")
    box = box.astype(npstr)
    what = {abc: " ".join(box[i]) for i, abc in enumerate(["A", "B", "C"])}
    return modify(data=data, what={"CELL": what}, head="FORCE_EVAL/SUBSYS")


def modify_coord(
    data: ScriptData,
    *,
    head: str = "TOPOLOGY",
    modified_dict={"COORD_FILE_NAME": "run.xyz", "COORD_FILE_FORMAT": "xyz"},
) -> ScriptData:
    subsys_data = data["FORCE_EVAL"]["SUBSYS"]
    if "COORD" in subsys_data:
        subsys_data.pop("COORD")
    subsys_data[head] = modified_dict
    return data
