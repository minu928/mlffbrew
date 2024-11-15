from os import sep
from mlffbrew.typing import ScriptData, Dict


def modify(
    data: ScriptData,
    what: Dict[str, str],
    *,
    add: bool = False,
    head: str = None,
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
