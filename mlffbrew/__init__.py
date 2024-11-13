__author__ = "Minwoo Kim"
__email__ = "minu928@snu.ac.kr"


try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unkown"


from mlffbrew import slurm
from mlffbrew import programs
from mlffbrew import unit
from mlffbrew import space

__all__ = ["slurm", "programs", "unit", "space"]
