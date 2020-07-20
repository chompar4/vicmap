from math import sqrt

semi_major_axis = {
    "WGS84": 6378137,
    "GRS80": 6378137,
    "ANS": 6378160,
    "CLARKE": 6378350.871924,
}

reciprocal_flattening = {
    "WGS84": 298.257223563,
    "GRS80": 298.257222101,
    "ANS": 298.25,
    "CLARKE": 294.26,
}

class ReferenceEllipsoid:
    """
    Commonly reffered to as a spheroid.
    creates a reference ellipsoid with paramaters
        a: semi-major axis length (m)
        a: semi-minor axis length (m)
        f: flattening
        _f: reciprocal of flattening
        e: first eecentricity 
        e2: first eecentricity squared
        n: third flattening
    Each registered ellipsoid has a url:
        url: https://epsg.io/{epsg_code}-ellipsoid
    """
    def __init__(self, code, name, epsg_code):
        self.a = semi_major_axis[code]
        self._f = reciprocal_flattening[code]
        self.code = code
        self.name = name
        self.epsg_code = epsg_code

    @property
    def url(self):
        return "https://epsg.io/{}-ellipsoid".format(self.epsg_code)

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
        return self.f / (2 - self.f)

    @property
    def f(self):
        return 1/self._f


# supported reference ellipsoids
WGS84 = ReferenceEllipsoid(
    code="WGS84",
    name="World Geodetic System 1984", 
    epsg_code=7030,
)

GRS80 = ReferenceEllipsoid(
    code="GRS80", 
    name="Geodetic Reference System 1980", 
    epsg_code=7019,
)

ANS = ReferenceEllipsoid(
    code="ANS", 
    name="Australian National Spheroid",
    epsg_code=7003,
)

CLARKE = ReferenceEllipsoid(
    code= "CLARKE", 
    name= "Clarke 1866 Spheroid", 
    epsg_code=7008,
)

reference_ellipsoids = {
    e.code: e
    for e in [WGS84, GRS80, ANS, CLARKE]
}