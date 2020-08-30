import math
from pyproj import CRS, Transformer
from vicmap.projections import lambert_conformal_conic, utm
from vicmap.datums import GDA94, WGS84
from vicmap.grids import VICGRID94, MGAGrid
from datetime import date as datetime
from vicmap.utils import try_declination_import


class Point:
    def transform_to(self, other):
        """
        Transform between one point and another.
        """

        coords = self.proj_coords[-2:]

        if isinstance(other, MGAGrid):
            # dont what MGA zone other is in, project to wgs first
            to_wgs = Transformer.from_crs(self.crs, WGS84.crs)
            dLat, dLng = to_wgs.transform(*coords)

            zone = other.get_zone(dLng)
            other_crs = other.crs(zone)

        else:
            other_crs = other.crs
            zone = None

        if other_crs == self.crs:
            return self.proj_coords
        transformer = Transformer.from_crs(self.crs, other_crs)
        new = transformer.transform(*coords)
        return (zone, *new) if zone else new

    @property
    def grid_magnetic_angle(self):
        """
        The horizontal angle at a place between grid north 
        and magnetic north. Varies with location, time, grid.
        """

        # NOTE: decl is always East (+ve) in vic
        return self.magnetic_declination - self.grid_convergence


class GeoPoint(Point):
    def __init__(self, dLat, dLng, datum=WGS84):
        self.dLat = dLat
        self.dLng = dLng
        self.datum = datum

    @property
    def display_coords(self):
        return self.proj_coords

    @property
    def proj_coords(self):
        return (self.dLat, self.dLng)

    @property
    def crs(self):
        return self.datum.crs

    @property
    def magnetic_declination(self):
        """
        The horizontal angle at a place between true north and 
        magnetic north. Varies with location and time.
        """
        declination = try_declination_import()

        z = 0  # TODO: compute height using AHD/DTM
        date = datetime.today()
        return declination(self.dLat, self.dLng, z, date)

    @property
    def grid_convergence(self):
        """
        The horizontal angle at a place between true north and grid north. 
        Proportional to the longitude difference between the place and 
        the central meridian.
        returns 
            γ: grid convergence degrees, East >0, West <0
        """
        return 0

    def __repr__(self):
        return f"<GeoPt_({self.dLat},{self.dLng})_{self.datum.code}>"


class PlanePoint(Point):
    def __init__(self, u, v, grid):
        self.u = u - grid.E0
        self.v = v - grid.N0
        self.grid = grid
        self.datum = grid.datum

        self.φ = None
        self.λ = None

    def invert(self):
        """
        Transform a pair of u, v coords in the plane
        to a pair of (φ, λ) coords on the ellipsoid.
        """
        if not self.φ or self.λ:
            self.φ, self.λ = self.transform_to(other=self.datum)
        return (self.φ, self.λ)

    @property
    def magnetic_declination(self):
        """
        The horizontal angle at a place between true north and 
        magnetic north. Varies with location and time.
        """
        declination = try_declination_import()

        (φ, λ) = self.invert()
        z = 0  # TODO: compute height using AHD/DTM
        date = datetime.today()
        return declination(φ, λ, z, date)

    @property
    def E(self):
        return self.u + self.grid.E0

    @property
    def N(self):
        return self.v + self.grid.N0

    @property
    def display_coords(self):
        return self.proj_coords

    @property
    def proj_coords(self):
        return (self.E, self.N)


class VICPoint(PlanePoint):
    def __init__(self, E, N, grid):
        super().__init__(u=E, v=N, grid=grid)
        self.crs = CRS.from_epsg(grid.epsg_code)

    @property
    def grid_convergence(self):
        """
        The horizontal angle at a place between true north and grid north. 
        Proportional to the longitude difference between the place and 
        the central meridian.
        returns 
            γ: grid convergence degrees, East >0, West <0
        """
        (φ, λ) = self.invert()
        _, _, _, γ = lambert_conformal_conic(φ, λ, self.datum.ellipsoid, self.grid)
        return γ

    def __eq__(self, other):
        return self.grid == other.grid and self.display_coords == other.display_coords

    def __repr__(self):
        return f"<VicPt_({self.E},{self.N})_{self.grid.code}>"


