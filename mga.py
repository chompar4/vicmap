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
    grid_convergence, 
    point_scale_factor
)
from constants.mga import (
    E0, 
    N0,
    zone_width, 
    m0
)
import numpy as np
import math
cot = lambda x: 1/tan(x)
π = math.pi
ln = math.log

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
        datum: default GDA20
    returns: 
        z: Zone
        E: UTM Easting
        N: UTM Northing
        m: Point Scale Factor
        γ: Grid Convergence
    """

    print('geo -> MGA using {} datum'.format(datum.name))

    assert -90 < dLat <= 90, 'latitude out of bounds'
    assert -180 < dLng < 180, 'longitude out of bounds'

    rLat = radians(dLat)
    rLng = radians(dLng)
    z = get_zone(dLng)

    # Step 1: Compute ellipsiodal constants
    a, b, f, e, e2, n = datum.ellipsoidal_constants

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

def mga_to_geographic(E, N, datum=GDA20):
    """
    Inverse transformation from MGA coords to 
    geographic coords.
    """
    pass