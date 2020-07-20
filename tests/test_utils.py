from utils import point_scale_factor, grid_convergence, get_zone, pq_coefficients, transverse_mercator, gauss_schreiber, conformal_latitude, rectifying_radius, krueger_coefficients

import pytest 
import numpy as np

from math import radians
from datums import WGS84

zones = [
    (108, 114, 49),
    (114, 120, 50),
    (120, 126, 51),
    (126, 132, 52),
    (132, 138, 53),
    (138, 144, 54),
    (144, 150, 55),
    (150, 156, 56),
]

@pytest.mark.parametrize("west,east,zn", zones)
def test_get_zone(west, east, zn):
    for lng in np.linspace(start=west, stop=east, num=10):
        if lng == east: 
            assert get_zone(lng) == zn + 1  # range of zones = [west, east) 
        else:
            assert get_zone(lng) == zn

def test_rectifying_radius():
    a = 6378137
    n = 1.679220395E-03
    assert round(rectifying_radius(a, n), 12) == 6367449.14576869

def test_krueger_coefficients():
    n = 1.679220395E-03
    α = krueger_coefficients(n)
    assert round(α[2], 12) == round(8.377318247286E-04, 12), 'a2: {}'.format(round(α[2], 12))
    assert round(α[4], 15) == round(7.608527848150E-07, 15), 'a4: {}'.format(round(α[4], 15))
    assert round(α[6], 17) == round(1.197645520855E-09, 17), 'a6: {}'.format(round(α[6], 17))
    assert round(α[8], 20) == round(2.429170728037E-12, 20), 'a8: {}'.format(round(α[8], 20))
    assert round(α[10], 22) == round(5.711818510466E-15, 22), 'a10: {}'.format(round(α[10], 22))
    assert round(α[12], 24) == round(1.479997974926E-17, 24), 'a12: {}'.format(round(α[12], 24))
    assert round(α[14], 27) == round(4.107624250384E-20, 27), 'a14: {}'.format(round(α[14], 27))
    assert round(α[16], 30) == round(1.210785086483E-22, 30), 'a16: {}'.format(round(α[16], 30))

def test_conformal_latitude():
    t, σ, _t, _φ = conformal_latitude(-0.413121596, 0.081819191043) 

    assert round(t, 12) == -0.438347537637, "t: {}".format(round(t,12))
    assert round(σ, 12) == -0.002688564995, 'σ: {}'.format(round(σ, 12))
    assert round(_t, 12) == -0.435413597268, "_t: {}".format(round(_t, 10))
    assert round(_φ, 12) == -0.410657890504, "_φ: {}".format(round(_φ, 10))

def test_gauss_schreiber():
    _t = -0.435413597639
    ω = -0.019451463
    a = 6378137.0
    _ε, _N = gauss_schreiber(_t, ω, a)

    assert round(_ε, 12) == -0.410727143471, "_e : {}".format(_ε)
    assert round(_N, 12) == -0.017835003097, "_N : {}".format(_N)
    
def test_transverse_mercator():
    _Nu = -0.017835003
    _ε = -0.410727143
    n = 1.679220395E-03
    α = krueger_coefficients(n)

    E, Nu = transverse_mercator(_Nu, _ε, α)
    
    assert round(Nu, 12) == -0.017855357573, 'N: {}'.format(round(N, 9))
    assert round(E, 12) == -0.411341629424, 'E: {}'.format(round(E, 9))

def test_pq_coefficients():
    _N = -0.017835003
    _ε = -0.410727143
    n = 1.679220395E-03
    α = krueger_coefficients(n)

    q, p = pq_coefficients(α, _ε, _N)
    assert round(q, 12) == round(-4.398179750E-05, 12), 'q: {}'.format(round(q, 12))
    assert round(p, 12) == 1.001141754741E+00, 'p: {}'.format(round(p, 12))

def test_grid_convergence():
    q = -4.398179750E-05
    p = 1.001141755E+00
    _t = -0.435413597639
    ω = -0.019451463
    dLat = -23.67012389
    γ = grid_convergence(q, p, _t, ω, dLat)
    assert round(γ, 12) == -0.007810024262, 'γ: {}'.format(γ)

def test_point_scale_factor():
    e2 = 6.694380023E-03
    A = 6367449.1457711
    a = 6378137.0
    q = -4.398179750E-05
    p = 1.001141755E+00
    t = -0.438347538010
    _t = -0.435413597639 
    ω = -0.019451463
    rLat = -0.413121596
    m = point_scale_factor(rLat, A, a, q, p, t, _t, e2, ω)
    assert round(m, 12) == 0.999759539516, 'm: {}'.format(m)