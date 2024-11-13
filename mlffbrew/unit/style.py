from mlffbrew.dataclasses import FrameUnit


metal = FrameUnit(
    energy="eV",
    coords="angstrom",
    atoms=None,
    force="eV/angstrom",
    stress="eV/angstrom^3",
    box="angstrom",
    virial="eV",
)
