import numpy as np
from atombrew import Home
from typing import List, Dict, Literal, Union
from mlffbrew.typing import Force, Coords, npf64, FilePath


ForceAndCoordsDict = Dict[Literal["force", "coord"], Union[Force, Coords]]


def parse_trj(trjfiles: List[FilePath]) -> ForceAndCoordsDict:
    nframe = len(trjfiles)
    natoms = Home(trjfiles[0]).natoms
    coords = np.array([nframe, natoms, 3], dtype=npf64)
    forces = np.array([nframe, natoms, 3], dtype=npf64)
    for frame, trjfile in enumerate(trjfiles):
        home = Home(trjfile)
        coords[frame] = home.coords
        forces[frame] = home.forces
    return {"coord": coords, "force": forces}
