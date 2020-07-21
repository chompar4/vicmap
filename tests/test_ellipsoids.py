from geodesy.ellipsoids import WGS84, GRS80, ANS, CLARKE


def test_wgs84():

    ellipsoid = WGS84

    assert ellipsoid.a == 6378137
    assert ellipsoid._f == 298.257223563
    assert ellipsoid.b == 6399593.625758493
    assert abs(ellipsoid.e2 - 0.006694380) < 1e-8
    assert abs(ellipsoid.e - 0.081819191) < 1e-8
    assert ellipsoid.url == "https://epsg.io/7030-ellipsoid"


def test_grs80():

    ellipsoid = GRS80

    assert ellipsoid.a == 6378137
    assert ellipsoid._f == 298.257222101
    assert ellipsoid.b == 6399593.625864023
    assert abs(ellipsoid.e2 - 0.006694380) < 1e-8
    assert abs(ellipsoid.e - 0.081819191) < 1e-8
    assert ellipsoid.url == "https://epsg.io/7019-ellipsoid"


def test_ans():

    ellipsoid = ANS

    assert ellipsoid.a == 6378160
    assert ellipsoid._f == 298.25
    assert ellipsoid.b == 6399617.224558453
    assert abs(ellipsoid.e2 - 0.006694542) < 1e-8
    assert abs(ellipsoid.e - 0.08182018) < 1e-8
    assert ellipsoid.url == "https://epsg.io/7003-ellipsoid"


def test_clarke():

    ellipsoid = CLARKE

    assert ellipsoid.a == 6378350.871924
    assert ellipsoid._f == 294.26
    assert ellipsoid.b == 6400100.687350324
    assert abs(ellipsoid.e2 - 0.006785162) < 1e-8
    assert abs(ellipsoid.e - 0.082372092) < 1e-8
    assert ellipsoid.url == "https://epsg.io/7008-ellipsoid"
