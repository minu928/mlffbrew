from os import sep
from mlffbrew.typing import ScriptData, Dict


def modify(
    data: ScriptData,
    what: Dict[str, str],
    *,
    add: bool = False,
    head: str = None,
) -> ScriptData:
    sub_data = data
    if head is not None:
        for this_head in head.split(sep=sep):
            sub_data = sub_data[this_head]
    for key, val in what.items():
        if key not in sub_data and not add:
            raise KeyError(f"Can not moify data, Key({key}) absent")
        sub_data[key] = val
    return data
