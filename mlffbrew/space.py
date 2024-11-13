import numpy as np
from mlffbrew.typing import Box, Stress, Virial


def calculate_volume(box: Box, *, dim: int = 3) -> float:
    box = np.array(box)
    ndim = box.ndim
    if ndim == 0:
        return box**dim
    elif ndim == 1 and box.shape[0] == dim:
        return np.prod(box)
    elif ndim == 2 and box.shape == (dim, dim):
        a, b, c = box
        return np.cross(a, b) @ c
    else:
        raise ValueError(f"Box shape is not acceptable, {box.shape}")


def calculate_virial(box: Box, stress: Stress, *, dim: int = 3) -> Virial:
    box = np.array(box)
    stress = np.array(stress)
    volume = calculate_volume(box=box, dim=dim)
    virial = stress * volume
    return virial
