import pytest
from vicgrid import geo_to_vicgrid
from utils import dms_to_dd
from geodesy.datums import GDA94, AGD66, GDA20
from geodesy.points import GeoPoint, PlanePoint, VICPoint
from geodesy.grids import MGA, VICGRID94, VICGRID

import math

"""
The points chosen here have been a part of the state geodetic network adjustment
from AGD66 to GDA94 and are the official values as recorded in the Survey Marks
Enquiry Service – SMES (21/11/00). We reproduce these values to the nearest meter.
"""

known_vals_agd66 = [
    (-37, 145, 2500000, 4500000),  # true origin
    (
        dms_to_dd(-34, 29, 46.7724),
        dms_to_dd(141, 59, 14.8833),
        2223143.321,
        4773459.258,
    ),
    (dms_to_dd(-38, 3, 59.0913), dms_to_dd(141, 24, 52.3647), 2185431.606, 4375727.525),
    (
        dms_to_dd(-37, 23, 45.2184),
        dms_to_dd(148, 46, 38.6881),
        2834353.246,
        4449435.092,
    ),
    (dms_to_dd(-36, 1, 03.6403), dms_to_dd(145, 59, 53.8910), 2589988.794, 4608524.140),
    (dms_to_dd(-38, 7, 52.7666), dms_to_dd(145, 9, 42.9142), 2514197.138, 4374434.703),
]

TOL = 1e0


@pytest.mark.parametrize("lat,lng,E,N", known_vals_agd66)
def test_known_vals_easting(lat, lng, E, N):

    pt = GeoPoint(lat, lng, datum=AGD66)
    vic_pt = geo_to_vicgrid(pt)
    diff = abs(vic_pt.E - E)
    assert diff <= TOL


@pytest.mark.parametrize("lat,lng,E,N", known_vals_agd66)
def test_known_vals_northing(lat, lng, E, N):

    pt = GeoPoint(lat, lng, datum=AGD66)
    vic_pt = geo_to_vicgrid(pt)
    diff = abs(vic_pt.N - N)
    assert diff <= TOL


@pytest.mark.parametrize("lat,lng,E,N", known_vals_agd66)
def test_known_vals_total(lat, lng, E, N):

    """ cartesian local approximation """

    pt = GeoPoint(lat, lng, datum=AGD66)
    vic_pt = geo_to_vicgrid(pt)
    diff = math.sqrt((vic_pt.E - E) ** 2 + (vic_pt.N - N) ** 2)
    assert diff <= TOL


def test_geo_to_vicgrid_non_GDA_datum():

    lat = -23
    lng = 145

    pt1 = GeoPoint(lat, lng, datum=GDA20)
    pt2 = GeoPoint(lat, lng, datum=GDA94)
    pt3 = GeoPoint(lat, lng, datum=AGD66)

    geo_to_vicgrid(pt3)

    with pytest.raises(AssertionError) as e_info:
        geo_to_vicgrid(pt2)

    with pytest.raises(AssertionError) as e_info:
        geo_to_vicgrid(pt1)


def test_geo_to_mga_non_geopoint():

    lat = -23
    lng = 145
    pt = PlanePoint(lat, lng, grid=MGA)
    with pytest.raises(AssertionError) as e_info:
        geo_to_vicgrid(pt)


def test_grid_convergence_central_meridian_vicpoint():
    """
    Convergence along central meridian of vicgrid should 
    equal 0
    """
    sf = 100000
    delta = 20
    for n in range(23, 28):
        E = 25
        grid_pt = VICPoint(E * sf, n * sf, grid=VICGRID94)
        assert grid_pt.grid_convergence == 0

        grid_pt = VICPoint(E * sf, (n + delta) * sf, grid=VICGRID)
        # import ipdb

        # ipdb.set_trace()
        assert grid_pt.grid_convergence == 0

