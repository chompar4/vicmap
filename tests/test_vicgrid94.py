import pytest
from vicgrid import geo_to_vicgrid94
from utils import dms_to_dd
from geodesy.datums import GDA94, AGD66, GDA20
from geodesy.points import GeoPoint, PlanePoint
from geodesy.grids import MGA

import math

"""
The points chosen here have been a part of the state geodetic network adjustment
from AGD66 to GDA94 and are the official values as recorded in the Survey Marks
Enquiry Service – SMES (21/11/00). We reproduce these values to the nearest meter.
"""

known_vals_gda94 = [
    (-37, 145, 2500000, 2500000),  # true origin
    (dms_to_dd(-34, 29, 41.377), dms_to_dd(141, 59, 19.5899), 2223259.175, 2773628.391),
    (dms_to_dd(-38, 3, 53.8007), dms_to_dd(141, 24, 57.2580), 2185545.806, 2375895.467),
    (
        dms_to_dd(-37, 23, 39.6610),
        dms_to_dd(148, 46, 43.1871),
        2834469.388,
        2449602.655,
    ),
    (
        dms_to_dd(-36, 00, 58.1475),
        dms_to_dd(145, 59, 58.4589),
        2590104.617,
        2608691.847,
    ),
    (dms_to_dd(-38, 7, 47.3418), dms_to_dd(145, 9, 47.6172), 2514311.897, 2374602.216),
]

TOL = 1e0


@pytest.mark.parametrize("lat,lng,E,N", known_vals_gda94)
def test_known_vals_94_easting(lat, lng, E, N):

    pt = GeoPoint(lat, lng, datum=GDA94)
    pt_vic94 = geo_to_vicgrid94(pt)
    diff = abs(pt_vic94.E - E)
    assert diff <= TOL


@pytest.mark.parametrize("lat,lng,E,N", known_vals_gda94)
def test_known_vals_94_northing(lat, lng, E, N):

    pt = GeoPoint(lat, lng, datum=GDA94)
    pt_vic94 = geo_to_vicgrid94(pt)
    diff = abs(pt_vic94.N - N)
    assert diff <= TOL


@pytest.mark.parametrize("lat,lng,E,N", known_vals_gda94)
def test_known_vals_94_total(lat, lng, E, N):

    """ cartesian local approximation """

    pt = GeoPoint(lat, lng, datum=GDA94)
    pt_vic94 = geo_to_vicgrid94(pt)
    diff = math.sqrt((pt_vic94.E - E) ** 2 + (pt_vic94.N - N) ** 2)
    assert diff <= TOL


def test_geo_to_vicgrid_non_GDA94_datum():

    lat = -23
    lng = 145

    pt1 = GeoPoint(lat, lng, datum=GDA20)
    pt2 = GeoPoint(lat, lng, datum=GDA94)
    pt3 = GeoPoint(lat, lng, datum=AGD66)

    geo_to_vicgrid94(pt2)

    with pytest.raises(AssertionError) as e_info:
        geo_to_vicgrid94(pt3)

    with pytest.raises(AssertionError) as e_info:
        geo_to_vicgrid94(pt1)


def test_geo_to_mga_non_geopoint():

    lat = -23
    lng = 145
    pt = PlanePoint(lat, lng, grid=MGA)
    with pytest.raises(AssertionError) as e_info:
        geo_to_vicgrid94(pt)
