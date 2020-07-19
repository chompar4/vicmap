from constants import (
    semi_major_axis, 
    inverse_flattening,
    E0, 
    N0,
    m0,
    zone_width
)
import math
from utils import (
    get_cm,
    get_zone,
    conformal_latitude,
    gauss_schreiber,
    transverse_mercator,
    pq_coefficients,
    krueger_coefficients,
    rectifying_radius,
    ellipsoidal_constants,
    grid_convergence, 
    point_scale_factor
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

def geographic_to_mga(dLat, dLng):
    """
    Perform a transformation from geographic to MGA grid coordinates
    using the Krueger n-series equations, up to order 8.
    Ellipsoidal constants are defined in the constants file. 
    In theory these calculations should be accutate 
    to the nearest micrometer.
    Accepts:
        dLat: latitude in decimal degrees (-90, 90]
        dLng: longitude in decimal degrees (-180, 180]
    returns: 
        z: Zone
        E: UTM Easting
        N: UTM Northing
        m: Point Scale Factor
        γ: Grid Convergence
    """

    # Define datum
    datum = "GDA20"
    a = semi_major_axis[datum]
    _f = inverse_flattening[datum]

    print('performing conversion using {} datum'.format(datum))

    assert -90 < dLat <= 90, 'latitude out of bounds'
    assert -180 < dLng < 180, 'longitude out of bounds'

    rLat = math.radians(dLat)
    rLng = math.radians(dLng)
    z = get_zone(dLng)

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
    _ε, _Nu = gauss_schreiber(_t, ω, a)

    # Step 7 - TM ratios 
    ε, Nu = transverse_mercator(_Nu, _ε, α)

    # Step 8 - TM coords
    X = A*Nu
    Y = A*ε

    # Step 9 - MGA2020 coordinates (E, N)
    easting = m0 * X + E0
    northing = m0 * Y + N0

    # Step 10 - q & p
    q, p = pq_coefficients(α, _ε, _Nu)

    # Step 11 - Point scale factor m
    m = point_scale_factor(rLat, A, a, q, p, t, _t, e2, ω)

    # Step 12 - Grid convergence γ
    γ = grid_convergence(q, p, _t, ω, dLat)
    dγ = math.degrees(γ)

    return z, easting, northing, m, dγ

def geographic_to_vicgrid94(dLat, dLng):
    pass 

def geographic_to_vicgrid(dLat, dLng):
    pass 