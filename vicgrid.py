from datums import AGD66
from constants.vicgrid import N0 as N0_vicgrid
from constants.vicgrid94 import N0 as N0_vicgrid94
from vicgrid94 import geographic_to_vicgrid94

"""

It should be noted that the VICGRID94 projection incorporates 
a different origin specification to VICGRID in order to avoid 
confusion between coordinates generated by the two projections. 
The northing false origin for VICGRID94 has been adopted as 2,500,000
metres south of the intersection of the parallel of latitude 37S 
and the central meridian rather than the 4,500,000 specified for
the original VICGRID. The easting false origin remains unchanged 
at 2,500,000 metres west of the intersection of the parallel of 
latitude 37o S and the central meridian.

The formulae to compute Eastings and Northings for VICGRID / VICGRID94
are the same. However it should be noted that different ellipsoids apply
to the datum's relating to VICGRID and VICGRID94. VICGRID uses the
Australian Geodetic Datum 1966, which adopts the Australian National
Spheroid (ANS). VICGRID94 uses the Geocentric Datum of Australia,
which adopts the Geodetic Reference System 1980 (GRS80) ellipsoid.
The constants for the semi major axis and inverse flattening are 
different for ANS and GRS80.

"""

def geographic_to_vicgrid(dLat, dLng, datum=AGD66):
    delta = N0_vicgrid - N0_vicgrid94
    X, Y, m, γ = geographic_to_vicgrid94(dLat=dLat, dLng=dLng, datum=datum)
    return X, Y + delta, m, γ

def vicgrid_to_geographic():
    pass