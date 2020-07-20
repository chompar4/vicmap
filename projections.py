import math

cot = lambda x: 1 / tan(x)
π = math.pi
ln = math.log

from math import tan, cos, cosh, sin, sinh, atan, atanh, asinh, sqrt, radians, degrees


def lambert_conformal_conic(dLat, dLng, datum, φ1, φ2, λ0, φ0, E0, N0):
    """
    Perform a transformation from geographic grid coordinates
    using a Lambert conformal conic projection.
    See: https://pubs.usgs.gov/pp/1395/report.pdf
    Accepts:
        dLat: latitude in decimal degrees (-90, 90]
        dLng: longitude in decimal degrees (-180, 180]
        datum: reference ellipsoid and coordinate reference system
        φ1, φ2 : standard parralels 
        λ0: central meridian longitude of grid
        φ0: latitude of central parrelel
        E0: false easting (m)
        N0: false northing (m)
    returns: 
        X: Easting (m)
        Y: Northing (m)
        m: Point Scale Factor
        γ: Grid Convergence
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

    for phi in [dLat, φ1, φ2, φ0]:
        assert -90 < phi <= 90, "{}".format(phi)
    for theta in [dLng, λ0]:
        assert -180 < theta <= 180

    # work with radians
    φ = radians(dLat)
    λ = radians(dLng)

    λ0 = radians(λ0)
    φ0 = radians(φ0)

    φ1 = radians(φ1)
    φ2 = radians(φ2)

    a, _, f, e, e2, n = datum.ellipsoidal_constants

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

    # Step 2: determine easting and northing wrt true origin
    X = r * sin(θ)
    Y = r * cos(θ) - r0

    # Step 3: point scale factor (m) and grid convergence (γ)
    m = -(r * n) / v * cos(φ)
    γ = -θ

    return X + E0, Y + N0, m, γ
