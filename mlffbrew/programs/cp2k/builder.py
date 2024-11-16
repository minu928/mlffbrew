from typing import List
from mlffbrew.typing import ScriptFileOrScriptData, ScriptFile, ScriptData, FilePath

__all__ = ["build"]


def build(
    script: ScriptFileOrScriptData,
    coords_files: List[FilePath],
    *,
    workspace: str = "./",
    folderhead: str = "cp2k",
    exist_ok: bool = False,
    maxint: int = 4,
) -> None:

    try:
        import os
        from atombrew import Home
        from copy import deepcopy
        from mlffbrew.programs import cp2k
    except Exception as e:
        raise ImportError(f"Can Not Import, {e}")

    script_data: ScriptData = cp2k.scripter.read(script) if isinstance(script, ScriptFile) else script
    abs_workpath = os.path.abspath(workspace)
    for i, coords_file in enumerate(coords_files):
        folder_path = os.path.join(abs_workpath, f"{folderhead}.{str(i).zfill(maxint)}")
        os.makedirs(folder_path, exist_ok=exist_ok)
        home = Home(coords_file)

        # * Write Coord
        coord_path = os.path.join(folder_path, "run.xyz")
        home.write(coord_path, mode="w+")

        # * Write Script
        box = home.box
        data = deepcopy(script_data)
        data = cp2k.scripter.modify_coord(data=data)
        data = cp2k.scripter.modify_box(data=data, box=box)
        file = os.path.join(folder_path, "run.inp")
        cp2k.scripter.write(file=file, data=data, mode="w+")
