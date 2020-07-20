import pytest
from mga import geo_to_mga
from geodesy.points import GeoPoint, PlanePoint
from projections import utm
from utils import dms_to_dd
import numpy as np
from geodesy.datums import GDA20, GDA94, AGD66
from geodesy.grids import MGA


def test_geo_to_mga():

    lat = dms_to_dd(-23, 40, 12.446020)
    lng = dms_to_dd(133, 53, 7.84784)
    pt = GeoPoint(lat, lng, datum=GDA20)
    mga_pt = geo_to_mga(pt)

    assert mga_pt.zone == 53
    assert round(mga_pt.E, 2) == round(386352.397753, 2)
    assert round(mga_pt.N, 2) == round(7381850.768886, 2)

    cm = 135
    m0 = 0.9996
    E0 = 500000
    N0 = 10000000
    datum = GDA20
    _, _, m, γ = utm(lat, lng, ellipsoid=datum.ellipsoid, grid=MGA)

    assert round(m, 9) == 0.999759539
    assert round(γ, 9) == -0.447481418


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

    lat = -23
    lng = 145
    pt = PlanePoint(lat, lng, grid=MGA)
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
