from projections import utm
import math
from geodesy.datums import GDA20, GDA94
from geodesy.points import UTMPoint, GeoPoint, PlanePoint
from geodesy.grids import MGA20, MGA94


def geo_to_mga(point):
    """
    Perform a transformation from GDA20 or GDA94 geographic
    coordinates to MGA grid coordinates. UTM transformation
    depends only on the ellipsoidal constants of the datum.
    """

    assert isinstance(point, GeoPoint), "Please provide a GeoPoint() instance"

    dLat, dLng = point.dLat, point.dLng
    datum = point.datum
    grid = MGA94 if datum == GDA94 else MGA20

    assert datum in [GDA20, GDA94], "Please specify your coordinates in GDA20 or GDA94"
    print(f"({dLat}, {dLng}) -> {grid.name} using {datum.name} datum")

    zone = grid.get_zone(dLng)

    E, N, m, γ = utm(dLat, dLng, ellipsoid=datum.ellipsoid, grid=grid)
    return UTMPoint(zone, E, N, grid=grid)


def mga_to_geographic(point, datum=GDA20):
    """
    Inverse transformation from MGA coords to 
    geographic coords. Defaults to most recent GDA20 datum.
    """

    assert isinstance(point, PlanePoint), "Please provide a PlanePoint() instance"
    grid = point.grid

    assert grid in [GDA20, GDA94], "Please specify your coordinates in GDA20 or GDA94"
    print("({}, {}) -> MGA using {} datum".format(dLat, dLng, datum.name))

    raise NotImplementedError

    return GeoPoint(dLat, dLng, datum)
