from typing import Dict, Union
from mlffbrew.dataclass import State
from mlffbrew.unit._dataclass import StateUnit
from mlffbrew.unit._mutliplier import create_multiplier


def convert(
    data: Union[Dict, State],
    old_units: Union[Dict, StateUnit],
    new_units: Union[Dict, StateUnit],
) -> State:
    data = data.__dict__ if isinstance(data, State) else dict(data)
    old_units = old_units.__dict__ if isinstance(old_units, StateUnit) else dict(old_units)
    new_units = new_units.__dict__ if isinstance(new_units, StateUnit) else dict(new_units)
    for k, unit in old_units.items():
        unit = str(unit)
        if unit.lower() == "none":
            continue
        data[k] *= create_multiplier(expression=f"{unit}->{new_units[k]}")
    return State(**data)
