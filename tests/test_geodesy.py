
from geodesy import geographic_to_grid

def test_geographic_to_grid():

    z, E, N, m, γ = geographic_to_grid(-23.67012389, 133.8855133)

    assert z == 53
    assert E == 386352.397753
    assert N == 7381850.768886
    assert m == 0.999759539
    assert γ == -0.447481418

