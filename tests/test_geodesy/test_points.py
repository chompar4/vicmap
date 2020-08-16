import pytest
from geodesy.utils import dms_to_dd
from geodesy.datums import GDA94, AGD66, GDA20
from geodesy.points import GeoPoint, PlanePoint, VICPoint, MGAPoint
from geodesy.grids import MGA94, MGA20, VICGRID94, VICGRID, MGAGrid

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


known_convergence_vic = [
    (23, 26, 0),
]


def test_grid_convergence_known_values_vicgrid():
    sf = 100000
    delta = 20

    for e, n, γ in known_convergence_vic:

        grid_pt = VICPoint(e * sf, n * sf, grid=VICGRID94)
        assert grid_pt.grid_convergence == 0

        grid_pt = VICPoint(e * sf, (n + delta) * sf, grid=VICGRID)
        assert grid_pt.grid_convergence == 0


def test_grid_convergence_signs_vicgrid():
    sf = 100000
    west_pt = VICPoint(23 * sf, 26 * sf, grid=VICGRID94)
    assert west_pt.grid_convergence < 0

    east_pt = VICPoint(26 * sf, 26 * sf, grid=VICGRID94)
    assert east_pt.grid_convergence > 0


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


known_convergence = [
    (54, 386352.39800000, 7381850.76900000, -0.447481417),
    (54, 600000, 6200000, 0.613256375),
    (54, 700000, 6200000, 1.226072822),
    (54, 700000, 5700000, 1.444944199),
    (55, 300000, 6100000, -1.267879176),
    (55, 400000, 5700000, -0.722763509),
]


def test_grid_convergence_known_vals_mga():
    for zn, e, n, γ in known_convergence:
        pt = MGAPoint(zone=zn, E=e, N=n, grid=MGA20)
        assert abs(pt.grid_convergence - γ) < 1e-3


def test_grid_convergence_zone_invariance_mga():
    for _, e, n, _ in known_convergence:
        pt54 = MGAPoint(zone=54, E=e, N=n, grid=MGA20)
        pt55 = MGAPoint(zone=55, E=e, N=n, grid=MGA20)
        assert abs(pt54.grid_convergence - pt55.grid_convergence) < 1e-3


def test_transform_to_compatible_types():

    """
    Check we can transform between all types of points
    """

    pts = [
        GeoPoint(dLat=-37, dLng=145, datum=GDA20),
        GeoPoint(dLat=-37, dLng=145, datum=GDA94),
        VICPoint(E=VICGRID.E0, N=VICGRID.N0, grid=VICGRID),
        VICPoint(E=VICGRID94.E0, N=VICGRID94.N0, grid=VICGRID94),
        MGAPoint(zone=55, E=MGA94.E0, N=MGA94.N0, grid=MGA94),
        MGAPoint(zone=55, E=MGA20.E0, N=MGA20.N0, grid=MGA20),
    ]

    grids = [VICGRID, VICGRID94, MGA20, MGA94]

    for pt in pts:
        for grid in grids:
            assert pt.transform_to(grid)
