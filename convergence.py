import math


def gda20_convergence(lat, lng):
    """
    Compute the grid convergence in decimal degrees for
    latitude and longitude coordinates in the MGA (Map Grid of Australia)
    zones 54 & 55 (VIC).
    # TODO: generalize to entire MGA (Map Grid of Australia)
    """

    lat, lng = float(lat), float(lng)

    assert -85 < lat < 85, "latitude value {} is outside zone 54 & 55".format(lat)
    assert 138 < lng < 150, "longitude value {} is outside zone 54 & 55".format(lng)

    # central meridian longitude of MGA zone
    cm_long = {49: 111, 50: 117, 51: 123, 52: 129, 53: 135, 54: 141, 55: 147, 56: 153}

    zone = 54 if 138 < lng < 144 else 55
    dev = math.radians(lng - cm_long[zone])

    latitude, longitude = math.radians(lat), math.radians(lng)

    grid_convergence_rad = math.atan(-math.sin(latitude) * math.tan(dev))
    grid_convergence_deg = math.degrees(grid_convergence_rad)

    return grid_convergence_deg
