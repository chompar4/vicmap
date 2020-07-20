from projections import utm
import math
from constants.mga import cm_mga_zone, cm_zone1, zone0_edge, zone_width, m0, E0, N0
from datums import GDA20


def get_zone(dLng):
    """
    gives the MGA zone containing dLng
    """
    return math.floor((dLng - zone0_edge) / zone_width)


def get_cm(dLng):
    """
    gives the central meridian longitude of the MGA zone containing dLng
    """
    return cm_mga_zone[get_zone(dLng)]


def geo_to_mga(dLat, dLng, datum=GDA20):
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

    print("({}, {}) -> MGA using {} datum".format(dLat, dLng, datum.name))

    zone = get_zone(dLng)
    cm = get_cm(dLng)

    E, N, m, γ = utm(dLat, dLng, cm, m0, E0, N0, datum)
    return zone, E, N


def mga_to_geographic(E, N):
    """
    Inverse transformation from MGA coords to 
    geographic coords.
    """
    pass
