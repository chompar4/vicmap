import pytest
from mga import geographic_to_mga
from utils import dms_to_dd


def test_geographic_to_mga():

    lat = dms_to_dd(-23, 40, 12.446020)
    lng = dms_to_dd(133, 53, 7.84784)
    z, E, N, m, γ = geographic_to_mga(lat, lng)

    assert z == 53
    assert round(E, 2) == round(386352.397753, 2)
    assert round(N, 2) == round(7381850.768886, 2)
    assert round(m, 9) == 0.999759539
    assert round(γ, 9) == -0.447481418
