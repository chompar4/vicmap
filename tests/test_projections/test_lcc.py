import pytest
from vicmap.utils import dms_to_dd
from vicmap.datums import GDA94, AGD66, GDA20
from vicmap.points import GeoPoint, PlanePoint
from vicmap.grids import MGA94, MGA20, VICGRID94, VICGRID
from vicmap.projections import lambert_conformal_conic as lcc

import math

"""
LAMBERT CONFORMAL CONIC TESTS
"""

"""
VICGRID94 KNOWN VALUES
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
def test_known_vals_vic94_easting(lat, lng, E, N):

    e, _, _, _ = lcc(lat, lng, GDA94.ellipsoid, VICGRID94)
    assert abs(e - E) <= TOL


@pytest.mark.parametrize("lat,lng,E,N", known_vals_gda94)
def test_known_vals_vic94_northing(lat, lng, E, N):

    _, n, _, _ = lcc(lat, lng, GDA94.ellipsoid, VICGRID94)
    assert abs(n - N) <= TOL


@pytest.mark.parametrize("lat,lng,E,N", known_vals_gda94)
def test_known_vals_vic94_total(lat, lng, E, N):

    e, n, _, _ = lcc(lat, lng, GDA94.ellipsoid, VICGRID94)
    assert math.sqrt((e - E) ** 2 + (n - N) ** 2) <= TOL


"""
VICGRID KNOWN VALUES
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


@pytest.mark.parametrize("lat,lng,E,N", known_vals_agd66)
def test_known_vals_vic_easting(lat, lng, E, N):

    e, _, _, _ = lcc(lat, lng, AGD66.ellipsoid, VICGRID)
    assert abs(e - E) <= TOL


@pytest.mark.parametrize("lat,lng,E,N", known_vals_agd66)
def test_known_vals_vic_northing(lat, lng, E, N):

    _, n, _, _ = lcc(lat, lng, AGD66.ellipsoid, VICGRID)
    assert abs(n - N) <= TOL


@pytest.mark.parametrize("lat,lng,E,N", known_vals_agd66)
def test_known_vals_vic_total(lat, lng, E, N):

    e, n, _, _ = lcc(lat, lng, AGD66.ellipsoid, VICGRID)
    assert math.sqrt((e - E) ** 2 + (n - N) ** 2) <= TOL
