from math import sqrt
from constants import semi_major_axis, semi_minor_axis, inverse_flattening

class Datum:
    def __init__(self, name):
        """
        creates a geodetic datum from paramaters
            a: equatorial radius (semi-major axis)
            b: polar radius (semi-minor axis)
            _f: inverse flattening 1/f
        """

        self.a = semi_major_axis[name]
        self.b = semi_minor_axis[name]
        self._f = inverse_flattening[name]
        self.name = name

    @property
    def e2(self):
        "e^2: eecentricity squared"
        return self.f * (2-self.f)

    @property
    def e(self):
        "eecentricity"
        return sqrt(self.e2)

    @property
    def n(self):
        "n: 3rd flattening"
        return self.f / (2 - self.f)

    @property
    def f(self):
        "f: flattening"
        return 1/self._f

    @property
    def constants(self):
        return (self.a, self.f, self.e, self.e2, self.n)



WGS84 = Datum(name="WGS84")

GDA20 = Datum(name="GDA20")

AGD66 = Datum(name="AGD66")

