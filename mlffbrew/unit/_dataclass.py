from dataclasses import dataclass


@dataclass
class StateUnit:
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
