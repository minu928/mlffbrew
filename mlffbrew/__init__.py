__author__ = "Minwoo Kim"
__email__ = "minu928@snu.ac.kr"


try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unkown"


from samsarabrew import slurm
from samsarabrew import programs
from samsarabrew import unit
from samsarabrew import space

__all__ = ["slurm", "programs", "unit", "space"]
