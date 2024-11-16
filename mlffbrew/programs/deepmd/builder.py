from typing import List
from mlffbrew.typing import ScriptFileOrScriptData, ScriptData, ScriptFile, FilePath


INPUT_FILE_NAME = "deepmd.json"


def build(
    script: ScriptFileOrScriptData,
    training_data: List[FilePath],
    *,
    n_ensemble: int = 4,
    workspace: str = "./",
    folderhead: str = "deepmd",
    exist_ok: bool = False,
    maxint: int = 4,
):
    try:
        import os
        from copy import deepcopy
        from mlffbrew.programs import deepmd
    except Exception as e:
        raise ImportError(f"Can Not Import, {e}")

    script_data: ScriptData = deepmd.scripter.read(script) if isinstance(script, ScriptFile) else script
    abs_workpath = os.path.abspath(workspace)
    for i in range(n_ensemble):
        folder_path = os.path.join(abs_workpath, f"{folderhead}.{str(i).zfill(maxint)}")
        os.makedirs(folder_path, exist_ok=exist_ok)

        this_script_data = deepcopy(script_data)
        this_script_data = deepmd.scripter.modify_seed(this_script_data)
        this_script_data = deepmd.scripter.modify_training(this_script_data, training_data=training_data)
        file = os.path.join(folder_path, INPUT_FILE_NAME)
        deepmd.scripter.write(file=file, data=this_script_data, mode="w+")
