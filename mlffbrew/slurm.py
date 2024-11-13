import os
from typing import Literal, Dict


def squeue(*, jobname: str = None, hostname: str = None, username: str = None, fmt: str = None) -> list[str]:
    cmd = f"ssh {hostname}" if hostname is not None else ""
    cmd += f" squeue -h"
    cmd += f" -n {jobname}" if jobname is not None else ""
    cmd += f" -u {username}" if username is not None else ""
    cmd += f" -o {fmt}" if fmt is not None else ""
    return os.popen(cmd=cmd).readlines()


def sbatch(script: str, *, hostname: str = None, remote_path: str = None) -> str:
    ssh_command = f"ssh -t {hostname} " if hostname else ""
    script = str(script)
    if not os.path.isfile(script):
        raise FileNotFoundError(f"Script is not found. {script}")
    cmd = f"{ssh_command} 'bash -l -c \"cd {remote_path} && sbatch {script}\"'"
    return os.popen(cmd=cmd).read().split()[-1].rstrip()


def query(
    jobid: str, *, hostname: str = None, sep: str = "~"
) -> Dict[Literal["id", "jobname", "username", "status"], str]:
    jobid = str(jobid)
    for line in squeue(hostname=hostname, fmt=f"'%i{sep}%j{sep}%u{sep}%t'"):
        id_, jobname, username, status = line.split(sep=sep)
        if id_ == jobid:
            return {"id": id_, "jobname": jobname, "username": username, "status": status}
    raise LookupError(f"Not find the jobid({jobid})")
