import math
from math import asinh, atan, atan2, atanh, cos, cosh, sin, sinh, sqrt, tan

import numpy as np

from vicmap.datums import GDA20

ln = math.log
sec = lambda x: 1 / cos(x)
cot = lambda x: 1 / tan(x)
π = math.pi


def dms_to_dd(d, m, s):
    assert -180 <= d <= 180
    assert 0 <= m < 60
    assert 0 <= s < 3600
    sign = -1 if d < 0 else 1
    dd = abs(d) + m / 60 + s / 3600
    return sign * dd


def TM_n_component(α, r, _ε, _N):
    return α[2 * r] * cos(2 * r * _ε) * sinh(2 * r * _N)


def TM_e_component(α, r, _ε, _N):
    return α[2 * r] * sin(2 * r * _ε) * cosh(2 * r * _N)


def rectifying_radius(a, n):
    """
    gives the rectifying radius A of a circle having
    the same circumference as the meridian ellipse with:
        a: semi major axis
        n: 3rd flattening
    """
    return (a / (1 + n)) * (
        1
        + (1 / 4) * n ** 2
        + (1 / 64) * n ** 4
        + (1 / 256) * n ** 6
        + (25 / 16384) * n ** 8
    )


def transverse_mercator(_Nu, _ε, α):
    """
    Compute normalised TM coordinates (ε, Nu)
    Accepts:
        _Nu: normalised gauss-schreiber northing
        _ε: normalised gauss-schreiber easting
        α: krueger_coefficients
    returns
        Nu: normalised TM northing
        ε: normalised TM easting
    """
    Nu = _Nu + sum(
        TM_n_component(α, r, _ε, _Nu) for r in np.linspace(start=1, stop=8, num=8)
    )
    ε = _ε + sum(
        TM_e_component(α, r, _ε, _Nu) for r in np.linspace(start=1, stop=8, num=8)
    )
    return ε, Nu


def gauss_schreiber(_t, ω, a):
    """
    gives a gauss-schreiber projection
    accepts:
        - t: tan of conformal latitude
        - ω: longitudal difference
        - a: ellipsoidal semi major axis
    returns:
        - _ε, _Nu : normalised gauss-schreiber coords
    """

    u = a * atan(_t / cos(ω))
    v = a * asinh(sin(ω) / sqrt(_t ** 2 + (cos(ω) ** 2)))

    _ε = u / a
    _Nu = v / a
    return _ε, _Nu


def q_component(α, r, _ε, _N):
    return 2 * r * α[2 * r] * sin(2 * r * _ε) * sinh(2 * r * _N)


def p_component(α, r, _ε, _N):
    return 2 * r * α[2 * r] * cos(2 * r * _ε) * cosh(2 * r * _N)


def pq_coefficients(α, _ε, _N):
    """
    gives the p, q coefficients for eq (70-75)
    accepts:
        _N: normalised gauss-schreiber northing
        _ε: normalised gauss-schreiber easting
        α: krueger_coefficients
    returns:
        p, q: coeffs
    """
    q = -sum(q_component(α, r, _ε, _N) for r in np.linspace(start=1, stop=8, num=8))
    p = 1 + sum(p_component(α, r, _ε, _N) for r in np.linspace(start=1, stop=8, num=8))
    return q, p


def conformal_latitude(φ, e):
    """
    gives the latitude of the conformal sphere
    with radius a. Accepts:
        φ: geographical latitude in radians
        e: ellipsoidal eecentricity
    returns
        t, σ : geographical properties
        _t, _σ: conformal properties

    """
    t = tan(φ)
    σ = sinh(e * atanh(e * t / sqrt(1 + t ** 2)))
    _t = t * sqrt(1 + σ ** 2) - σ * sqrt(1 + t ** 2)
    _φ = atan(_t)
    return t, σ, _t, _φ


def grid_convergence(q, p, _t, ω, dLat):
    """
    gives the angle between the meridian
    and the grid-line parallel to the u-axis
    for an MGA projection.
    """
    g = atan(abs(q / p)) + atan(abs(_t * tan(ω)) / sqrt(1 + _t ** 2))

    # East/West of Central Meridian
    ew = 1 if ω > 0 else -1

    # NOTE: this also depends if north of equator.
    # Only care about vic so assume ns = -1
    # ns = 1 if dLat > 0 else -1
    ns = -1

    coeff = -1 if ew == ns else 1
    return coeff * g


def point_scale_factor(rLat, A, a, q, p, t, _t, e2, ω, m0):
    """
    gives the point scale factor
    """
    return (
        m0
        * (A / a)
        * sqrt(q ** 2 + p ** 2)
        * (
            sqrt(1 + t ** 2)
            * sqrt(1 - e2 * sin(rLat) ** 2)
            / sqrt(_t ** 2 + cos(ω) ** 2)
        )
    )


