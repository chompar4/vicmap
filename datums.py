from ellipsoids import reference_ellipsoids

class Datum:
    def __init__(self, code, name, ellipsoid_code):
        """
        creates a geodetic datum from a reference ellipsoid.
        Note: the plural of datum is datums, not data.
        """
        self.ellipsoid = reference_ellipsoids[ellipsoid_code]
        self.code = code
        self.name = name

    @property
    def a(self):
        return self.ellipsoid.a

    @property
    def b(self):
        return self.ellipsoid.b

    @property
    def e2(self):
        return self.ellipsoid.e2

    @property
    def e(self):
        return self.ellipsoid.e

    @property
    def n(self):
        return self.ellipsoid.n

    @property
    def f(self):
        return self.ellipsoid.f
        
    @property
    def ellipsoidal_constants(self):
        return (self.a, self.b, self.f, self.e, self.e2, self.n)


# supported datums
GDA20 = Datum(
    code="GDA20", 
    name="Geocentric Datum of Australia 2020", 
    ellipsoid_code="GRS80",
)

GDA94 = Datum(
    code="GDA94", 
    name="Geocentric Datum of Australia 1994", 
    ellipsoid_code="GRS80",
)

AGD84 = Datum(
    code="AGD84", 
    name="Australian Geodetic Datum 1984", 
    ellipsoid_code="ANS",
)

AGD66 = Datum(
    code="AGD66", 
    name="Australian Geodetic Datum 1966", 
    ellipsoid_code="ANS",
)