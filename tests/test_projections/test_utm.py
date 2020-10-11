import pytest
from vicmap.datums import AGD66, GDA20, GDA94
from vicmap.grids import MGA20, MGA94
from vicmap.points import GeoPoint, PlanePoint
from vicmap.projections import utm
from vicmap.utils import dms_to_dd

"""
UNIVERSAL TRANSVERSE MERCATOR TESTS
"""


def test_utm_known_vals():

    for grid in [MGA94, MGA20]:

        lat = dms_to_dd(-23, 40, 12.446020)
        lng = dms_to_dd(133, 53, 7.84784)

        z, E, N, _, _ = utm(lat, lng, ellipsoid=GDA20.ellipsoid, grid=grid)

        assert z == 53
        assert abs(E - 386352.397753) < 1e-6
        assert abs(N - 7381850.768886) < 1e-6


def test_utm_grid_convergence():

    for grid in [MGA94, MGA20]:

        lat = dms_to_dd(-23, 40, 12.446020)
        lng = dms_to_dd(133, 53, 7.84784)

        _, _, _, _, γ = utm(lat, lng, ellipsoid=GDA20.ellipsoid, grid=grid)

        assert abs(γ + 0.447481418) < 1e-8


def test_utm_point_scale_factor():

    for grid in [MGA94, MGA20]:

        lat = dms_to_dd(-23, 40, 12.446020)
        lng = dms_to_dd(133, 53, 7.84784)

        _, _, _, m, _ = utm(lat, lng, ellipsoid=GDA20.ellipsoid, grid=grid)

        assert abs(m - 0.999759539) < 1e-8


def test_mga_datum_invariance():
    """
    same coordinates in different datums should be invariant if
    ellipsoidal constants are the same
    """

    lat = dms_to_dd(-23, 40, 12.446020)
    lng = dms_to_dd(133, 53, 7.84784)

    z1, E1, N1, m1, γ1 = utm(lat, lng, ellipsoid=GDA20.ellipsoid, grid=MGA20)
    z2, E2, N2, m2, γ2 = utm(lat, lng, ellipsoid=GDA94.ellipsoid, grid=MGA94)

    assert (z1, E1, N1, m1, γ1) == (z2, E2, N2, m2, γ2)
