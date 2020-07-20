import pytest
from mga import geo_to_mga
from utils import dms_to_dd
from datums import GDA20, GDA94


def test_geo_to_mga():

    lat = dms_to_dd(-23, 40, 12.446020)
    lng = dms_to_dd(133, 53, 7.84784)
    z, E, N, m, γ = geo_to_mga(lat, lng)

    assert z == 53
    assert round(E, 2) == round(386352.397753, 2)
    assert round(N, 2) == round(7381850.768886, 2)
    assert round(m, 9) == 0.999759539
    assert round(γ, 9) == -0.447481418


def test_geo_to_mga_94_20_invariance():

    lat = dms_to_dd(-23, 40, 12.446020)
    lng = dms_to_dd(133, 53, 7.84784)

    z20, E20, N20, m20, γ20 = geo_to_mga(lat, lng, datum=GDA20)
    z94, E94, N94, m94, γ94 = geo_to_mga(lat, lng, datum=GDA94)

    assert (z20, E20, N20, m20, γ20) == (z94, E94, N94, m94, γ94)

