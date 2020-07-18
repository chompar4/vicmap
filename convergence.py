import math
from utils import get_cm

radians = math.radians
sin = math.sin 
tan = math.tan 
degrees = math.degrees
atan = math.atan

def convergence(lat, lng):
    """
    gives the angle between the meridian
    and the grid-line parallel to the u-axis
    # TODO: get_cm only returns values inside MGA zones
    Works for both GDA20 and GDA94.
    accepts: 
        lat: latitude in decimal degrees 
        lng: longitude in decimal degrees
    returns 
        dG: grid convergence in decical degrees
    """

    dLat, dLng = float(lat), float(lng)

    assert -85 < dLat < 85, "latitude value {} is outside feasible bounds".format(lat)
    assert 108 < dLng < 156, "longitude value {} is outside MGA zones".format(lng)

    dev = radians(dLng - get_cm(dLng))
    rLat = radians(dLat)
    rG = atan(-sin(rLat) * tan(dev))
    dG = degrees(rG)

    return dG