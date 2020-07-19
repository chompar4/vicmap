
from geodesy import geographic_to_utm

def test_geographic_to_utm():

    z, E, N, m, γ = geographic_to_utm(-23.67012389, 133.8855133)

    assert z == 53
    assert round(E, 2) == round(386352.397753, 2)
    assert round(N, 2) == round(7381850.768886, 2)
    assert round(m, 9) == 0.999759539
    assert round(γ, 9) == -0.447481414

