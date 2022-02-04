import math
from datetime import date

import geomag
import pytest
from mock import patch
from vicmap.datums import AGD66, GDA20, GDA94, __all_datums__
from vicmap.grids import MGA20, MGA94, MGRS, VICGRID, VICGRID94, __all_grids__
from vicmap.points import GeoPoint, MGAPoint, MGRSPoint, VICPoint


def test_grid_convergence_central_meridian_vicgrid():
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
        assert grid_pt.grid_convergence == 0


def test_grid_convergence_signs_vicgrid():
    sf = 100000
    west_pt = VICPoint(23 * sf, 26 * sf, grid=VICGRID94)
    assert west_pt.grid_convergence < 0

    east_pt = VICPoint(26 * sf, 26 * sf, grid=VICGRID94)
    assert east_pt.grid_convergence > 0


def test_declination_vicgrid():
    sf = 100000
    west_pt = VICPoint(23 * sf, 26 * sf, grid=VICGRID94)
    assert west_pt.magnetic_declination


def test_grid_convergence_central_meridian_mga():
    """
    Convergence along central meridian of mga zones should
    equal 0
    """
    sf = 100000

    for n in range(57, 62):
        mga_pt = MGAPoint(54, 'H', 500000, n * sf, grid=MGA20)
        assert mga_pt.grid_convergence < 1e-5


known_convergence_mga = [
    (54, 600000, 6200000, 0.613256375),
    (54, 700000, 6200000, 1.226072822),
    (54, 700000, 5700000, 1.444944199),
    (55, 300000, 6100000, -1.267879176),
    (55, 400000, 5700000, -0.722763509),
]


def test_grid_convergence_known_vals_mga():
    for zn, e, n, γ in known_convergence_mga:
        pt = MGAPoint(zone=zn, lat_band='H', E=e, N=n, grid=MGA20)
        assert abs(pt.grid_convergence - γ) < 1e-3


def test_grid_convergence_zone_invariance_mga():
    for _, e, n, _ in known_convergence_mga:
        pt54 = MGAPoint(zone=54, lat_band='H', E=e, N=n, grid=MGA20)
        pt55 = MGAPoint(zone=55, lat_band='H', E=e, N=n, grid=MGA20)
        assert abs(pt54.grid_convergence - pt55.grid_convergence) < 1e-3


def test_declination_mga():
    west_pt = MGAPoint(54, 'H', 600000, 6200000, grid=MGA20)
    assert abs(west_pt.magnetic_declination - 9.350878790917436) < 1e3


def test_from_6FIG_mgrs():

    pt = MGRSPoint.from_6FIG(55, 'H', "fu", "275882")
    pt2 = MGAPoint(55, 'H', 627500, 5888200, grid=MGA20)

    assert pt.E == pt2.E and pt.N == pt2.N


def test_from_brennan():

    """
    Can use either map number or map name
    """

    known_vals = [
        ('991885', '7339', 29.027865, 142.017699), 
        ('991885', 'Tibooburra', 29.027865, 142.017699),
        ('452278', 'Mount Morgan', -33.15865, 150.26792),  # pipeline canyon
        ('452278', '8931-1S', -33.15865, 150.26792),  # pipeline canyon
        ('491177', 'Rock Hill', -33.25056, 150.30691),  # galah canyon
        ('491177', '8931-2N', -33.25056, 150.30691),  # galah canyon
        ('537885', 'Mount Wilson', -33.51472, 150.34826),  # mt wilson saddle
        ('537885', '8930-1N', -33.51472, 150.34826),  # mt wilson saddle
    ]

    for g6, mapp, eLat, eLng in known_vals:
        pt = MGAPoint.from_brennan(GR6=g6, map=mapp)
        dLat, dLng = pt.transform_to(pt.grid.datum)
        assert abs(dLat - eLat) <= 1e6
        assert abs(dLng - eLng) <= 1e6


def test_transform_to_compatible_types():

    """
    Check we can transform between all types of points
    """

    pts = [
        GeoPoint(dLat=-37, dLng=145, datum=GDA20),
        GeoPoint(dLat=-37, dLng=145, datum=GDA94),
        VICPoint(E=VICGRID.E0, N=VICGRID.N0, grid=VICGRID),
        VICPoint(E=VICGRID94.E0, N=VICGRID94.N0, grid=VICGRID94),
        MGAPoint(zone=55, lat_band='H', E=700000, N=6200000, grid=MGA94),
        MGAPoint(zone=55, lat_band='H', E=700000, N=6200000, grid=MGA20),
        MGRSPoint.from_mga(zone=54, lat_band='H', E=5.04 * 1e5, N=5.85 * 1e6),
    ]

    for pt in pts:
        for other in __all_grids__ + __all_datums__:
            try:
                pt.transform_to(other)
            except:
                assert False, f'{pt} -> {other}'


def test_transform_to_mgrs():

    o = GeoPoint(dLat=-37, dLng=145, datum=GDA94)
    assert o.transform_to(MGRS) == (55, "H", "CV", "22038", "03258")


