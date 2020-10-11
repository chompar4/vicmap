from vicmap.ellipsoids import ANS, CLARKE, GRS67, GRS80, WGS84


def test_wgs84():

    ellipsoid = WGS84

    assert ellipsoid.a == 6378137
    assert ellipsoid._f == 298.257223563
    assert ellipsoid.b == 6356752.314245179
    assert abs(ellipsoid.e2 - 0.006694380) < 1e-8
    assert abs(ellipsoid.e - 0.081819191) < 1e-8


def test_grs80():

    ellipsoid = GRS80

    assert ellipsoid.a == 6378137
    assert ellipsoid._f == 298.257222101
    assert ellipsoid.b == 6399593.625864023
    assert abs(ellipsoid.e2 - 0.006694380) < 1e-8
    assert abs(ellipsoid.e - 0.081819191) < 1e-8


def test_grs80():

    ellipsoid = GRS67

    assert ellipsoid.a == 6378160
    assert ellipsoid._f == 298.247167427
    assert ellipsoid.b == 6356774.516090714
    print(ellipsoid.e2, ellipsoid.e)
    assert abs(ellipsoid.e2 - 0.006694605328567654) < 1e-8
    assert abs(ellipsoid.e - 0.08182056788221195) < 1e-8


def test_ans():

    ellipsoid = ANS

    assert ellipsoid.a == 6378160
    assert ellipsoid._f == 298.25
    assert ellipsoid.b == 6356774.719195305
    assert abs(ellipsoid.e2 - 0.006694542) < 1e-8
    assert abs(ellipsoid.e - 0.08182018) < 1e-8


def test_clarke():

    ellipsoid = CLARKE

    assert ellipsoid.a == 6378350.871924
    assert ellipsoid._f == 294.26
    assert ellipsoid.b == 6356674.970095943
    assert abs(ellipsoid.e2 - 0.006785162) < 1e-8
    assert abs(ellipsoid.e - 0.082372092) < 1e-8
