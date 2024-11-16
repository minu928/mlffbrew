from mlffbrew.typing import ScriptData


script_data: ScriptData = {
    "model": {
        "type_map": ["H", "O"],
        "descriptor": {
            "type": "se_e2_a",
            "sel": [96, 48],
            "rcut_smth": 0.5,
            "rcut": 6.0,
            "neuron": [25, 50, 100],
            "resnet_dt": False,
            "axis_neuron": 12,
            "seed": None,
            "activation_function": "gelu_tf",
        },
        "fitting_net": {
            "neuron": [240, 240, 240],
            "resnet_dt": False,
            "seed": None,
        },
    },
    "learning_rate": {
        "type": "exp",
        "decay_steps": 5000,
        "start_lr": 0.001,
        "stop_lr": 3.51e-08,
    },
    "loss": {
        "start_pref_e": 0.02,
        "limit_pref_e": 1,
        "start_pref_f": 1000,
        "limit_pref_f": 1,
        "start_pref_v": 0.01,
        "limit_pref_v": 1,
    },
    "training": {
        "training_data": {
            "systems": ["../00.data/training_data"],
            "batch_size": "auto",
            "_comment": "that's all",
        },
        "validation_data": {
            "systems": ["../00.data/validation_data/"],
            "batch_size": "auto",
            "numb_btch": 1,
            "_comment": "that's all",
        },
        "numb_steps": 1000000,
        "seed": None,
        "disp_file": "lcurve.out",
        "disp_freq": 1000,
        "save_freq": 1000,
    },
}
