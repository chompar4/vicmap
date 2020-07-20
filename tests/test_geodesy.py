import pytest
from geodesy import geographic_to_mga, geographic_to_vicgrid94
from utils import dms_to_dd
import math

def test_geographic_to_mga():

    z, E, N, m, γ = geographic_to_mga(-23.67012389, 133.8855133)

    assert z == 53
    assert round(E, 2) == round(386352.397753, 2)
    assert round(N, 2) == round(7381850.768886, 2)
    assert round(m, 9) == 0.999759539
    assert round(γ, 9) == -0.447481414

def test_geographic_to_vicgrid94_center():
    # center of vic
    e, n = geographic_to_vicgrid94(-37, 145)
    assert e == 2500000
    assert n == 2500000

known_vals94 = [
    (dms_to_dd(-34, 29, 41.377), dms_to_dd(141, 59, 19.5899), 2223259.175, 2773628.391),
    (dms_to_dd(-38, 3, 53.8007), dms_to_dd(141, 24, 57.2580), 2185545.806, 2375895.467),
    (dms_to_dd(-37, 23, 39.6610), dms_to_dd(148, 46, 43.1871), 2834469.388, 2449602.655),
    (dms_to_dd(-36, 00, 58.1475), dms_to_dd(145, 59, 58.4589), 2590104.617, 2608691.847),
    (dms_to_dd(-38, 7, 47.3418), dms_to_dd(145, 9, 47.6172), 2514311.897, 2374602.216), 
]

TOL = 1e-3

@pytest.mark.parametrize("lat,lng,E,N", known_vals94)
def test_known_vals_94_easting(lat, lng, E, N):

    e, n = geographic_to_vicgrid94(lat, lng)
    diff = abs(e-E)
    assert diff <= TOL

@pytest.mark.parametrize("lat,lng,E,N", known_vals94)
def test_known_vals_94_northing(lat, lng, E, N):

    e, n = geographic_to_vicgrid94(lat, lng)
    diff = abs(n-N)
    assert diff <= TOL

@pytest.mark.parametrize("lat,lng,E,N", known_vals94)
def test_known_vals_94_total(lat, lng, E, N):

    """ cartesian local approximation """

    e, n = geographic_to_vicgrid94(lat, lng)
    diff = math.sqrt((e-E)**2 + (n-N)**2)
    assert diff <= TOL