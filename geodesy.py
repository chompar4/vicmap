from constants import coordinate_set, a, _f, false_easting, false_northing, central_scale_factor, zone_width, central_meridian
import math
from utils import get_cm

tan = math.tan 
cos = math.cos 
sin = math.sin
sinh = math.sinh
atan = math.atan 
atanh = math.atanh
asinh = math.asinh
sqrt = math.sqrt

def geographic_to_grid(dLat, dLng):
    print('performing conversion using {}'.format(coordinate_set))

    rLat = math.radians(dLat)
    rLng = math.radians(dLng)


    # Step 1: Compute ellipsiodal constants

    f = 1/_f            # flattening 
    e2 = f * (2-f)      # e^2
    n = f / (2-f)       # n 

    # Step 2a: Compute powers of n 
    n2 = n ** 2
    n3 = n ** 3
    n4 = n ** 4
    n5 = n ** 5
    n6 = n ** 6 
    n7 = n ** 7
    n8 = n ** 8

    # Step 2b: Compute rectifying radius A 
    A = a / (1 + n) * (
        1 
        + (1/4) * n2 
        + (1/64) * n4
        + (1/256) * n6 
        + (25/ 16384) * n8
    )

    assert round(A, 7)  == 6367449.145771

    # Step 3: {\alpha_2r} coefficients for r = 1, 2, ..., 8
    # TODO: functionalise
    α2 = (
        1/2*n 
        - 2/3*n2 
        + 5/16*n3 
        + 41/180*n4 
        - 127/288*n5 
        + 7891/37800*n6 
        + 72161/387072*n7
        - 18975107/50803200*n8 
    )
    α4 = (
        13/48*n2 
        -3/5*n3 
        + 557/1440*n4
        +281/630*n5
        -1983433/1935360*n6 
        +13769/28800*n7
        +148003883/174182400*n8
    )
    α6 = (
        61/240*n3
        - 103/140*n4
        +15061/26880*n5
        + 167603/181440*n6 
        - 67102379/29030400*n7
        +79682431/79833600*n8
    )
    α8 = (
        49561/161280*n4 
        - 179/168*n5 
        + 6601661/7257600*n6 
        + 97445/49896*n7 
        - 40176129013/7664025600*n8
    )
    α10 = (
        34729/80640*n5
        - 3418889/1995840*n6
        +14644087/9123840*n7 
        + 2605413599/622702080*n8
    )
    α12 = (
        212378941/319334400*n6
        -30705481/10378368*n7 
        + 175214326799/58118860800*n8
    )
    α14 = (
        1522256789/1383782400*n7 
        - 16759934899/3113510400*n8
    )
    α16 = (
        1424729850961/743921418240*n8
    )

    assert round(α2, 16) == 8.377318247286E-04, 'a2: {}'.format(round(α2, 16))
    assert round(α4, 19) == 7.608527848150E-07, 'a4: {}'.format(round(α4, 19))
    assert round(α6, 21) == 1.197645520855E-09, 'a6: {}'.format(round(α6, 21))
    assert round(α8, 24) == 2.429170728037E-12, 'a8: {}'.format(round(α8, 24))
    assert round(α10, 27) == 5.711818510466E-15, 'a10: {}'.format(round(α10, 27))
    assert round(α12, 29) == 1.479997974926E-17, 'a12: {}'.format(round(α12, 29))
    assert round(α14, 32) == 4.107624250384E-20, 'a14: {}'.format(round(α14, 32))
    assert round(α16, 34) == 1.210785086483E-22, 'a16: {}'.format(round(α16, 34))

    # Step 4 - conformal latitude φ

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
    v = a * asinh(
        sin(ω) / sqrt(_t**2 + (cos(ω)**2))
        )

    _ε = u / a 
    _N = v / a

    assert round(_ε, 9) == -0.410727143, "_e : {}".format(_ε)
    assert round(_N, 9) == -0.017835003, "_N : {}".format(_N)

if __name__ == "__main__":
    geographic_to_grid(-23.67012389, 133.8855133)