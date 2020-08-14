import pytest
from mga import geo_to_mga
from geodesy.points import GeoPoint, PlanePoint
from projections import utm
from utils import dms_to_dd
import numpy as np
from geodesy.datums import GDA20, GDA94, AGD66
from geodesy.grids import MGA20, MGA94


def test_geo_to_mga():

    for grid in [MGA94, MGA20]:

        lat = dms_to_dd(-23, 40, 12.446020)
        lng = dms_to_dd(133, 53, 7.84784)
        pt = GeoPoint(lat, lng, datum=GDA20)
        mga_pt = geo_to_mga(pt)

        assert mga_pt.zone == 53
        assert abs(mga_pt.E - 386352.397753) < 1e-6
        assert abs(mga_pt.N - 7381850.768886) < 1e-6

        cm = 135
        m0 = 0.9996
        E0 = 500000
        N0 = 10000000
        datum = GDA20
        _, _, m, γ = utm(lat, lng, ellipsoid=datum.ellipsoid, grid=grid)

        assert abs(m - 0.999759539) < 1e-8
        assert abs(γ + 0.447481418) < 1e-8


def test_geo_to_mga_non_GDA_datum():

    lat = -23
    lng = 145

    pt1 = GeoPoint(lat, lng, datum=GDA20)
    pt2 = GeoPoint(lat, lng, datum=GDA94)
    pt3 = GeoPoint(lat, lng, datum=AGD66)

    geo_to_mga(pt1)
    geo_to_mga(pt2)

    with pytest.raises(AssertionError) as e_info:
        geo_to_mga(pt3)


def test_geo_to_mga_non_geopoint():

    for grid in [MGA94, MGA20]:
        lat = -23
        lng = 145
        pt = PlanePoint(lat, lng, grid=grid)
        with pytest.raises(AssertionError) as e_info:
            geo_to_mga(pt)


def test_geo_to_mga_94_20_invariance():
    """
    same coordinates in different datums should be invariant if 
    ellipsoidal constants are the same
    """

    lat = dms_to_dd(-23, 40, 12.446020)
    lng = dms_to_dd(133, 53, 7.84784)

    pt1 = GeoPoint(lat, lng, datum=GDA20)
    pt2 = GeoPoint(lat, lng, datum=GDA94)

    mga_pt1 = geo_to_mga(pt1)
    mga_pt2 = geo_to_mga(pt2)

    assert mga_pt1.coords == mga_pt2.coords
