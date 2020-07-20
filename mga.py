from projections import utm
import math
from geodesy.datums import GDA20, GDA94
from geodesy.points import UTMPoint
from geodesy.grids import MGA


def geo_to_mga(point):
    """
    Perform a transformation from GDA20 or GDA94 geographic
    coordinates to MGA grid coordinates. UTM transformation
    depends only on the ellipsoidal constants of the datum.
    Accepts:
        dLat: latitude in decimal degrees (-90, 90]
        dLng: longitude in decimal degrees (-180, 180]
        datum: default GDA20
    returns: 
        z: Zone
        E: UTM Easting
        N: UTM Northing
        m: Point Scale Factor
        γ: Grid Convergence
    """

    dLat, dLng = point.dLat, point.dLng
    datum = point.datum

    assert datum in [GDA20, GDA94], "Please specify your coordinates in GDA20 or GDA94"
    print("({}, {}) -> MGA using {} datum".format(dLat, dLng, datum.name))

    zone = MGA.get_zone(dLng)

    E, N, m, γ = utm(dLat, dLng, ellipsoid=datum.ellipsoid, grid=MGA)
    return UTMPoint(zone, E, N, grid=MGA)


def mga_to_geographic(E, N):
    """
    Inverse transformation from MGA coords to 
    geographic coords.
    """
    pass
