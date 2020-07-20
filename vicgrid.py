from datums import AGD66
from constants.vicgrid import N0 as N0_vicgrid
from constants.vicgrid94 import N0 as N0_vicgrid94
from vicgrid94 import geographic_to_vicgrid94

"""
VICGRID is identical to VICGRID94 but with a different false northing
"""

def geographic_to_vicgrid(dLat, dLng, datum=AGD66):
    delta = N0_vicgrid - N0_vicgrid94
    X, Y, m, γ = geographic_to_vicgrid94(dLat=dLat, dLng=dLng, datum=datum)
    return X, Y + delta, m, γ

def vicgrid_to_geographic():
    pass