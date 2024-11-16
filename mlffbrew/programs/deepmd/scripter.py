import json
from typing import List
from numpy.random import randint
from mlffbrew.typing import ScriptData, ScriptFile, FilePath
from mlffbrew.programs.scripter import modify


def write(file: ScriptFile, data: ScriptData, *, mode: str = "w") -> None:
    with open(file, mode=mode) as f:
        json.dump(data, f)


def read(file: ScriptFile) -> ScriptData:
    with open(file, "r") as f:
        script_data = json.load(f)
    return script_data


def modify_seed(data: ScriptData) -> ScriptData:
    r1, r2, r3 = randint(1, 1e8, 3)
    data = modify(data=data, what=dict(seed=int(r1)), head="model/descriptor")
    data = modify(data=data, what=dict(seed=int(r2)), head="model/fitting_net")
    data = modify(data=data, what=dict(seed=int(r3)), head="training")
    return data


def modify_training(data: ScriptData, training_data: List[FilePath]) -> ScriptData:
    return modify(data=data, what=dict(systems=training_data), head="training/training_data")
