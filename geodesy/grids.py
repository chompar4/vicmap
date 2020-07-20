import math


class UTMGrid:
    pass


class MGAGrid(UTMGrid):
    def __init__(self, E0, N0, m0, zw, cm1):

        """
        Representation of the MGA (Map Grid of Australia) projection.
        A specific UTM grid in the plane defined for australia.
        Origin Datum
            GDA94 / GDA20
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

        self.E0 = E0
        self.N0 = N0
        self.m0 = m0
        self.zw = zw
        self.cm1 = cm1

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

    def get_cm(self, dLng):
        zn = self.get_zone(dLng)
        return self.cms[zn]


MGA = MGAGrid(E0=500000, N0=10000000, m0=0.9996, zw=6, cm1=-177)

