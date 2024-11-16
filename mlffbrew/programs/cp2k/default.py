from mlffbrew.typing import ScriptData


script_data: ScriptData = {
    "GLOBAL": {
        "PROJECT": "RUN",
        "RUN_TYPE": "ENEGY_FORCE",
    },
    "FORCE_EVAL": {
        "METHOD": "Quickstep",
        "STRESS_TENSOR": "ANALYTICAL",
        "DFT": {
            "BASIS_SET_FILE_NAME": "BASIS_MOLOPT_SCAN",
            "POTENTIAL_FILE_NAME": "GTH_POTENTIALS_SCAN",
            "CHARGE": 0,
            "MULTIPLICITY": 1,
            "MGRID": {
                "CUTOFF": 1200,
                "REL_CUTOFF": 60,
                "NGRIDS": 5,
            },
            "QS": {
                "METHOD": "GPW",
                "EPS_DEFAULT": 1.0e-14,
                "EXTRAPOLATION": "ASPC",
            },
            "POISSON": {
                "PERIODIC": "XYZ",
            },
            "SCF": {
                "SCF_GUESS": "RESTART",
                "MAX_SCF": 50,
                "EPS_SCF": 1.0e-7,
                "OUTER_SCF": {
                    "EPS_SCF": 1.0e-7,
                    "MAX_SCF": 10,
                },
                "OT": {"PRECONDITIONER": "FULL_SINGLE_INVERSE", "MINIMIZER": "CG"},
            },
            "XC": {
                "XC_FUNCTIONAL": {
                    "MGGA_X_R2SCAN": {},
                    "MGGA_C_R2SCAN": {},
                }
            },
        },
        "SUBSYS": {
            "CELL": {
                "A": "12.6 0.0 0.0",
                "B": "0.0 12.6 0.0",
                "C": "0.0 0.0 12.6",
            },
            "TOPOLOGY": {"COORD_FILE_NAME": "./run.xyz", "COORD_FILE_FORMAT": "XYZ"},
            "KIND H": {
                "BASIS_SET": "TZV2P-MOLOPT-SCAN-GTH-q1",
                "POTENTIAL": "GTH-SCAN-1",
            },
            "KIND O": {
                "BASIS_SET": "TZV2P-MOLOPT-SCAN-GTH-q6",
                "POTENTIAL": "GTH-SCAN-6",
            },
        },
    },
}