def test_known_vals_mgrs():

    pts = [
        (MGRSPoint.from_mga(54, "K", 5.04 * 1e5, 5.85 * 1e6), (54, "K", "WD", "04000", "50000")),
        (MGRSPoint.from_mga(54, "H", 6.5 * 1e5, 6.15 * 1e6), (54, "H", "XG", "50000", "50000")),
        (
            MGRSPoint.from_mga(55, "K", 4.567 * 1e5, 6.1556 * 1e6),
            (55, "K", "DB", "56700", "55600"),
        ),
        (
            MGRSPoint.from_mga(55, "K", 6.78997 * 1e5, 5.8514 * 1e6),
            (55, "K", "FU", "78997", "51400"),
        ),
    ]

    for pt, val in pts:

        assert pt.display_coords == val


def test_bounds():

    top_left = MGRSPoint.from_mga(54, 'J', 486103, 6666177)
    top_right = MGRSPoint.from_mga(54, 'H', 489461, 5644232)

    assert all([top_left, top_right])


def test_lower_left_mgrs():

    """
    Lower left corner of all mgrs grids should
    have 6 figure GR 000000
    """

    for zone in [54, 55, 56]:
        for lat_band in ['H', 'J', 'K']:

            for col in getattr(MGRS, f'cols{zone}').values():
                for row in MGRS.getrows(zone).values():

                    pt = MGRSPoint.from_mga(zone, lat_band, col[0], row[0])
                    assert pt.x == "00000" and pt.y == "00000"


def test_mgrs_precision():

    p1 = MGRSPoint.from_mga(54, 'H', 7e5, 6.2e6, precision=5)
    assert p1.x == "00000"
    assert p1.x == "00000"

    p1 = MGRSPoint.from_mga(54, 'H', 7e5, 6.2e6, precision=4)
    assert p1.x == "0000"
    assert p1.x == "0000"

    p1 = MGRSPoint.from_mga(54, 'H', 7e5, 6.2e6, precision=3)
    assert p1.x == "000"
    assert p1.x == "000"

    p1 = MGRSPoint.from_mga(54, 'H', 7e5, 6.2e6, precision=2)
    assert p1.x == "00"
    assert p1.x == "00"

    p1 = MGRSPoint.from_mga(54, 'H', 7e5, 6.2e6, precision=1)
    assert p1.x == "0"
    assert p1.x == "0"


def test__eq__vic():

    p1 = VICPoint(E=2.2e6, N=4.2e6, grid=VICGRID)
    p2 = VICPoint(E=2.2e6, N=4.2e6, grid=VICGRID)

    assert p1 == p2


def test__eq__mga():

    p1 = MGAPoint(zone=55, lat_band='H', E=250000, N=5600000, grid=MGA94)
    p2 = MGAPoint(zone=55, lat_band='H', E=250000, N=5600000, grid=MGA94)

    assert p1 == p2


def test__eq__mgrs():

    p1 = MGRSPoint(zone=55, lat_band='H', usi="FU", x=30, y=20)
    p2 = MGRSPoint(zone=55, lat_band='H', usi="FU", x=30, y=20)

    assert p1 == p2


def test__eq__geo():
    p1 = GeoPoint(40, 50)
    p2 = GeoPoint(40, 50)

    assert p1 == p2


def test_magnetic_functions():

    """
    Check we can call all declination functions
    """

    pts = [
        GeoPoint(dLat=-37, dLng=145, datum=GDA20),
        GeoPoint(dLat=-37, dLng=145, datum=GDA94),
        VICPoint(E=VICGRID.E0, N=VICGRID.N0, grid=VICGRID),
        VICPoint(E=VICGRID94.E0, N=VICGRID94.N0, grid=VICGRID94),
        MGAPoint(zone=55, lat_band='H', E=800000, N=6300000, grid=MGA94),
        MGAPoint(zone=55, lat_band='H', E=800000, N=6300000, grid=MGA20),
        MGRSPoint.from_mga(54, 'H', 5.04 * 1e5, 5.85 * 1e6),
    ]

    for pt in pts:
        assert pt.magnetic_declination
        assert f"{pt.grid_convergence}"
        assert pt.grid_magnetic_angle


def test_repr__():

    pts = [
        (GeoPoint(dLat=-37, dLng=145, datum=GDA20), "<GeoPt_(-37,145)_GDA20>"),
        (GeoPoint(dLat=-37, dLng=145, datum=GDA94), "<GeoPt_(-37,145)_GDA94>"),
        (
            VICPoint(E=VICGRID.E0, N=VICGRID.N0, grid=VICGRID),
            "<VicPt_(2500000,4500000)_VICGRID>",
        ),
        (
            VICPoint(E=VICGRID94.E0, N=VICGRID94.N0, grid=VICGRID94),
            "<VicPt_(2500000,2500000)_VICGRID94>",
        ),
        (
            MGAPoint(zone=55, lat_band='H', E=800000, N=6300000, grid=MGA94),
            "<MGAPt_(800000,6300000)_MGA94>",
        ),
        (
            MGAPoint(zone=55, lat_band='H', E=800000, N=6300000, grid=MGA20),
            "<MGAPt_(800000,6300000)_MGA20>",
        ),
        (
            MGRSPoint.from_mga(54, 'K', 5.04 * 1e5, 5.85 * 1e6),
            "<MGRSPt_(54, K, WD, 04000, 50000)_MGRS>",
        ),
        (
            MGRSPoint(54, 'H', "WD", 4000, 50000, precision=5),
            "<MGRSPt_(54, H, WD, 04000, 50000)_MGRS>",
        ),
    ]

    for pt, rep in pts:
        assert pt.__repr__() == rep


