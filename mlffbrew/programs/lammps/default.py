from mlffbrew.typing import ScriptData


script_data: ScriptData = {
    "variable": {
        "NSTEPS": None,
        "TEMP": None,
        "PRES": None,
        "THERMO_FREQ": None,
        "DUMP_FREQ": None,
        "TIME_STEP": None,
        "TAU_T": None,
        "TAU_P": None,
        "SEED": None,
    },
    "units": "metal",
    "boundary": "p p p",
    "atom_style": "atomic",
    "neighbor": "1.0 bin",
    "mass": {"1": "1.008000", "2": "15.999000"},
    "pair_style": "gen_deepmd",
    "pair_coeff": "* *",
    "thermo_style": "custom step temp pe ke etotal press vol lx ly lz xy xz yz",
    "thermo": "${THERMO_FREQ}",
    "dump": "gen_dump",
    "velocity": "gen_velocity",
    "fix": {"gen_npt": None},
    "timestep": "${V_TIME_STEP}",
    "run": "${NSTEPS} upto",
}
