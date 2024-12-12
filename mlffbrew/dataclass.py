import numpy as np
from typing import Literal
from dataclasses import dataclass
from mlffbrew.typing import npstr, npf64, Box, Atoms, Coords, Energy, Stress, Virial, Force


STATE_KEYS = ["coords", "atoms", "energy", "stress", "virial", "force", "box"]


@dataclass(slots=True)
class State:
    coords: Coords = None
    atoms: Atoms = None
    energy: Energy = None
    stress: Stress = None
    virial: Virial = None
    force: Force = None
    box: Box = None

    def __post_init__(self):
        if self.coords is not None:
            self.coords = np.array(self.coords, dtype=npf64)
            if len(self.coords.shape) != 2 or self.coords.shape[1] != 3:
                raise ValueError(f"coords should be (N, 3) shape, got {self.coords.shape}")

        if self.force is not None:
            self.force = np.array(self.force, dtype=npf64)
            if self.coords is not None and self.force.shape != self.coords.shape:
                raise ValueError(f"force shape {self.force.shape} doesn't match coords shape {self.coords.shape}")

        if self.atoms is not None:
            self.atoms = np.array(self.atoms, dtype=npstr)
            if self.coords is not None and len(self.atoms) != len(self.coords):
                raise ValueError(f"Number of atoms {len(self.atoms)} doesn't match coords length {len(self.coords)}")

        if self.box is not None:
            self.box = np.array(self.box, dtype=npf64)
            if self.box.shape != (3, 3):
                raise ValueError(f"box should be (3, 3) shape, got {self.box.shape}")

        if self.stress is not None:
            self.stress = np.array(self.stress, dtype=npf64)
            if self.stress.shape != (3, 3):
                raise ValueError(f"stress should be (3, 3) shape, got {self.stress.shape}")

        if self.virial is not None:
            self.virial = np.array(self.virial, dtype=npf64)
            if self.virial.shape != (3, 3):
                raise ValueError(f"virial should be (3, 3) shape, got {self.virial.shape}")

        if self.energy is not None:
            self.energy = np.array(self.energy, dtype=npf64)
            if self.energy.shape != ():
                raise ValueError(f"energy should be scalar, got shape {self.energy.shape}")


def state(**kwrgs: Literal["coords", "atoms", "energy", "stress", "virial", "force", "box"]) -> State:
    for key in kwrgs.keys():
        if key not in STATE_KEYS:
            raise KeyError(f"{key} is not included in STATE_KEYS")
    return State(**kwrgs)
