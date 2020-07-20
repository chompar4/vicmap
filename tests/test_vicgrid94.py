import pytest
from vicgrid import geographic_to_vicgrid94
from utils import dms_to_dd
from datums import GDA94, AGD66

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

    e, n = geographic_to_vicgrid94(lat, lng)
    diff = abs(e - E)
    assert diff <= TOL


@pytest.mark.parametrize("lat,lng,E,N", known_vals_gda94)
def test_known_vals_94_northing(lat, lng, E, N):

    e, n = geographic_to_vicgrid94(lat, lng)
    diff = abs(n - N)
    assert diff <= TOL


@pytest.mark.parametrize("lat,lng,E,N", known_vals_gda94)
def test_known_vals_94_total(lat, lng, E, N):

    """ cartesian local approximation """

    e, n = geographic_to_vicgrid94(lat, lng)
    diff = math.sqrt((e - E) ** 2 + (n - N) ** 2)
    assert diff <= TOL
