from datums import GDA20

def test_ellipsoidal_constants():

    a, b, f, e, e2, n = GDA20.ellipsoidal_constants

    assert a == 6378137
    assert 1/f == 298.257222101
    assert b == 6399593.625864023
    assert round(e2, 9) == 0.006694380
    assert round(e, 9) == 0.081819191