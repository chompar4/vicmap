from utils import ellipsoidal_constants, rectifying_radius, krueger_coefficients

def test_ellipsoidal_constants():

    inv_flat = 298.257222101
    f, e2, n = ellipsoidal_constants(inv_flat) 
    assert round(f, 12) == 3.352810681E-03
    assert round(e2, 12) == 6.694380023E-03
    assert round(n, 12) == 1.679220395E-03

def test_rectifying_radius():
    a = 6378137
    n = 1.679220395E-03
    assert round(rectifying_radius(a, n), 7 == 6367449.145771)

def test_krueger_coefficients():
    n = 1.679220395E-03
    α = krueger_coefficients(n)
    assert round(α[2], 12) == round(8.377318247286E-04, 12), 'a2: {}'.format(round(α[2], 12))
    assert round(α[4], 15) == round(7.608527848150E-07, 15), 'a4: {}'.format(round(α[4], 15))
    assert round(α[6], 17) == round(1.197645520855E-09, 17), 'a6: {}'.format(round(α[6], 17))
    assert round(α[8], 20) == round(2.429170728037E-12, 20), 'a8: {}'.format(round(α[8], 20))
    assert round(α[10], 22) == round(5.711818510466E-15, 22), 'a10: {}'.format(round(α[10], 22))
    assert round(α[12], 24) == round(1.479997974926E-17, 24), 'a12: {}'.format(round(α[12], 24))
    assert round(α[14], 27) == round(4.107624250384E-20, 27), 'a14: {}'.format(round(α[14], 27))
    assert round(α[16], 30) == round(1.210785086483E-22, 30), 'a16: {}'.format(round(α[16], 30))

