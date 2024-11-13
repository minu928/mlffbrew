from typing import Dict, Union
from samsarabrew.unit import style
from samsarabrew.unit._mutliplier import create_multiplier
from samsarabrew.dataclasses import FrameData, FrameUnit


__all__ = ["convert", "create_multiplier", "style"]


def convert(
    data: Union[Dict, FrameData],
    old_units: Union[Dict, FrameUnit],
    new_units: Union[Dict, FrameUnit],
) -> FrameData:
    data = data.__dict__ if isinstance(data, FrameData) else dict(data)
    old_units = old_units.__dict__ if isinstance(old_units, FrameUnit) else dict(old_units)
    new_units = new_units.__dict__ if isinstance(new_units, FrameUnit) else dict(new_units)
    for k, unit in old_units.items():
        unit = str(unit)
        if unit.lower() == "none":
            continue
        data[k] *= create_multiplier(expression=f"{unit}->{new_units[k]}")
    return FrameData(**data)
