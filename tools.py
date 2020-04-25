import math


def gda20_convergence(lat, lng):
    """
    Compute the grid convergence in decimal degrees for
    latitude and longitude coordinates in the MGA (Map Grid of Australia)
    zones 54 & 55 (VIC).
    # TODO: generalize to entire MGA (Map Grid of Australia)
    """

    lat, lng = float(lat), float(lng)

    assert -85 < lat < 85, "latitude value is outside zone 54 & 55"
    assert 138 < lng < 150, "longitude value is outside zone 54 & 55"

    z54, z55 = 141, 147  # TODO: generalize
    zone = 54 if lng < 144 else 55
    o = z54 if zone == 54 else z55

    h = math.tan(math.pi * (lng - o) / 180)

    latitude, longitude = math.radians(lat), math.radians(lng)

    grid_convergence_rad = math.atan(-math.sin(latitude) * h)
    grid_convergence_deg = math.degrees(grid_convergence_rad)

    return grid_convergence_deg
