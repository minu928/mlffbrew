from mlffbrew.typing import List, npstr

__all__ = ["build"]


def build(
    script: str,
    coords_files: List[npstr],
    *,
    workspace: str = "./",
    folderhead: str = "cp2k",
    exist_ok: bool = False,
    maxint: int = 4,
) -> None:

    try:
        import os
        import atombrew as atb
        from copy import deepcopy
        from mlffbrew.programs import cp2k
    except:
        raise ImportError("Can Not Import.")

    script_info = cp2k.scripter.read(script) if isinstance(script, str) else script
    for i, coords_file in enumerate(coords_files):
        folder_path = os.path.join(workspace, f"{folderhead}.{str(i).zfill(maxint)}")
        os.makedirs(folder_path, exist_ok=exist_ok)
        home = atb.Home(coords_file)

        # * Write Coord
        coord_path = os.path.join(folder_path, "run.xyz")
        home.write(coord_path, mode="w+")

        # * Write Script
        box = home.box
        data = deepcopy(script_info)
        data = cp2k.scripter.modify_coord(data=data)
        data = cp2k.scripter.modify_box(data=data, box=box)
        file = os.path.join(folder_path, "run.inp")
        cp2k.scripter.write(file=file, data=data, mode="w+")
