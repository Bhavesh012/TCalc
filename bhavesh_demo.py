import astropy.units as u
from bhavesh import telescope

c8 = telescope(203.2, 10, 40, 52*u.deg)
print(c8.calc_mag())