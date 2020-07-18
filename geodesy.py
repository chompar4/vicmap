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
    TM_e_component, 
    grid_convergence
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
    f, e, e2, n = ellipsoidal_constants(_f)

    # Step 2: Compute rectifying radius A
    A = rectifying_radius(a, n)

    # Step 3: krueger coefficients for r = 1, 2, ..., 8
    α = krueger_coefficients(n)

    # Step 4 - conformal latitude _φ
    t, σ, _t, _φ = conformal_latitude(rLat, e) 

    # Step 5 - longitude difference
    central_meridian = get_cm(dLng)
    ω = rLng - math.radians(central_meridian)

    # Step 6 - Gauss-Schreiber 
    _ε, _N = gauss_schreiber(_t, ω, a)

    # Step 7 - TM ratios 
    N, E = transverse_mercator(_N, _ε, α)

    # Step 8 - TM coords
    X = A*N
    Y = A*E

    # Step 9 - MGA2020 coordinates (E, N)
    easting = central_scale_factor * X + false_easting
    northing = central_scale_factor * Y + false_northing

    print('Easting: {}'.format(easting))
    print('Northing: {}'.format(northing))

    # Step 10 - q & p
    q, p = pq_coefficients(α, _ε, _N)

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