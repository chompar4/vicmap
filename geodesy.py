from constants import (
    E0_mga, 
    N0_mga,
    E0_vicgrid94, 
    N0_vicgrid94,
    m0,
    zone_width
)
import math
from utils import (
    vicgrid94_constants,
    get_cm,
    get_zone,
    conformal_latitude,
    gauss_schreiber,
    transverse_mercator,
    pq_coefficients,
    krueger_coefficients,
    rectifying_radius,
    grid_convergence, 
    point_scale_factor
)
import numpy as np
import math
cot = lambda x: 1/tan(x)
π = math.pi

from math import tan, cos, cosh, sin, sinh, atan, atanh, asinh, sqrt, radians, degrees
from datums import GDA20

def geographic_to_mga(dLat, dLng, datum=GDA20):
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

    print('performing conversion using {} datum'.format(datum.name))

    assert -90 < dLat <= 90, 'latitude out of bounds'
    assert -180 < dLng < 180, 'longitude out of bounds'

    rLat = radians(dLat)
    rLng = radians(dLng)
    z = get_zone(dLng)

    # Step 1: Compute ellipsiodal constants
    a, f, e, e2, n = datum.constants

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
    easting = m0 * X + E0_mga
    northing = m0 * Y + N0_mga

    # Step 10 - q & p
    q, p = pq_coefficients(α, _ε, _Nu)

    # Step 11 - Point scale factor m
    m = point_scale_factor(rLat, A, a, q, p, t, _t, e2, ω)

    # Step 12 - Grid convergence γ
    γ = grid_convergence(q, p, _t, ω, dLat)
    dγ = math.degrees(γ)

    return z, easting, northing, m, dγ

def geographic_to_vicgrid94(dLat, dLng):
    
    from constants import φ1, φ2, cm_vicgrid94, λ0, φ0, datum_vicgrid94
    from datums import GDA20

    # datum 
    datum = GDA20

    # pre-compute
    qp = 1/4*π

    # work with radians
    φ = radians(dLat)
    λ = radians(dLng)

    φ1 = radians(φ1)
    φ2 = radians(φ2)
    λ0 = radians(λ0)
    φ0 = radians(φ0)

    # Step 1: n, r, ρ0, F
    n, F, r0, m, q = vicgrid94_constants(φ, φ0, φ1, φ2, datum)

    # Step 2: determine easting and northing
    r = -n * (m * tan(q)) ** n
    θ = -n * (λ - λ0)

    X = r * sin(θ)
    Y = r * cos(θ) - r0

    return X + E0_vicgrid94, Y + N0_vicgrid94



def geographic_to_vicgrid(dLat, dLng):
    pass