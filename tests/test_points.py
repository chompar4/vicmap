import pytest
from vicmap.utils import dms_to_dd
from vicmap.datums import GDA94, AGD66, GDA20
from vicmap.points import GeoPoint, PlanePoint, VICPoint, MGAPoint, MGRSPoint
from vicmap.grids import MGA94, MGA20, VICGRID94, VICGRID, MGAGrid, MGRS

import math


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
    zn = 54
    sf = 100000

    for n in range(57, 62):
        mga_pt = MGAPoint(54, 500000, n * sf, grid=MGA20)
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
        pt = MGAPoint(zone=zn, E=e, N=n, grid=MGA20)
        assert abs(pt.grid_convergence - γ) < 1e-3


def test_grid_convergence_zone_invariance_mga():
    for _, e, n, _ in known_convergence_mga:
        pt54 = MGAPoint(zone=54, E=e, N=n, grid=MGA20)
        pt55 = MGAPoint(zone=55, E=e, N=n, grid=MGA20)
        assert abs(pt54.grid_convergence - pt55.grid_convergence) < 1e-3


def test_declination_mga():
    sf = 100000
    west_pt = MGAPoint(54, 600000, 6200000, grid=MGA20)
    assert abs(west_pt.magnetic_declination - 9.350878790917436) < 1e3


def test_declination_mgrs():
    pt = MGRSPoint.from_mga(54, 5.04 * 1e5, 5.85 * 1e6)
    assert abs(pt.magnetic_declination - 9.813430953842529) < 1e-3


def test_from_6FIG_mgrs():

    pt = MGRSPoint.from_6FIG(55, "fu", "275882")
    pt2 = MGAPoint(55, 627500, 5888200, grid=MGA20)

    assert pt.E == pt2.E and pt.N == pt2.N


def test_transform_to_compatible_types():

    """
    Check we can transform between all types of points
    """

    pts = [
        GeoPoint(dLat=-37, dLng=145, datum=GDA20),
        GeoPoint(dLat=-37, dLng=145, datum=GDA94),
        VICPoint(E=VICGRID.E0, N=VICGRID.N0, grid=VICGRID),
        VICPoint(E=VICGRID94.E0, N=VICGRID94.N0, grid=VICGRID94),
        MGAPoint(zone=55, E=700000, N=6200000, grid=MGA94),
        MGAPoint(zone=55, E=700000, N=6200000, grid=MGA20),
        MGRSPoint.from_mga(zone=54, E=5.04 * 1e5, N=5.85 * 1e6),
    ]

    grids = [VICGRID, VICGRID94, MGA20, MGA94, MGRS]

    for pt in pts:
        for grid in grids:
            assert pt.transform_to(grid)


def test_transform_to_mgrs():

    o = GeoPoint(dLat=-37, dLng=145, datum=GDA94)
    assert o.transform_to(MGRS) == (55, "CV", "22038", "03258")


def test_known_vals_mgrs():

    pts = [
        (MGRSPoint.from_mga(54, 5.04 * 1e5, 5.85 * 1e6), (54, "WD", "04000", "50000"),),
        (MGRSPoint.from_mga(54, 6.5 * 1e5, 6.15 * 1e6), (54, "XG", "50000", "50000"),),
        (
            MGRSPoint.from_mga(55, 4.567 * 1e5, 6.1556 * 1e6),
            (55, "DB", "56700", "55600"),
        ),
        (
            MGRSPoint.from_mga(55, 6.78997 * 1e5, 5.8514 * 1e6),
            (55, "FU", "78997", "51400"),
        ),
    ]

    for pt, val in pts:

        assert pt.display_coords == val


def test_lower_left_mgrs():

    """
    Lower left corner of all mgrs grids should
    return origin
    """

    pts = [
        MGRSPoint.from_mga(54, cols[0], rows[0])
        for k, cols in MGRS.cols54.items()
        for k, rows in MGRS.rows54.items()
    ]
    for pt in pts:
        assert pt.x == "00000" and pt.y == "00000"

    pts = [
        MGRSPoint.from_mga(55, cols[0], rows[0])
        for k, cols in MGRS.cols55.items()
        for k, rows in MGRS.rows55.items()
    ]
    for pt in pts:
        assert pt.x == "00000" and pt.y == "00000"


def test_mgrs_precision():

    p1 = MGRSPoint.from_mga(54, 7e5, 6.2e6, precision=5)
    assert p1.x == "00000"
    assert p1.x == "00000"

    p1 = MGRSPoint.from_mga(54, 7e5, 6.2e6, precision=4)
    assert p1.x == "0000"
    assert p1.x == "0000"

    p1 = MGRSPoint.from_mga(54, 7e5, 6.2e6, precision=3)
    assert p1.x == "000"
    assert p1.x == "000"

    p1 = MGRSPoint.from_mga(54, 7e5, 6.2e6, precision=2)
    assert p1.x == "00"
    assert p1.x == "00"

    p1 = MGRSPoint.from_mga(54, 7e5, 6.2e6, precision=1)
    assert p1.x == "0"
    assert p1.x == "0"


def test__eq__vic():

    p1 = VICPoint(E=2.2e6, N=4.2e6, grid=VICGRID)
    p2 = VICPoint(E=2.2e6, N=4.2e6, grid=VICGRID)

    assert p1 == p2


def test__eq__mga():

    p1 = MGAPoint(zone=55, E=250000, N=5600000, grid=MGA94)
    p2 = MGAPoint(zone=55, E=250000, N=5600000, grid=MGA94)

    assert p1 == p2


def test__eq__mgrs():

    p1 = MGRSPoint(zone=55, usi="FU", x=30, y=20)
    p2 = MGRSPoint(zone=55, usi="FU", x=30, y=20)

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
        MGAPoint(zone=55, E=800000, N=6300000, grid=MGA94),
        MGAPoint(zone=55, E=800000, N=6300000, grid=MGA20),
        MGRSPoint.from_mga(54, 5.04 * 1e5, 5.85 * 1e6),
    ]

    for pt in pts:
        assert pt.magnetic_declination
        assert f"{pt.grid_convergence}"
        assert pt.grid_magnetic_angle


def test_repr__():

    pts = [
        (GeoPoint(dLat=-37, dLng=145, datum=GDA20), f"<GeoPt_(-37,145)_GDA20>"),
        (GeoPoint(dLat=-37, dLng=145, datum=GDA94), f"<GeoPt_(-37,145)_GDA94>"),
        (
            VICPoint(E=VICGRID.E0, N=VICGRID.N0, grid=VICGRID),
            f"<VicPt_(2500000,4500000)_VICGRID>",
        ),
        (
            VICPoint(E=VICGRID94.E0, N=VICGRID94.N0, grid=VICGRID94),
            f"<VicPt_(2500000,2500000)_VICGRID94>",
        ),
        (
            MGAPoint(zone=55, E=800000, N=6300000, grid=MGA94),
            f"<MGAPt_(800000,6300000)_MGA94>",
        ),
        (
            MGAPoint(zone=55, E=800000, N=6300000, grid=MGA20),
            f"<MGAPt_(800000,6300000)_MGA20>",
        ),
        (
            MGRSPoint.from_mga(54, 5.04 * 1e5, 5.85 * 1e6),
            f"<MGRSPt_(54, WD, 04000, 50000)_MGRS>",
        ),
        (
            MGRSPoint(54, "WD", 4000, 50000, precision=5),
            f"<MGRSPt_(54, WD, 04000, 50000)_MGRS>",
        ),
    ]

    for pt, rep in pts:
        assert pt.__repr__() == rep
