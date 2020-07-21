import math


class MGAGrid:
    def __init__(self, E0, N0, m0, zw, cm1):
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

    def get_cm(self, zn):
        return self.cms[zn]


class VICGRID:
    def __init__(self, φ1, φ2, E0, N0, φ0, λ0):
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
        self.E0 = E0
        self.N0 = N0
        self.φ1 = φ1
        self.φ2 = φ2
        self.λ0 = λ0
        self.φ0 = φ0

    @property
    def constants(self):
        return (self.φ1, self.φ2, self.λ0, self.φ0, self.E0, self.N0)


class VICGRID94(VICGRID):
    def __init__(self, φ1, φ2, E0, N0, φ0, λ0):
        """
        Representation of the VICGRID94 plane.
        Identical to VICGRID with a different false northing.
        """
        super().__init__(φ1, φ2, E0, N0, φ0, λ0)


MGA = MGAGrid(E0=500000, N0=10000000, m0=0.9996, zw=6, cm1=-177)
VICGRID = VICGRID(φ1=-36, φ2=-38, E0=2500000, N0=4500000, φ0=-37, λ0=145)
VICGRID94 = VICGRID94(φ1=-36, φ2=-38, E0=2500000, N0=2500000, φ0=-37, λ0=145)

