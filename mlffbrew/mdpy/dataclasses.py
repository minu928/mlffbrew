import numpy as np
from dataclasses import dataclass
from mlffbrew.typing import npstr, npf64, Box, Atoms, Coords, Energy, Stress, Virial, Force


STATE_KEYS = ["coords", "atoms", "energy", "stress", "virial", "force", "box"]


@dataclass
class State:
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
            setattr(self, k, np.array(v, dtype=npstr if k in ["atoms"] else npf64))
