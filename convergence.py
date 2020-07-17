import math

def convergence(lat, lng):
    """
    Compute the grid convergence in decimal degrees for
    latitude and longitude coordinates in the MGA (Map Grid of Australia) zones.
    Does not depend on datum so should work for gda94 & gda20 (and future datums). 

    Grid convergence will increase away from the zone's central meridian,
    and will equal 0 at the central meridian.
    """

    lat, lng = float(lat), float(lng)

    assert -85 < lat < 85, "latitude value {} is outside feasible bounds".format(lat)
    assert 108 < lng < 156, "longitude value {} is outside MGA zones".format(lng)

    # MGA zones of longitude
    mga_zones = {
        (108, 114): 49,
        (114, 120): 50,
        (120, 126): 51,
        (126, 132): 52,
        (132, 138): 53,
        (138, 144): 54,
        (144, 150): 55,
        (150, 156): 56,
    }

    # central meridian longitude of MGA zones
    cm_long = {49: 111, 50: 117, 51: 123, 52: 129, 53: 135, 54: 141, 55: 147, 56: 153}

    zone = next(zn for (lb, ub), zn in mga_zones.items() if lb < lng <= ub)
    central_meridial = cm_long[zone]

    dev = math.radians(lng - central_meridial)

    latitude = math.radians(lat)

    grid_convergence_rad = math.atan(-math.sin(latitude) * math.tan(dev))
    grid_convergence_deg = math.degrees(grid_convergence_rad)

    return grid_convergence_deg
