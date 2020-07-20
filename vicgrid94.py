import numpy as np
import math
cot = lambda x: 1/tan(x)
π = math.pi
ln = math.log

from math import tan, cos, cosh, sin, sinh, atan, atanh, asinh, sqrt, radians, degrees
from datums import GDA20
from constants.vicgrid94 import N0


def geographic_to_vicgrid94(dLat, dLng, datum=GDA20):
    """
    Perform a transformation from geographic to VICGRID94 grid coordinates
    using a Lambert conformal conic projection.
    Ellipsoidal constants are defined in the constants file. 
    In theory these calculations should be accutate 
    to the nearest meter.
    Accepts:
        dLat: latitude in decimal degrees (-90, 90]
        dLng: longitude in decimal degrees (-180, 180]
        datum: default GDA20
    returns: 
        E: VICGRID94 Easting
        N: VICGRID94 Northing
        m: Point Scale Factor
        γ: Grid Convergence
    """

    from constants.vicgrid94 import φ1, φ2, λ0, φ0, E0, N0
    print('geo -> VICGRID94 using {} datum'.format(datum.name))
    
    # Helper functions
    def Q(φ):
        return π/4 - φ/2

    def T(φ):
        lhs = (1 - sin(φ)) / (1 + sin(φ))
        rhs = (1 + e * sin(φ)) / (1 - e * sin(φ))
        inner = lhs * (rhs ** e)
        return sqrt(inner)

    def M(φ):
        top = cos(φ)
        bottom = (1 - e**2 * sin(φ) **2)
        return top / sqrt(bottom)

    # work with radians
    φ = radians(dLat)
    λ = radians(dLng)

    λ0 = radians(λ0)
    φ0 = radians(φ0)

    φ1 = radians(φ1)
    φ2 = radians(φ2)

    a, _, f, e, e2, n = datum.constants

    m1 = M(φ1)
    m2 = M(φ2)
    q1 = Q(φ1)
    t1 = T(φ1)
    t2 = T(φ2)
    t0 = T(φ0)
    t = T(φ)

    n = (ln(m1) - ln(m2))/(ln(t1)-ln(t2))
    F = m1 / (n*(t1**n))

    # Step 2: determine polar coords
    rCoeff = -1 if n < 0 else 1
    r0 = rCoeff * a * F * (t0**n)
    r = rCoeff * a * F * (t**n)
    θ = rCoeff * n * (λ - λ0)

    # Step 2: determine easting and northing wrt true origin
    X = r * sin(θ)
    Y = r * cos(θ) - r0

    # TODO: m and γ
    m = None
    γ = None

    return X + E0, Y + N0, m, γ


def geographic_to_vicgrid(dLat, dLng):
    pass