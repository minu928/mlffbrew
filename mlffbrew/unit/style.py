from mlffbrew.unit._dataclass import StateUnit


metal = StateUnit(
    energy="eV",
    coords="angstrom",
    atoms=None,
    force="eV/angstrom",
    stress="eV/angstrom^3",
    box="angstrom",
    virial="eV",
)
