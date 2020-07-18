from convergence import convergence
from constants import cm_mga_zone
import numpy as np
import pytest

def test_known_convergence():
    assert convergence(80, 150) == -2.9545046305808174


meridian_grid = [
    (lat, cm) for lat in np.linspace(start=-75, stop=80, num=32)
    for zone, cm in cm_mga_zone.items()
]

@pytest.mark.parametrize("lat,lng", meridian_grid)
def test_meridian_convergence(lat, lng):
    assert convergence(lat, lng) == 0