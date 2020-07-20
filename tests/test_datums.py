from datums import GDA20, GDA94, AGD84, AGD66, ANG


def test_gda20():

    a, b, f, e, e2, n = GDA20.ellipsoid.constants

    assert a == 6378137
    assert 1 / f == 298.257222101
    assert b == 6399593.625864023
    assert round(e2, 9) == 0.006694380
    assert round(e, 9) == 0.081819191


def test_gda94():

    a, b, f, e, e2, n = GDA94.ellipsoid.constants

    assert a == 6378137
    assert 1 / f == 298.257222101
    assert b == 6399593.625864023
    assert round(e2, 9) == 0.006694380
    assert round(e, 9) == 0.081819191


def test_agd84():

    a, b, f, e, e2, n = AGD84.ellipsoid.constants

    assert a == 6378160
    assert 1 / f == 298.25
    assert b == 6399617.224558453
    assert round(e2, 9) == 0.006694542
    assert round(e, 9) == 0.08182018


def test_agd66():

    a, b, f, e, e2, n = AGD66.ellipsoid.constants

    assert a == 6378160
    assert 1 / f == 298.25
    assert b == 6399617.224558453
    assert round(e2, 9) == 0.006694542
    assert round(e, 9) == 0.08182018


def test_ang():

    a, b, f, e, e2, n = ANG.ellipsoid.constants

    assert a == 6378350.871924
    assert 1 / f == 294.26
    assert b == 6400100.687350324
    assert round(e2, 9) == 0.006785162
    assert round(e, 9) == 0.082372092
