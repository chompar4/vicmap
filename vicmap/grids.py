import math

from pyproj import CRS

from vicmap.datums import AGD66, GDA20, GDA94


class Grid:
    pass


class MGAGrid(Grid):

    base_code = 283  # epsg

    def __init__(self):
        """
        Representation of the MGA (Map Grid of Australia) plane.
        A specific UTM grid in the plane defined for australia.
        Origin Datum
            GDA94 / GDA20 only
        accepts
            E0: false easting (m)
            N0: false northing (m)
            m0: central scale factor
            zw: zone width (degrees longitude)
            cm1: central meridians of zone 1
        computes
            zones: all zones in the UTM grid
            z0_edge: longitude of western edge of the 0th zone
        """
        self.E0 = 500000
        self.N0 = 10000000
        self.m0 = 0.9996
        self.zw = 6
        self.cm1 = -177

    def epsg_code(self, zone):
        """
        MGA has a different epsg code for each zone,
        following the pattern: `283{z}`
        where z is the zone of projection.
        """
        return int(f"{self.base_code}{zone}")

    def crs(self, zone):
        return CRS.from_epsg(self.epsg_code(zone))

    @property
    def cms(self):
        """
        gives a dictionary of central meridians for each MGA zone
        """
        cms = {}
        idx = 1
        cm = self.cm1
        while cm < 180:
            cms[idx] = cm
            cm += self.zw
            idx += 1
        return cms

    @property
    def z0_edge(self):
        return self.cms[1] - 1.5 * self.zw

    def get_zone(self, dLng):
        """
        gives the MGA zone containing dLng
        """
        return math.floor((dLng - self.z0_edge) / self.zw)

    def get_cm(self, zn):
        return self.cms[zn]


class MGAGrid20(MGAGrid):
    datum = GDA20
    name = "Map Grid of Australia (2020)"
    code = "MGA20"


class MGAGrid94(MGAGrid):
    datum = GDA94
    name = "Map Grid of Australia (1994)"
    code = "MGA94"


