import numpy as np
from dataclasses import dataclass
from samsarabrew.typing import npstr, npf64, Box, Atoms, Coords, Energy, Stress, Virial, Force


@dataclass
class FrameData:
    version: npstr = None
    coords: Coords = None
    atoms: Atoms = None
    energy: Energy = None
    stress: Stress = None
    virial: Virial = None
    force: Force = None
    box: Box = None

    def __init__(self, **kwrgs):
        for k, v in kwrgs.items():
            if not hasattr(self, k):
                raise AttributeError(f"Attribute {k} is not included.")
            setattr(self, k, np.array(v, dtype=npstr if k in ["atoms", "version"] else npf64))


@dataclass
class FrameUnit:
    coords: str = None
    atoms: str = None
    energy: str = None
    stress: str = None
    virial: str = None
    force: str = None
    box: str = None

    def __init__(self, **kwrgs):
        for k, v in kwrgs.items():
            if not hasattr(self, k):
                raise AttributeError(f"Attribute {k} is not included.")
            setattr(self, k, str(v))
