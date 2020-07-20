from math import sqrt

semi_major_axis = {
    "WGS84": 6378137,
    "GRS80": 6378137,
    "ANS": 6378160,
}

reciprocal_flattening = {
    "WGS84": 298.257223563,
    "GRS80": 298.257222101, 
    "ANS": 298.25,
}

class ReferenceEllipsoid:
    """
    Commonly reffered to as a spheroid, which is confusing.
    creates a reference ellipsoid with paramaters
            a: semi-major axis length (m)
            a: semi-minor axis length (m)
            f: flattening
            _f: reciprocal of flattening
            e: first eecentricity 
            e2: first eecentricity squared
            n: third flattening
    """
    def __init__(self, code, name):
        self.a = semi_major_axis[code]
        self._f = reciprocal_flattening[code]
        self.code = code
        self.name = name 

    @property
    def b(self):
        return self.a / (1 - self.f)

    @property
    def e2(self):
        return self.f * (2-self.f)
    
    @property
    def e(self):
        return sqrt(self.e2)

    @property
    def n(self):
        return (self.a - self.b) / (self.a + self.b)

    @property
    def f(self):
        return 1/self._f


# supported reference ellipsoids
WGS84 = ReferenceEllipsoid(
    code="WGS84", 
    name="World Geodetic System 1984"
)

GRS80 = ReferenceEllipsoid(
    code="GRS80", 
    name=" Geodetic Reference System 1980 "
)

ANS = ReferenceEllipsoid(
    code="ANS", 
    name="Australian National Spheroid",
)

reference_ellipsoids = {
    e.code: e
    for e in [WGS84, GRS80, ANS]
}