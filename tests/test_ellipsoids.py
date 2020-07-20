from ellipsoids import WGS84, GRS80, ANS, ANG

def test_wgs84():

    datum = WGS84 

    assert datum.a == 6378137
    assert datum._f == 298.257223563
    assert datum.b == 6399593.625758493
    assert round(datum.e2, 9) == 0.006694380
    assert round(datum.e, 9) == 0.081819191

def test_grs80():

    datum = GRS80

    assert datum.a == 6378137
    assert datum._f == 298.257222101
    assert datum.b == 6399593.625864023
    assert round(datum.e2, 9) == 0.006694380
    assert round(datum.e, 9) == 0.081819191

def test_ans():

    datum = ANS

    assert datum.a == 6378160
    assert datum._f == 298.25
    assert datum.b == 6399617.224558453
    assert round(datum.e2, 9) == 0.006694542
    assert round(datum.e, 9) == 0.08182018

def test_ang():

    datum = ANG

    assert datum.a == 6378350.871924
    assert datum._f == 294.26
    assert datum.b == 6400100.687350324
    assert round(datum.e2, 9) == 0.006785162
    assert round(datum.e, 9) == 0.082372092