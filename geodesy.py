from constants import (
    coordinate_set, 
    a, 
    _f, 
    false_easting,
    false_northing,
    central_scale_factor,
    zone_width
)
import math
from utils import (
    get_cm,
    krueger_coefficients,
    rectifying_radius,
    ellipsoidal_constants,
    q_component,
    p_component,
    TM_n_component,
    TM_e_component
)
import numpy as np
import math

tan = math.tan
cos = math.cos
cosh = math.cosh
sin = math.sin
sinh = math.sinh
atan = math.atan 
atanh = math.atanh
asinh = math.asinh
sqrt = math.sqrt

def geographic_to_grid(dLat, dLng):
    """
    Perform a transformation from geographic to grid coordinates
    using the Krueger n-series equations. Ellipsoidal constants
    are defined in the constants file. In theory these 
    calculations should be accutate to less than a micrometer. 
    Accepts:
        - dLat: latitude in decimal degrees (-90, 90]
        - dLng: longitude in decimal degrees (-180, 180]
    returns: 
        - Zone
        - Easting 
        - Northing
        - Point Scale Factor
        - Grid Convergence
    """

    print('performing conversion using {} datum'.format(coordinate_set))

    assert -90 < dLat <= 90, 'latitude out of bounds'
    assert -180 < dLng < 180, 'longitude out of bounds'

    rLat = math.radians(dLat)
    rLng = math.radians(dLng)

    # Step 1: Compute ellipsiodal constants
    f, e2, n = ellipsoidal_constants(_f)

    # Step 2: Compute rectifying radius A 
    A = rectifying_radius(a, n)
    assert round(A, 7)  == 6367449.145771

    # Step 3: krueger coefficients for r = 1, 2, ..., 8
    α = krueger_coefficients(n)

    assert round(α[2], 16) == 8.377318247286E-04, 'a2: {}'.format(round(α2, 16))
    assert round(α[4], 19) == 7.608527848150E-07, 'a4: {}'.format(round(α4, 19))
    assert round(α[6], 21) == 1.197645520855E-09, 'a6: {}'.format(round(α6, 21))
    assert round(α[8], 24) == 2.429170728037E-12, 'a8: {}'.format(round(α8, 24))
    assert round(α[10], 27) == 5.711818510466E-15, 'a10: {}'.format(round(α10, 27))
    assert round(α[12], 29) == 1.479997974926E-17, 'a12: {}'.format(round(α12, 29))
    assert round(α[14], 32) == 4.107624250384E-20, 'a14: {}'.format(round(α14, 32))
    assert round(α[16], 34) == 1.210785086483E-22, 'a16: {}'.format(round(α16, 34))

    # Step 4 - conformal latitude _φ
    e = sqrt(e2)
    t = tan(rLat)
    σ = sinh(e * atanh(e * t / sqrt(1 + t**2)))
    _t = t*sqrt(1 + σ**2) - σ*sqrt(1 + t**2)
    _φ = atan(_t)


    assert round(e, 12)  == 0.081819191043, "e: {}".format(round(e, 12))
    assert round(σ, 12) == -0.002688564997, 'σ: {}'.format(round(σ, 12))
    assert round(_t, 10) == -0.4354135975, "_t: {}".format(round(_t, 10))
    assert round(_φ, 10) == -0.4106578907, "_φ (rad): {}".format(round(_φ, 10))

    # Step 5 - longitude difference 
    central_meridian = get_cm(dLng)
    ω = rLng - math.radians(central_meridian)

    # Step 6 - Gauss-Schreiber 
    u = a * atan(_t/cos(ω))
    v = a * asinh(sin(ω) / sqrt(_t**2 + (cos(ω)**2)))

    _ε = u / a 
    _N = v / a

    assert round(_ε, 9) == -0.410727143, "_e : {}".format(_ε)
    assert round(_N, 9) == -0.017835003, "_N : {}".format(_N)

    # Step 7 - TM rations 
    N = _N + sum(TM_n_component(α, r, _ε, _N) for r in np.linspace(start=1, stop=8, num=8))
    E = _ε + sum(TM_e_component(α, r, _ε, _N) for r in np.linspace(start=1, stop=8, num=8))

    assert round(N, 9) == -0.017855357, 'N: {}'.format(round(N, 9))
    assert round(E, 9) == -0.411341630, 'E: {}'.format(round(E, 9))

    # Step 8 - TM coords
    X = A*N
    Y = A*E

    # Step 9 - MGA2020 coordinates (E, N)
    easting = central_scale_factor * X + false_easting
    northing = central_scale_factor * Y + false_northing

    # currently accurate to 10m - functionalising alpha will fix this
    # assert round(easting, 4) == 386352.3977, 'Easting: {}'.format(round(easting, 4))
    # assert round(northing, 4) == 7381850.7688, 'Northing: {}'.format(northing)

    print('Easting: {}'.format(easting))
    print('Northing: {}'.format(northing))

    # Step 10 - q & p
    q = - sum(q_component(α, r, _ε, _N) for r in np.linspace(start=1, stop=8, num=8))
    p = 1 + sum(p_component(α, r, _ε, _N) for r in np.linspace(start=1, stop=8, num=8))

    assert round(q, 13) == -4.39817971E-05, 'q: {}'.format(round(q, 13))
    assert round(p, 9) == 1.001141755, 'q: {}'.format(round(p, 9))

    # Step 11 - Point scale factor k
    k = central_scale_factor * (A/a) * sqrt(q**2 + p**2) * (
        sqrt(1 + t**2)*sqrt(1-e2*sin(rLat)**2)
        /
        sqrt(_t**2 + cos(ω)**2)
    )

    assert round(k, 10) == round(0.99975953924774, 10), 'k: {}'.format(k)

    # Step 12 - Grid convergence γ
    γ = grid_convergence(q, p, _t, ω)
    assert round(γ, 9) == round(0.0078100240938, 9), 'γ: {}'.format(γ)

if __name__ == "__main__":
    geographic_to_grid(-23.67012389, 133.8855133)