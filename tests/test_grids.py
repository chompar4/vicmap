import pytest
from geodesy.grids import MGA, VICGRID, VICGRID94
import numpy as np

zones = [
    (108, 114, 49),
    (114, 120, 50),
    (120, 126, 51),
    (126, 132, 52),
    (132, 138, 53),
    (138, 144, 54),
    (144, 150, 55),
    (150, 156, 56),
]


@pytest.mark.parametrize("west,east,zn", zones)
def test_get_zone(west, east, zn):
    grid = MGA
    for lng in np.linspace(start=west, stop=east, num=10):
        if lng == east:
            assert grid.get_zone(lng) == zn + 1  # range of zones = [west, east)
        else:
            assert grid.get_zone(lng) == zn


def test_mga_grid():

    assert MGA.E0 == 500000
    assert MGA.N0 == 10000000
    assert MGA.m0 == 0.9996
    assert MGA.zw == 6
    assert MGA.cm1 == -177
    assert MGA.get_zone(-177) == 1

    cm_mga_zone = {
        49: 111,
        50: 117,
        51: 123,
        52: 129,
        53: 135,
        54: 141,
        55: 147,
        56: 153,
    }
    for zn, cm in cm_mga_zone.items():
        assert MGA.get_cm(zn) == cm, "zn: {}, expected cm: {}".format(zn, cm)
        assert MGA.get_zone(cm) == zn

    assert MGA.z0_edge == -177 - 1.5 * 6


def test_vicgrid():

    assert VICGRID.E0 == 2500000
    assert VICGRID.N0 == 4500000

    assert VICGRID.φ1 == -36
    assert VICGRID.φ2 == -38

    assert VICGRID.λ0 == 145
    assert VICGRID.φ0 == -37

    assert VICGRID.constants == (-36, -38, 145, -37, 2500000, 4500000)


def test_vicgrid94():

    assert VICGRID94.E0 == 2500000
    assert VICGRID94.N0 == 2500000

    assert VICGRID94.φ1 == -36
    assert VICGRID94.φ2 == -38

    assert VICGRID94.λ0 == 145
    assert VICGRID94.φ0 == -37

    assert VICGRID94.constants == (-36, -38, 145, -37, 2500000, 2500000)
