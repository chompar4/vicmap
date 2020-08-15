import pytest
from geodesy.utils import dms_to_dd
from geodesy.datums import GDA94, AGD66, GDA20
from geodesy.points import GeoPoint, PlanePoint, VICPoint, MGAPoint
from geodesy.grids import MGA94, MGA20, VICGRID94, VICGRID, MGAGrid

import math


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
        assert grid_pt.grid_convergence == 0


def test_grid_convergence_signs_vicpoint():
    sf = 100000
    west_pt = VICPoint(23 * sf, 26 * sf, grid=VICGRID94)
    assert west_pt.grid_convergence < 0

    east_pt = VICPoint(26 * sf, 26 * sf, grid=VICGRID94)
    assert east_pt.grid_convergence > 0
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

    for pt in pts:
        assert pt.transform_to(VICGRID)
        assert pt.transform_to(VICGRID94)
        assert pt.transform_to(MGA20)
        assert pt.transform_to(MGA94)
