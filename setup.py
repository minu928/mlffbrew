from pathlib import Path
from setuptools import setup, find_packages


version_dict = {}
with open(Path(__file__).parents[0] / "mlffbrew/_version.py") as this_v:
    exec(this_v.read(), version_dict)
version = version_dict["version"]
del version_dict


setup(
    name="mlffbrew",
    version=version,
    author="Minwoo Kim",
    author_email="minu928@snu.ac.kr",
    url="https://github.com/minu928/mlffbrew",
    install_requies=[],
    description="Package for brewing the machine learning force field.",
    packages=find_packages(),
    keywords=["MachineLearningForceField", "MolecularDynamics", "DensityFunctionalTheory"],
    python_requires=">=3.10",
    package_data={"": ["*"]},
    install_requires=["numpy>=1.22.3,<2.0.0", "atombrew>=0.0.9"],
    zip_safe=False,
)