class MGAPoint(PlanePoint):
    def __init__(self, zone, E, N, grid):
        super().__init__(u=E, v=N, grid=grid)
        self.zone = zone

    @property
    def crs(self):
        """
        MGA crs depends upon zone
        """
        return self.grid.crs(self.zone)

    @property
    def display_coords(self):
        return (self.zone, self.E, self.N)

    @property
    def proj_coords(self):
        return (self.E, self.N)

    @property
    def grid_convergence(self):
        """
        The horizontal angle at a place between true north and grid north. 
        Proportional to the longitude difference between the place and 
        the central meridian.
        returns 
            γ: grid convergence degrees, East >0, West <0
        """
        (φ, λ) = self.invert()
        _, _, _, _, γ = utm(φ, λ, ellipsoid=self.datum.ellipsoid, grid=self.grid)
        return γ

    def __eq__(self, other):
        return self.grid == other.grid and self.display_coords == other.display_coords

    def __repr__(self):
        return f"<MGAPt_({self.E},{self.N})_{self.grid.code}>"


class MGRSPoint(MGAPoint):

    """
    MGA point with a 100k square identifier (usi)
    """

    # TODO: make me a nice function / expression. This is yuck
    sf = 1e5
    cols54 = {
        "Y": [7 * sf, 8 * sf],
        "X": [6 * sf, 7 * sf],
        "W": [5 * sf, 6 * sf],
        "V": [4 * sf, 5 * sf],
    }

    rows54 = {
        "H": [62 * sf, 63 * sf],
        "G": [61 * sf, 62 * sf],
        "F": [60 * sf, 61 * sf],
        "E": [59 * sf, 60 * sf],
        "D": [58 * sf, 59 * sf],
        "C": [57 * sf, 58 * sf],
    }

    cols55 = {
        "B": [2 * sf, 3 * sf],
        "C": [3 * sf, 4 * sf],
        "D": [4 * sf, 5 * sf],
        "E": [5 * sf, 6 * sf],
        "F": [6 * sf, 7 * sf],
        "G": [7 * sf, 8 * sf],
    }

    rows55 = {
        "S": [56 * sf, 57 * sf],
        "T": [57 * sf, 58 * sf],
        "U": [58 * sf, 59 * sf],
        "V": [59 * sf, 60 * sf],
        "A": [60 * sf, 61 * sf],
        "B": [61 * sf, 62 * sf],
    }

    @property
    def usi(self):
        cols = self.cols54 if self.zone == 54 else self.cols55
        rows = self.rows54 if self.zone == 54 else self.rows55
        X = next(code for code, (lb, ub) in cols.items() if lb <= self.E < ub)
        Y = next(code for code, (lb, ub) in rows.items() if lb <= self.N < ub)
        return f"{X}{Y}"

    @property
    def x(self):
        """ strip the first digit off the MGA easting """
        val = round(self.E)
        start, end = 1, min(1 + self.precision, 6)
        return f"{val}"[start:end]

    @property
    def y(self):
        """ strip the first two digits off the MGA northing """
        val = round(self.N)
        start, end = 2, min(2 + self.precision, 7)
        return f"{val}"[start:end]

    @property
    def display_coords(self):
        return (self.zone, self.usi, self.x, self.y)

    @property
    def precision(self):
        """
        Precision of the specified coordinates only, 
        not the accuracy of the coordinates.
        5 fig = 1m, ..., 1 fig = 10k
        """
        return 5

    def __repr__(self):
        return (
            f"<MGRSPt_({self.zone}, {self.usi}, {self.x}, {self.y})_{self.grid.code}>"
        )

