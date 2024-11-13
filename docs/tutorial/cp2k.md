# Tutorial-`mlff.programs.cp2k`
[CP2K HomePage](https://www.cp2k.org/)

## How to Parse the LogFile of CP2K

``` python
from mlffbrew.programs import cp2k


logfile = "./example/results/cp2k.output"
data, unit = cp2k.opener.parse_logfile(logfile)
print(f"{data=}")
print(f"{unit=}")
```

## How to Change the Unit of Data

``` python
from mlffbrew.programs import cp2k


logfile = "./example/results/cp2k.output"
data, unit = cp2k.opener.parse_logfile(logfile)
metal_unit = mb.unit.style.metal
converted_data = mb.unit.convert(data, old_units=unit, new_units=metal_unit)
print(f"{converted_data=}")
```

## How to Calculate the Virial

``` python
from mlffbrew.programs import cp2k


logfile = "./example/results/cp2k.output"
data, unit = cp2k.opener.parse_logfile(logfile)
virial = mb.space.calculate_virial(data.box, data.stress)
converted_data.virial = virial
print(f"{data=}")
```