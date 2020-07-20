from math import sqrt, sin
from constants.ellipsoid import semi_major_axis, inverse_flattening

class Datum:
    def __init__(self, name):
        """
        creates a geodetic datum from paramaters
            a: equatorial radius (semi-major axis)
            b: polar radius (semi-minor axis)
            _f: inverse flattening 1/f
        """

        self.a = semi_major_axis[name]
        self._f = inverse_flattening[name]
        self.name = name

    @property
    def b(self):
        "b; semi minor acis length (meters)"
        return self.a / (1 - self.f)

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
        return (self.a, self.b, self.f, self.e, self.e2, self.n)

    @property
    def distance(self, point1, point2):
        '''
        From: geo-py package, which explodes on build currently
        Calculating distance with using vincenty's formula
        https://en.wikipedia.org/wiki/Vincenty's_formulae
        '''

        CONVERGENCE_THRESHOLD = 1e-12
        MAX_ITERATIONS = 15

        lon1, lat1 = (radians(coord) for coord in point1)
        lon2, lat2 = (radians(coord) for coord in point2)

        U1 = atan((1 - self.f) * tan(lat1))
        U2 = atan((1 - self.f) * tan(lat2))
        L = lon2 - lon1
        Lambda = L

        sinU1 = sin(U1)
        cosU1 = cos(U1)
        sinU2 = sin(U2)
        cosU2 = cos(U2)

        for _ in range(MAX_ITERATIONS):
            sinLambda = sin(Lambda)
            cosLambda = cos(Lambda)
            sinSigma = sqrt(
                (cosU2 * sinLambda) ** 2 +
                (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
            # coincident points
            if sinSigma == 0:
                return 0.0

            cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
            sigma = atan2(sinSigma, cosSigma)
            sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
            cosSqAlpha = 1 - sinAlpha ** 2
            try:
                cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
            except ZeroDivisionError:
                cos2SigmaM = 0

            C = (self.f / 16) * cosSqAlpha * (
                4 + self.f * (4 - 3 * cosSqAlpha)
            )
            LambdaPrev = Lambda
            Lambda = (
                L + (1 - C) * self.f * sinAlpha * (
                    sigma + C * sinSigma * (
                        cos2SigmaM + C * cosSigma * (
                            -1 + 2 * cos2SigmaM ** 2
                        )
                    )
                )
            )

            if abs(Lambda - LambdaPrev) < CONVERGENCE_THRESHOLD:
                break
        else:
            # failure to converge
            return None

        uSq = cosSqAlpha * (self.a ** 2 - self.b ** 2) / (self.b ** 2)
        A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
        B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
        deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma *
                    (-1 + 2 * cos2SigmaM ** 2) - B / 6 * cos2SigmaM *
                    (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2)))
        s = self.b * A * (sigma - deltaSigma)
        return s


WGS84 = Datum(name="WGS84")
GDA20 = Datum(name="GDA20")
GDA94 = Datum(name="GDA94")
AGD66 = Datum(name="AGD66")

