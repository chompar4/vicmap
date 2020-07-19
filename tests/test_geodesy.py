import pytest
from geodesy import geographic_to_mga, geographic_to_vicgrid94

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
    (-34.49482703, 141.988775, 2223259.175, 2773628.391),
    (-38.06494464, 141.415905, 2185545.806, 2375895.467),
    (-37.39435028, 148.7786631, 2834469.388, 2449602.655),
    (-36.01615208, 145.163227, 2590104.617, 2608691.847),
    (-39.06611111, 145.163227, 2514311.897, 2374602.216), 
]

@pytest.mark.parametrize("lat,lng,E,N", known_vals94)
def test_known_vals_94(lat, lng, E, N):

    e, n = geographic_to_vicgrid94(lat, lng)
    assert round(e, 2) == round(E, 2)
    assert round(n, 2) == round(N, 2)