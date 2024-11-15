import numpy as np
from typing import Dict, Union, Literal
from numpy.typing import NDArray


npf64 = np.float64
npstr = np.str_

Number = Union[float, int]

Box = NDArray[npf64]
Stress = NDArray[npf64]
Virial = NDArray[npf64]
Coords = NDArray[npf64]
Energy = NDArray[npf64]
Force = NDArray[npf64]
Atoms = NDArray[npstr]

ScriptFile = str
ScriptData = Dict[str, Union[Dict, str]]
ScriptFileOrScriptData = Union[ScriptFile, ScriptData]

Ensemble = Literal["nve", "nvt", "npt"]
Element = str
