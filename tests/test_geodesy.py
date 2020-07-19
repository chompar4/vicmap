
from geodesy import geographic_to_mga, geographic_to_vicgrid94

def test_geographic_to_mga():

    z, E, N, m, γ = geographic_to_mga(-23.67012389, 133.8855133)

    assert z == 53
    assert round(E, 2) == round(386352.397753, 2)
    assert round(N, 2) == round(7381850.768886, 2)
    assert round(m, 9) == 0.999759539
    assert round(γ, 9) == -0.447481414

def test_geographic_to_vicgrid94_origin():
    # origin of crs
    e, n = geographic_to_vicgrid94(-59.6, 126.72)
    assert e == 0
    assert n == 0

def test_geographic_to_vicgrid94_center():
    # center of vic
    e, n = geographic_to_vicgrid94(-37, 145)
    assert e == 2500000
    assert n == 2500000


def test_known_vals():

    lat = -39.06611111
    lng = 145.163227

    e, n = geographic_to_vicgrid94(lat, lng)
    assert e == 2514311.897
    assert n == 2374602.216