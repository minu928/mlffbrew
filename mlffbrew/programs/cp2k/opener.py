from typing import Tuple
from mlffbrew.dataclass import State
from mlffbrew.unit import StateUnit
from mlffbrew.typing import FilePath


def parse_logfile(logfile: FilePath) -> Tuple[State, StateUnit]:
    data = {
        "energy": None,
        "coords": [],
        "atoms": [],
        "force": [],
        "stress": [],
        "box": [],
    }
    unit = {
        "energy": None,
        "coords": None,
        "atoms": None,
        "force": None,
        "stress": None,
        "box": None,
    }
    with open(logfile, "r") as f:
        is_coords_line_start = False
        is_force_line_start = False
        is_stress_line_start = False
        while line := f.readline():
            # LINE: box
            if line.startswith(" CELL| Vector"):
                splited_line = line.split()
                data["box"].append(splited_line[4:7])
                unit["box"] = splited_line[3][1:-2]
                continue

            # LINE: energy
            if line.startswith(" ENERGY| Total"):
                splited_line = line.split()
                this_unit = splited_line[-2][1:-2]
                if this_unit == "a.u.":
                    this_unit = "hatree"
                unit["energy"] = this_unit
                data["energy"] = splited_line[-1]
                continue

            # LINE: coords and atoms
            if "ATOMIC COORDINATES" in line:
                unit["coords"] = line.split()[-1]
                continue
            if line.startswith(" Atom  Kind  Element"):
                is_coords_line_start = True
                continue
            elif line == "\n":
                is_coords_line_start = False
                continue
            elif is_coords_line_start:
                splited_line = line.split()
                data["atoms"].append(splited_line[2])
                data["coords"].append(splited_line[4:7])
                continue

            # LINE: force
            if line.startswith(" ATOMIC FORCES in"):
                this_unit = line.split()[-1][1:-1]
                if this_unit == "a.u.":
                    this_unit = "hatree/bohr"
                unit["force"] = this_unit
            if line.startswith(" # Atom   Kind"):
                is_force_line_start = True
                continue
            elif line.startswith(" SUM OF ATOMIC"):
                is_force_line_start = False
                continue
            elif is_force_line_start:
                data["force"].append(line.split()[3:7])
                continue

            # LINE: stress
            if line.startswith(" STRESS| Analytical"):
                is_stress_line_start = True
                unit["stress"] = line.split()[-1][1:-1]
                next(f)  # skip next line
                continue
            elif line.startswith(" STRESS| 1/3"):
                is_stress_line_start = False
                continue
            elif is_stress_line_start:
                data["stress"].append(line.split()[2:])
                continue

    return State(**data), StateUnit(**unit)