class MGRSGrid(MGAGrid20):
    """
    Columns:
    Near the equator, the columns of UTM zone 1 have the letters A–H,
    the columns of UTM zone 2 have the letters J–R (omitting O),
    and the columns of UTM zone 3 have the letters S–Z.
    At zone 4, the column letters start over from A, and so on around
    the world.
    """

    name = "Military Grid Reference System (MGA20)"
    code = "MGRS"

    """
    The intersection of a UTM zone and a latitude band is (normally) a
    6° × 8° polygon called a grid zone, whose designation in MGRS is
    formed by the zone number followed by the latitude band letter (uppercase).
    """

    latitude_bands = {
        "G": [-48, -40],
        "H": [-40, -32],
        "J": [-32, -24],
        "K": [-24, -16],
        "L": [-16, 8]
    }

    # TODO: make me a nice function / expression. This is yuck. It repeats every 3 zones.

    sf = 1e5  # meters
    cols54 = {
        "S": [1 * sf, 2 * sf],
        "T": [2 * sf, 3 * sf],
        "U": [3 * sf, 4 * sf],
        "V": [4 * sf, 5 * sf],
        "W": [5 * sf, 6 * sf],
        "X": [6 * sf, 7 * sf],
        "Y": [7 * sf, 8 * sf],
        "Z": [8 * sf, 9 * sf],
    }

    cols55 = {
        "A": [1 * sf, 2 * sf],
        "B": [2 * sf, 3 * sf],
        "C": [3 * sf, 4 * sf],
        "D": [4 * sf, 5 * sf],
        "E": [5 * sf, 6 * sf],
        "F": [6 * sf, 7 * sf],
        "G": [7 * sf, 8 * sf],
        "H": [8 * sf, 9 * sf],
    }

    cols56 = {
        "J": [1 * sf, 2 * sf],
        "K": [2 * sf, 3 * sf],
        "L": [3 * sf, 4 * sf],
        "M": [4 * sf, 5 * sf],
        "N": [5 * sf, 6 * sf],
        "P": [6 * sf, 7 * sf],
        "Q": [7 * sf, 8 * sf],
        "R": [8 * sf, 9 * sf],
    }

    columns = [cols54, cols55, cols56]
    assert all('I' not in r for r in columns), '`I` should not be an MGRS column name'
    assert all('O' not in r for r in columns), '`O` should not be an MGRS column name'
    assert all(len(r.keys()) == 8 for r in columns), 'all mgrs cols must have 8 entries'

    """
    In the AA scheme,[2] also known as MGRS-New,
    [3] which is used for WGS84 and some other modern geodetic datums,
    the letter for the first row – just north of the equator – is A in
    odd-numbered zones, and F in even-numbered zones, as shown in figure 1.

    NOTE: both the even & odd rows here will repeat, but we only care about
    VIC/NSW. TODO: handle repeating.
    """

    even_rows = {
        "A": [55 * sf, 56 * sf],
        "B": [56 * sf, 57 * sf],
        "C": [57 * sf, 58 * sf],
        "D": [58 * sf, 59 * sf],
        "E": [59 * sf, 60 * sf],
        "F": [60 * sf, 61 * sf],
        "G": [61 * sf, 62 * sf],
        "H": [62 * sf, 63 * sf],
        "J": [63 * sf, 64 * sf],
        "K": [64 * sf, 65 * sf],
        "L": [65 * sf, 66 * sf],
        "M": [66 * sf, 67 * sf],
        "N": [67 * sf, 68 * sf],
        "P": [68 * sf, 69 * sf],
        "Q": [69 * sf, 70 * sf],
        "R": [70 * sf, 71 * sf],
        "S": [71 * sf, 72 * sf],
        "T": [72 * sf, 73 * sf],
        "U": [73 * sf, 74 * sf],
        "V": [74 * sf, 75 * sf],
    }

    odd_rows = {
        "R": [55 * sf, 56 * sf],
        "S": [56 * sf, 57 * sf],
        "T": [57 * sf, 58 * sf],
        "U": [58 * sf, 59 * sf],
        "V": [59 * sf, 60 * sf],
        "A": [60 * sf, 61 * sf],
        "B": [61 * sf, 62 * sf],
        "C": [61 * sf, 62 * sf],
        "D": [62 * sf, 63 * sf],
        "E": [63 * sf, 64 * sf],
        "F": [64 * sf, 65 * sf],
        "G": [65 * sf, 66 * sf],
        "H": [66 * sf, 67 * sf],
        "J": [67 * sf, 68 * sf],
        "K": [68 * sf, 69 * sf],
        "L": [69 * sf, 70 * sf],
        "M": [70 * sf, 71 * sf],
        "N": [71 * sf, 72 * sf],
        "P": [72 * sf, 73 * sf],
        "Q": [73 * sf, 74 * sf]
    }

    assert all('I' not in r for r in even_rows), '`I` should not be an MGRS row name'
    assert all('I' not in r for r in odd_rows), '`I` should not be an MGRS row name'
    assert all('O' not in r for r in even_rows), '`O` should not be an MGRS row name'
    assert all('O' not in r for r in even_rows), '`O` should not be an MGRS row name'

    def getrows(self, zone_num):
        """
        Rows change depending on the UTM zone.
        """
        if zone_num % 2 == 0:
            return self.even_rows
        return self.odd_rows

    def get_latitude_band(self, dLat):
        band = next((k for k, (lb, ub) in self.latitude_bands.items() if lb <= dLat <= ub), None)
        assert band, f'Could not find a latitude band in AUS for {dLat}'
        return band


class VICGRID(Grid):

    datum = AGD66
    epsg_code = 3110
    code = "VICGRID"

    def __init__(self):
        """
        Representation of the VICGRID plane.
        Contains all constants required for projection.
        Origin Datum
            AGD66
        accepts
            φ1, φ2: standard parralels
            E0: false easting (m)
            N0: false northing (m)
            φ0: origin parrallel latitude (degrees)
            λ0: central meridian longitude (degrees)
        """
        self.E0 = 2500000
        self.N0 = 4500000
        self.φ1 = -36
        self.φ2 = -38
        self.λ0 = 145
        self.φ0 = -37
        self.r0 = 8472630.5

    @property
    def crs(self):
        return CRS.from_epsg(self.epsg_code)

    @property
    def constants(self):
        return (self.φ1, self.φ2, self.λ0, self.φ0, self.E0, self.N0)


class VICGRID94(VICGRID):

    datum = GDA94
    epsg_code = 3111
    code = "VICGRID94"

    def __init__(self):
        """
        Representation of the VICGRID94 plane.
        Identical to VICGRID with a different false northing.
        Contains all constants required for projection.
        Origin Datum
            GDA94
        accepts
            φ1, φ2: standard parralels
            E0: false easting (m)
            N0: false northing (m)
            φ0: origin parrallel latitude (degrees)
            λ0: central meridian longitude (degrees)
        """
        self.E0 = 2500000
        self.N0 = 2500000
        self.φ1 = -36
        self.φ2 = -38
        self.λ0 = 145
        self.φ0 = -37
        self.r0 = 8472630.5




MGA94 = MGAGrid94()
MGA20 = MGAGrid20()
VICGRID = VICGRID()
VICGRID94 = VICGRID94()
MGRS = MGRSGrid()

__all_grids__ = [MGA94, MGA20, VICGRID, VICGRID94, MGRS]
