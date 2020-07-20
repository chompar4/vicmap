from ellipsoids import reference_ellipsoids

"""
See: https://www.icsm.gov.au/education/fundamentals-mapping/datums/datums-explained-more-detail
"""


class Datum:
    def __init__(self, code, name, ellipsoid_code, reference_frame, epsg_code):
        """
        creates a geodetic datum from a reference ellipsoid.
            ellipsoid: reference ellipsoid
            reference_frame: reference_frame of datum coordinate system
        Note: the plural of datum is datums, not data.
        """
        self.ellipsoid = reference_ellipsoids[ellipsoid_code]
        self.reference_frame = reference_frame
        self.epsg_code = epsg_code
        self.code = code
        self.name = name

    @property
    def url(self):
        return "https://epsg.io/{}-datum".format(self.epsg_code)

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
WGS84 = Datum(
    code="WGS84",
    name="World Geodetic System",
    ellipsoid_code="WGS84",
    reference_frame="WGS84",
    epsg_code=6326,
)

GDA20 = Datum(
    code="GDA20",
    name="Geocentric Datum of Australia 2020",
    ellipsoid_code="GRS80",
    reference_frame="ITRF2014",
    epsg_code=1168,
)

GDA94 = Datum(
    code="GDA94",
    name="Geocentric Datum of Australia 1994",
    ellipsoid_code="GRS80",
    reference_frame="ITRF92",
    epsg_code=6283,
)

AGD84 = Datum(
    code="AGD84",
    name="Australian Geodetic Datum 1984",
    ellipsoid_code="ANS",
    reference_frame="",
    epsg_code=6203,
)

AGD66 = Datum(
    code="AGD66",
    name="Australian Geodetic Datum 1966",
    ellipsoid_code="ANS",
    reference_frame="",
    epsg_code=6202,
)

ANG = Datum(
    code="ANG",
    name="unknown",
    ellipsoid_code="CLARKE",
    reference_frame="",
    epsg_code="",
)
