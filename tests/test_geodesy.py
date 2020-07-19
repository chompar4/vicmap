
from geodesy import geographic_to_mga, geographic_to_vicgrid94

def test_geographic_to_mga():

    z, E, N, m, γ = geographic_to_mga(-23.67012389, 133.8855133)

    assert z == 53
    assert round(E, 2) == round(386352.397753, 2)
    assert round(N, 2) == round(7381850.768886, 2)
    assert round(m, 9) == 0.999759539
    assert round(γ, 9) == -0.447481414

def test_geographic_to_vicgrid94():

    # origin
    e, n = geographic_to_vicgrid94(-59.5, 116.72)
    assert e == 0 and n == 0

    # center of vic
    e, n = geographic_to_vicgrid94(-37, 145)
    assert e == 2500000 and n == 2500000