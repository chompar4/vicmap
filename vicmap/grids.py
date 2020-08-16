import math
from vicmap.datums import GDA20, GDA94, AGD66
from pyproj import CRS


class MGAGrid:

    base_code = 283  # epsg

    def __init__(self):
        """
        Representation of the MGA (Map Grid of Australia) plane.
        A specific UTM grid in the plane defined for australia.
        Origin Datum
            GDA94 / GDA20 only
        accepts
            E0: false easting (m)
            N0: false northing (m)
            m0: central scale factor
            zw: zone width (degrees longitude)
            cm1: central meridians of zone 1
        computes
            zones: all zones in the UTM grid
            z0_edge: longitude of western edge of the 0th zone
        """
        self.E0 = 500000
        self.N0 = 10000000
        self.m0 = 0.9996
        self.zw = 6
        self.cm1 = -177

    def epsg_code(self, zone):
        """
        MGA has a different epsg code for each zone, 
        following the pattern: `283{z}` 
        where z is the zone of projection.
        """
        return int(f"{self.base_code}{zone}")

    def crs(self, zone):
        return CRS.from_epsg(self.epsg_code(zone))

    @property
    def cms(self):
        """
        gives a dictionary of central meridians for each MGA zone
        """
        cms = {}
        idx = 1
        cm = self.cm1
        while cm < 180:
            cms[idx] = cm
            cm += self.zw
            idx += 1
        return cms

    @property
    def z0_edge(self):
        return self.cms[1] - 1.5 * self.zw

    def get_zone(self, dLng):
        """
        gives the MGA zone containing dLng
        """
        return math.floor((dLng - self.z0_edge) / self.zw)

    def get_cm(self, zn):
        return self.cms[zn]


class MGAGrid20(MGAGrid):
    datum = GDA20
    name = "Map Grid of Australia (2020)"


class MGAGrid94(MGAGrid):
    datum = GDA94
    name = "Map Grid of Australia (1994)"


class VICGRID:

    datum = AGD66
    epsg_code = 3110

    def __init__(self):
        """
        Representation of the VICGRID plane.
        Contains all constants required for projection.
        Origin Datum 
            AGD66 only
        accepts 
            φ1, φ2: standard parralels
            E0: false easting (m)
            N0: false northing (m)
            φ0: origin parrallel latitude (degrees)
            λ0: central meridian longitude (degrees)
        """
        self.E0 = 2500000
        self.N0 = 4500000
        self.φ1 = -36
        self.φ2 = -38
        self.λ0 = 145
        self.φ0 = -37
        self.r0 = 8472630.5

    @property
    def crs(self):
        return CRS.from_epsg(self.epsg_code)

    @property
    def constants(self):
        return (self.φ1, self.φ2, self.λ0, self.φ0, self.E0, self.N0)


class VICGRID94(VICGRID):

    datum = GDA94
    epsg_code = 3111

    def __init__(self):
        """
        Representation of the VICGRID94 plane.
        Identical to VICGRID with a different false northing.
        Contains all constants required for projection.
        Origin Datum 
            AGD66 only
        accepts 
            φ1, φ2: standard parralels
            E0: false easting (m)
            N0: false northing (m)
            φ0: origin parrallel latitude (degrees)
            λ0: central meridian longitude (degrees)
        """
        self.E0 = 2500000
        self.N0 = 2500000
        self.φ1 = -36
        self.φ2 = -38
        self.λ0 = 145
        self.φ0 = -37
        self.r0 = 8472630.5


MGA94 = MGAGrid94()
MGA20 = MGAGrid20()
VICGRID = VICGRID()
VICGRID94 = VICGRID94()

