from utils import (
    dms_to_dd,
    point_scale_factor,
    grid_convergence,
    pq_coefficients,
    transverse_mercator,
    gauss_schreiber,
    conformal_latitude,
    rectifying_radius,
    krueger_coefficients,
)

import pytest
import numpy as np

from math import radians


def test_rectifying_radius():
    a = 6378137
    n = 1.679220395e-03
    assert abs(rectifying_radius(a, n) - 6367449.14576869) < 1e-8


def test_krueger_coefficients():
    n = 1.679220395e-03
    α = krueger_coefficients(n)
    assert abs(α[2] - 8.377318247286e-04) < 1e-12
    assert abs(α[4] - 7.608527848150e-07) < 1e-14
    assert abs(α[6] - 1.197645520855e-09) < 1e-16
    assert abs(α[8] - 2.429170728037e-12) < 1e-19
    assert abs(α[10] - 5.711818510466e-15) < 1e-22
    assert abs(α[12] - 1.479997974926e-17) < 1e-24
    assert abs(α[14] - 4.107624250384e-20) < 1e-27
    assert abs(α[16] - 1.210785086483e-22) < 1e-30


def test_conformal_latitude():
    t, σ, _t, _φ = conformal_latitude(-0.413121596, 0.081819191043)

    assert abs(t + 0.438347537637) < 1e-8
    assert abs(σ + 0.002688564995) < 1e-8
    assert abs(_t + 0.435413597268) < 1e-8
    assert abs(_φ + 0.410657890504) < 1e-8


def test_gauss_schreiber():
    _t = -0.435413597639
    ω = -0.019451463
    a = 6378137.0
    _ε, _N = gauss_schreiber(_t, ω, a)

    assert abs(_ε + 0.410727143471) < 1e-8
    assert abs(_N + 0.017835003097) < 1e-8


def test_transverse_mercator():
    _Nu = -0.017835003
    _ε = -0.410727143
    n = 1.679220395e-03
    α = krueger_coefficients(n)

    E, Nu = transverse_mercator(_Nu, _ε, α)

    assert abs(Nu + 0.017855357573) < 1e-8
    assert abs(E + 0.411341629424) < 1e-8


def test_pq_coefficients():
    _N = -0.017835003
    _ε = -0.410727143
    n = 1.679220395e-03
    α = krueger_coefficients(n)

    q, p = pq_coefficients(α, _ε, _N)
    assert abs(q + 4.398179750e-05) < 1e-8
    assert abs(p - 1.001141754741e00) < 1e-8


def test_grid_convergence():
    q = -4.398179750e-05
    p = 1.001141755e00
    _t = -0.435413597639
    ω = -0.019451463
    dLat = -23.67012389
    γ = grid_convergence(q, p, _t, ω, dLat)
    assert abs(γ + 0.007810024262) < 1e-8


def test_point_scale_factor():
    e2 = 6.694380023e-03
    A = 6367449.1457711
    a = 6378137.0
    q = -4.398179750e-05
    p = 1.001141755e00
    t = -0.438347538010
    _t = -0.435413597639
    ω = -0.019451463
    rLat = -0.413121596
    m0 = 0.9996
    m = point_scale_factor(rLat, A, a, q, p, t, _t, e2, ω, m0)
    assert abs(m - 0.999759539516) < 1e-8


def test_dms_to_dd():

    val = dms_to_dd(-23, 40, 12.446020)
    assert abs(val + 23.67012389) < 1e-6

    val = dms_to_dd(133, 53, 7.84784)
    assert abs(val - 133.8855133) < 1e-6
