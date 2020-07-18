import math
from utils import get_cm

def convergence(lat, lng):
    """
    Compute the grid convergence in decimal degrees for
    latitude and longitude coordinates in the MGA (Map Grid of Australia) zones.
    # TODO: get_cm only returns values inside MGA zones
    Works for both GDA20 and GDA94.
    accepts: 
        lat: latitude in decimal degrees 
        lng: longitude in decimal degrees
    returns 
        dG: grid convergence in decical degrees
    """

    lat, lng = float(lat), float(lng)

    assert -85 < lat < 85, "latitude value {} is outside feasible bounds".format(lat)
    assert 108 < lng < 156, "longitude value {} is outside MGA zones".format(lng)

    dev = math.radians(lng - get_cm(lng))
    latitude = math.radians(lat)
    rG = math.atan(-math.sin(latitude) * math.tan(dev))
    dG = math.degrees(rG)

    return dG


if __name__ == "__main__":
    print(convergence(80, 155))