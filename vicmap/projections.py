import math

cot = lambda x: 1 / tan(x)
π = math.pi
ln = math.log

from math import tan, cos, cosh, sin, sinh, atan, atanh, asinh, sqrt, radians, degrees

from vicmap.utils import (
    conformal_latitude,
    gauss_schreiber,
    transverse_mercator,
    pq_coefficients,
    krueger_coefficients,
    rectifying_radius,
    grid_convergence,
    point_scale_factor,
)


def lambert_conformal_conic(dLat, dLng, ellipsoid, grid):
    """
    Perform a transformation from geographic to grid coordinates
    using a Lambert conformal conic projection.
    See: https://pubs.usgs.gov/pp/1395/report.pdf
    Accepts:
        dLat: latitude in decimal degrees (-90, 90]
        dLng: longitude in decimal degrees (-180, 180]
        ellipsoidal: reference ellipsoid containing ellipsoidal constants
        grid: plane specification containing grid constants
    returns: 
        X: easting (m) relative to false origin
        Y: northing (m) relative to false origin
        m: point scale factor
        γ: grid convergence
    """

    # Helper functions
    def Q(φ):
        return π / 4 - φ / 2

    def T(φ):
        lhs = (1 - sin(φ)) / (1 + sin(φ))
        rhs = (1 + e * sin(φ)) / (1 - e * sin(φ))
        inner = lhs * (rhs ** e)
        return sqrt(inner)

    def V(φ):
        bottom = 1 - e2 * sin(φ) ** 2
        return a / sqrt(bottom)

    def M(φ):
        top = cos(φ)
        bottom = 1 - e ** 2 * sin(φ) ** 2
        return top / sqrt(bottom)

    φ1, φ2, λ0, φ0, E0, N0 = grid.constants

    for phi in [dLat, φ1, φ2, φ0]:
        assert -90 < phi <= 90, "{}".format(phi)
    for theta in [dLng, λ0]:
        assert -180 < theta <= 180

    # Step 1: work with radians
    φ = radians(dLat)
    λ = radians(dLng)

    λ0 = radians(λ0)
    φ0 = radians(φ0)

    φ1 = radians(φ1)
    φ2 = radians(φ2)

    a, _, f, e, e2, n = ellipsoid.constants

    m1 = M(φ1)
    m2 = M(φ2)
    q1 = Q(φ1)
    t1 = T(φ1)
    t2 = T(φ2)
    t0 = T(φ0)
    t = T(φ)
    v = V(φ)

    n = (ln(m1) - ln(m2)) / (ln(t1) - ln(t2))
    F = m1 / (n * (t1 ** n))

    # Step 2: determine polar coords
    rCoeff = -1 if n < 0 else 1
    r0 = rCoeff * a * F * (t0 ** n)
    r = rCoeff * a * F * (t ** n)
    θ = rCoeff * n * (λ - λ0)

    # Step 3: determine easting and northing wrt true origin
    X = r * sin(θ)
    Y = r * cos(θ) - r0

    # Step 4: point scale factor (m) and grid convergence (γ)
    m = -(r * n) / v * cos(φ)
    γ = θ

    return X + E0, Y + N0, m, math.degrees(γ)


def utm(dLat, dLng, ellipsoid, grid):
    """
    Perform a UTM projection from ellipsoid to grid
    using the Krueger n-series equations, up to order 8.
    See: https://www.icsm.gov.au/sites/default/files/GDA2020TechnicalManualV1.1.1.pdf
    In theory these calculations should be accurate 
    to the nearest micrometer.
    Accepts:
        dLat: latitude in decimal degrees (-90, 90]
        dLng: longitude in decimal degrees (-180, 180]
        ellipsoidal: reference ellipsoid containing ellipsoidal constants
        grid: plane specification containing grid constants
    returns: 
        z: zone
        E: UTM easting (m) relative to false origin
        N: UTM northing (m) relative to false origin
        m: point scale factor
        γ: grid convergence
    """

    assert -90 < dLat <= 90, "latitude out of bounds"
    assert -180 < dLng < 180, "longitude out of bounds"

    rLat = radians(dLat)
    rLng = radians(dLng)

    m0 = grid.m0
    zn = grid.get_zone(dLng)
    cm = grid.get_cm(zn)

    # Step 1: Compute ellipsiodal constants
    a, _, f, e, e2, n = ellipsoid.constants

    # Step 2: Compute rectifying radius A
    A = rectifying_radius(a, n)

    # Step 3: krueger coefficients for r = 1, 2, ..., 8
    α = krueger_coefficients(n)

    # Step 4 - conformal latitude _φ
    t, σ, _t, _φ = conformal_latitude(rLat, e)

    # Step 5 - longitude difference
    ω = rLng - math.radians(cm)

    # Step 6 - Gauss-Schreiber
    _ε, _Nu = gauss_schreiber(_t, ω, a)

    # Step 7 - TM ratios
    ε, Nu = transverse_mercator(_Nu, _ε, α)

    # Step 8 - TM coords
    X = A * Nu
    Y = A * ε

    # Step 9 - MGA2020 coordinates (E, N)
    easting = grid.m0 * X + grid.E0
    northing = grid.m0 * Y + grid.N0

    # Step 10 - q & p
    q, p = pq_coefficients(α, _ε, _Nu)

    # Step 11 - Point scale factor m
    m = point_scale_factor(rLat, A, a, q, p, t, _t, e2, ω, m0)

    # Step 12 - Grid convergence γ
    γ = grid_convergence(q, p, _t, ω, dLat)

    return zn, easting, northing, m, math.degrees(γ)