def krueger_coefficients(n):
    """
    Compute the coefficients (α) required for Kruegers eq'n.
    See docs in reference for these. AFAIK know general form
    of these has been presented.
    """

    n2 = n ** 2
    n3 = n ** 3
    n4 = n ** 4
    n5 = n ** 5
    n6 = n ** 6
    n7 = n ** 7
    n8 = n ** 8

    α2 = (
        1 / 2 * n
        - 2 / 3 * n2
        + 5 / 16 * n3
        + 41 / 180 * n4
        - 127 / 288 * n5
        + 7891 / 37800 * n6
        + 72161 / 387072 * n7
        - 18975107 / 50803200 * n8
    )

    α4 = (
        13 / 48 * n2
        - 3 / 5 * n3
        + 557 / 1440 * n4
        + 281 / 630 * n5
        - 1983433 / 1935360 * n6
        + 13769 / 28800 * n7
        + 148003883 / 174182400 * n8
    )
    α6 = (
        61 / 240 * n3
        - 103 / 140 * n4
        + 15061 / 26880 * n5
        + 167603 / 181440 * n6
        - 67102379 / 29030400 * n7
        + 79682431 / 79833600 * n8
    )
    α8 = (
        49561 / 161280 * n4
        - 179 / 168 * n5
        + 6601661 / 7257600 * n6
        + 97445 / 49896 * n7
        - 40176129013 / 7664025600 * n8
    )
    α10 = (
        34729 / 80640 * n5
        - 3418889 / 1995840 * n6
        + 14644087 / 9123840 * n7
        + 2605413599 / 622702080 * n8
    )
    α12 = (
        212378941 / 319334400 * n6
        - 30705481 / 10378368 * n7
        + 175214326799 / 58118860800 * n8
    )
    α14 = 1522256789 / 1383782400 * n7 - 16759934899 / 3113510400 * n8
    α16 = 1424729850961 / 743921418240 * n8

    return {2: α2, 4: α4, 6: α6, 8: α8, 10: α10, 12: α12, 14: α14, 16: α16}


def ellipsoidal_distance(φ1, λ1, φ2, λ2, a, b, f):
    """
    Use Vincenty's inverse formula along an ellipsoidal geodesic
    (assumes radians are specified as input)
    accepts:
        - φ1 : decimal latitude in radians
        - λ1 : decimal longitude in radians
        - φ2 : decimal latitude in radians
        - λ1 : decimal longitude in radians
        - a, b, f : ellipsoidal constants
    returns
        - s : ellipsoidal arc distance (meters)
    Reference (pg 49):
    https://www.icsm.gov.au/sites/default/files/2020-08/GDA2020%20Technical%20Manual%20V1.4_0.pdf
    """

    U1 = atan((1 - f) * tan(φ1))
    U2 = atan((1 - f) * tan(φ2))

    λ = λ2 - λ1

    tol = 1e-11
    λ_old = λ
    for iter in range(1, 16):

        t = (cos(U2) * sin(λ_old)) ** 2
        t += (cos(U1) * sin(U2) - sin(U1) * cos(U2) * cos(λ_old)) ** 2

        sin_σ = t ** 0.5
        cos_σ = sin(U1) * sin(U2) + cos(U1) * cos(U2) * cos(λ_old)
        σ = atan2(sin_σ, cos_σ)

        sin_α = cos(U1) * cos(U2) * sin(λ_old) / sin_σ
        cos_sq_α = 1 - sin_α ** 2
        cos_2σ_m = cos_σ - 2 * sin(U1) * sin(U2) / cos_sq_α
        C = f * cos_sq_α * (4 + f * (4 - 3 * cos_sq_α)) / 16

        t = σ + C * sin_σ * (cos_2σ_m + C * cos_σ * (-1 + 2 * cos_2σ_m ** 2))
        λ_new = λ + (1 - C) * f * sin_α * t
        if abs(λ_new - λ_old) <= tol:
            break
        else:
            λ_old = λ_new

    u2 = cos_sq_α * ((a ** 2 - b ** 2) / b ** 2)
    A = 1 + (u2 / 16384) * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = (u2 / 1024) * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    t = cos_2σ_m + 0.25 * B * (cos_σ * (-1 + 2 * cos_2σ_m ** 2))
    t -= (B / 6) * cos_2σ_m * (-3 + 4 * sin_σ ** 2) * (-3 + 4 * cos_2σ_m ** 2)
    delta_σ = B * sin_σ * t
    s = b * A * (σ - delta_σ)

    return s
