from pyproj import CRS

from vicmap.ellipsoids import reference_ellipsoids

"""
See: https://www.icsm.gov.au/education/fundamentals-mapping/datums/datums-explained-more-detail
"""


class Datum:
    def __init__(self, code, name, ellipsoid_code, epsg_code):
        """
        creates a geodetic datum from a reference ellipsoid.
            ellipsoid: reference ellipsoid
            crs: crs of datum coordinate system
        Note: the plural of datum is datums, not data.
        """
        self.ellipsoid = reference_ellipsoids[ellipsoid_code]
        self.crs = CRS.from_epsg(epsg_code)
        self.epsg_code = epsg_code
        self.code = code
        self.name = name


# supported datums
WGS84 = Datum(
    code="WGS84", name="World Geodetic System", ellipsoid_code="WGS84", epsg_code=4326
)

GDA20 = Datum(
    code="GDA20",
    name="Geocentric Datum of Australia 2020",
    ellipsoid_code="GRS80",
    epsg_code=7844,
)

GDA94 = Datum(
    code="GDA94",
    name="Geocentric Datum of Australia 1994",
    ellipsoid_code="GRS80",
    epsg_code=4283,
)

AGD84 = Datum(
    code="AGD84",
    name="Australian Geodetic Datum 1984",
    ellipsoid_code="ANS",
    epsg_code=4203,
)

AGD66 = Datum(
    code="AGD66",
    name="Australian Geodetic Datum 1966",
    ellipsoid_code="ANS",
    epsg_code=4202,
)

__all_datums__ = [GDA94, GDA20, WGS84, AGD84, AGD66]