def test_distance_to_geo_known_vals():

    known = [
        (-37.95103342, 144.4248679, -37.65282114, 143.9264955, 54972.274),
        (-37.85103342, 144.3248679, -37.75282114, 143.8264955, 45224.112),
        (-37.75103342, 144.2248679, -37.85282114, 143.7264955, 45321.404),
        (-37.65103342, 144.1248679, -37.95282114, 143.6264955, 55212.127),
        (-37.55103342, 144.0248679, -38.05282114, 143.5264955, 70910.283),
        (-37.45103342, 143.9248679, -38.15282114, 143.4264955, 89407.481),
        (-37.35103342, 143.8248679, -38.25282114, 143.3264955, 109291.662),
        (-37.25103342, 143.7248679, -38.35282114, 143.2264955, 129927.587),
        (-37.15103342, 143.6248679, -38.45282114, 143.1264955, 151007.381),
        (-37.05103342, 143.5248679, -38.55282114, 143.0264955, 172368.273),
        (-36.95103342, 143.4248679, -38.65282114, 142.9264955, 193917.394),
        (-36.85103342, 143.3248679, -38.75282114, 142.8264955, 215598.311),
        (-36.75103342, 143.2248679, -38.85282114, 142.7264955, 237374.916),
    ]

    for φ1, λ1, φ2, λ2, D in known:
        p1 = GeoPoint(dLat=φ1, dLng=λ1, datum=GDA20)
        p2 = GeoPoint(dLat=φ2, dLng=λ2, datum=GDA20)

        assert p1.distance_to(p2) - D < 1e0  # meters


def test_distance_to_same_point():

    p1 = GeoPoint(dLat=-37.95103342, dLng=144.4248679, datum=GDA20)
    p2 = GeoPoint(dLat=-37.95103342, dLng=144.4248679, datum=GDA94)

    assert p1.distance_to(p2) == 0


def test_distance_to_transform_geo_datum():
    for d1 in __all_datums__:
        for d2 in __all_datums__:
            p1 = GeoPoint(dLat=-37.95103342, dLng=144.4248679, datum=d1)
            p2 = GeoPoint(dLat=-37.65282114, dLng=143.9264955, datum=d2)

            assert p1.distance_to(p2)


def test_distance_to_euclidian_u1km():

    delta = 1000
    for i in range(5600000, 6300000, 1000):

        p1 = MGAPoint(zone=55, lat_band='H', E=700000, N=i, grid=MGA94)
        p2 = MGAPoint(zone=55, lat_band='H', E=700000, N=i + delta, grid=MGA94)

        assert p1.distance_to(p2) == delta


def test_distance_to_euclidian_v1km():

    delta = 1000
    for i in range(200000, 800000, 1000):

        p1 = MGAPoint(zone=55, lat_band='H', E=i, N=6300000, grid=MGA94)
        p2 = MGAPoint(zone=55, lat_band='H', E=i + delta, N=6300000, grid=MGA94)

        assert p1.distance_to(p2) == delta


def test_distance_to_euclidian_uv1km():

    delta = 1000
    for i in range(200000, 800000, 1000):

        p1 = MGAPoint(zone=55, lat_band='H', E=i, N=6200000, grid=MGA94)
        p2 = MGAPoint(zone=55, lat_band='H', E=i + delta, N=6201000, grid=MGA94)

        assert p1.distance_to(p2) - 1414.21356 < 1e-4


def test_distance_to_all_types():

    pts = [
        GeoPoint(dLat=-37, dLng=145, datum=GDA20),
        GeoPoint(dLat=-37, dLng=145, datum=GDA94),
        VICPoint(E=VICGRID.E0, N=VICGRID.N0, grid=VICGRID),
        VICPoint(E=VICGRID94.E0, N=VICGRID94.N0, grid=VICGRID94),
        MGAPoint(zone=55, lat_band='H', E=800000, N=6300000, grid=MGA94),
        MGAPoint(zone=55, lat_band='H', E=800000, N=6300000, grid=MGA20),
        MGRSPoint.from_mga(54, 'H', 5.04 * 1e5, 5.85 * 1e6),
        MGRSPoint(54, 'H', "WD", 4000, 50000, precision=5),
    ]

    for pt in pts:
        for other in pts:
            assert pt.distance_to(other) >= 0
