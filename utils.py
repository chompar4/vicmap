from constants import mga_zones, cm_mga_zone

def get_mga_zone(lng):
    """
    Get the zone containing longitude 'lng'
    """
    return next(zn for (lb, ub), zn in mga_zones.items() if lb < lng <= ub)

def get_cm(lng):
    """
    Get the central meridian longitude of the zone
    containing 'lng'
    """
    return cm_mga_zone[get_mga_zone(lng)]