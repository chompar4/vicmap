from vicmap.datums import GDA20, GDA94, AGD84, AGD66


def test_gda20():

    a, b, f, e, e2, n = GDA20.ellipsoid.constants

    assert a == 6378137
    assert 1 / f == 298.257222101
    assert b == 6399593.625864023
    assert abs(e2 - 0.006694380) < 1e-8
    assert abs(e - 0.081819191) < 1e-8


def test_gda94():

    a, b, f, e, e2, n = GDA94.ellipsoid.constants

    assert a == 6378137
    assert 1 / f == 298.257222101
    assert b == 6399593.625864023
    assert abs(e2 - 0.006694380) < 1e-8
    assert abs(e - 0.081819191) < 1e-8


def test_agd84():

    a, b, f, e, e2, n = AGD84.ellipsoid.constants

    assert a == 6378160
    assert 1 / f == 298.25
    assert b == 6399617.224558453
    assert abs(e2 - 0.006694542) < 1e-8
    assert abs(e - 0.08182018) < 1e-8


def test_agd66():

    a, b, f, e, e2, n = AGD66.ellipsoid.constants

    assert a == 6378160
    assert 1 / f == 298.25
    assert b == 6399617.224558453
    assert abs(e2 - 0.006694542) < 1e-8
    assert abs(e - 0.08182018) < 1e-8
