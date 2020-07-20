import pytest
from mga import geo_to_mga, get_zone
from projections import utm
from utils import dms_to_dd
import numpy as np
from datums import GDA20, GDA94


def test_geo_to_mga():

    lat = dms_to_dd(-23, 40, 12.446020)
    lng = dms_to_dd(133, 53, 7.84784)
    z, E, N = geo_to_mga(lat, lng)

    assert z == 53
    assert round(E, 2) == round(386352.397753, 2)
    assert round(N, 2) == round(7381850.768886, 2)

    cm = 135
    m0 = 0.9996
    E0 = 500000
    N0 = 10000000
    datum = GDA20
    _, _, m, γ = utm(lat, lng, cm, m0, E0, N0, datum.ellipsoid)

    assert round(m, 9) == 0.999759539
    assert round(γ, 9) == -0.447481418


def test_geo_to_mga_94_20_invariance():
    """
    same coordinates in different datums should be invariant if 
    ellipsoidal constants are the same
    """

    lat = dms_to_dd(-23, 40, 12.446020)
    lng = dms_to_dd(133, 53, 7.84784)

    z20, E20, N20 = geo_to_mga(lat, lng, datum=GDA20)
    z94, E94, N94 = geo_to_mga(lat, lng, datum=GDA94)

    assert (z20, E20, N20) == (z94, E94, N94)


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
    for lng in np.linspace(start=west, stop=east, num=10):
        if lng == east:
            assert get_zone(lng) == zn + 1  # range of zones = [west, east)
        else:
            assert get_zone(lng) == zn
