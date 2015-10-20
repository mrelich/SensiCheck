
from math import cos, pi

# Common constants
livetime  = 365 * 24 * 60 * 60 # livetime in s
astronorm = 1e-8               # Normalized at 100TeV


# Muon constants
MuSolidAngle = 2 * pi * (1 + cos(85*pi/180)) / 1e-4
