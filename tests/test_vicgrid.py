import pytest
from vicgrid import geographic_to_vicgrid
from utils import dms_to_dd
from datums import GDA94, AGD66

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

    e, n = geographic_to_vicgrid(lat, lng)
    diff = abs(e - E)
    assert diff <= TOL


@pytest.mark.parametrize("lat,lng,E,N", known_vals_agd66)
def test_known_vals_northing(lat, lng, E, N):

    e, n = geographic_to_vicgrid(lat, lng)
    diff = abs(n - N)
    assert diff <= TOL


@pytest.mark.parametrize("lat,lng,E,N", known_vals_agd66)
def test_known_vals_total(lat, lng, E, N):

    """ cartesian local approximation """

    e, n = geographic_to_vicgrid(lat, lng)
    diff = math.sqrt((e - E) ** 2 + (n - N) ** 2)
    assert diff <= TOL
