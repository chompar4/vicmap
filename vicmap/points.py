import math
from pyproj import CRS, Transformer
from vicmap.projections import lambert_conformal_conic, utm
from vicmap.datums import GDA94, WGS84, Datum
from vicmap.grids import VICGRID94, Grid, VICGRID, MGAGrid, MGRSGrid, MGRS, MGA20, MGA94
from datetime import date as datetime
from vicmap.utils import try_declination_import, ellipsoidal_distance
from math import radians, sqrt


class Point:
    def reproject(self, other_epsg):
        """
        Give me coordinates of this point in coordinate system 
        specified by an epsg code.
        """
        # TODO
        pass

    def transform_to(self, other):
        """
        Give the coordinates of this point in another coordinate system.
        """

        assert isinstance(other, Datum) or isinstance(
            other, Grid
        ), "please provide a valid destination datum or grid"

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

        if isinstance(other, MGRSGrid):
            E, N = new
            pt = MGRSPoint.from_mga(zone=zone, E=E, N=N)
            return pt.display_coords

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

        assert -90 < dLat < 90, f"invalid latitude: {dLat}"
        assert -180 < dLng < 180, f"invalid longitude: {dLng}"

        self.dLat = dLat
        self.dLng = dLng
        self.datum = datum

    @property
    def rLat(self):
        return radians(self.dLat)

    @property
    def rLng(self):
        return radians(self.dLng)

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

    def distance_to(self, other):
        """
        Vincenty's inverse formula along an ellipsoidal geodesic 
        accepts: 
            - other : instance of GeoPoint
        returns 
            - s : ellipsoidal arc distance (meters)
        """

        assert isinstance(other, GeoPoint), f"please provide a GeoPoint"

        φ1, λ1 = self.rLat, self.rLng
        if other.datum.ellipsoid != self.datum.ellipsoid:
            """ geodesics depend on base ellipsoid, transform if required """
            φ2, λ2 = other.transform_to(self.datum)
        else:
            φ2, λ2 = other.rLat, other.rLng

        """ exit early if same point """
        if sqrt((φ1 - φ2) ** 2 + (λ1 - λ2) ** 2) < 1e-8:
            return 0

        a, b, f, _, _, _ = self.datum.ellipsoid.constants
        return ellipsoidal_distance(φ1, λ1, φ2, λ2, a, b, f)

    def __eq__(self, other):
        return self.datum == other.datum and self.display_coords == other.display_coords

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

    def __eq__(self, other):
        return self.grid == other.grid and self.display_coords == other.display_coords


class VICPoint(PlanePoint):
    def __init__(self, E, N, grid):

        assert grid in [VICGRID, VICGRID94], f"invalid grid: {grid.code}"
        assert 2.1e6 <= E <= 3e6, f"easting out of bounds: {E}"
        d = 2e6 if grid == VICGRID else 0
        assert 2.2e6 + d <= N <= 2.9e6 + d, f"northing out of bounds: {N}"

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

    def __repr__(self):
        return f"<VicPt_({self.E},{self.N})_{self.grid.code}>"


class MGAPoint(PlanePoint):
    def __init__(self, zone, E, N, grid):

        assert 200000 <= E <= 800000, f"invalid easting: {E}"
        assert 5600000 <= N <= 6300000, f"invalid northing: {N}"
        assert zone in [54, 55], f"invalid zone: {zone}"
        assert grid in [MGA20, MGA94, MGRS], f"invalid MGA grid: {grid.code}"

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

    def __repr__(self):
        return f"<MGAPt_({self.E},{self.N})_{self.grid.code}>"


class MGRSPoint(MGAPoint):

    grid = MGRS

    def __init__(self, zone, usi, x, y, precision=5):
        """
        MGRS : MGA with a 100k square alpha identifier (usi)
        accepts:
            precision:
                0 fig = 100k
                1 fig = 10k
                2 fig = 1k
                3 fig = 100m
                4 fig = 10m
                5 fig = 1m
        """

        assert 1 <= precision <= 5, f"invalid MGRS precision: {precision}"
        assert zone in [54, 55], f"invalid MGRS zone: {zone}"
        colName, rowName = usi[0].capitalize(), usi[1].capitalize()
        assert isinstance(usi, str) and len(usi) == 2, f"invalid MGRS usi: {usi}"
        col = colName in self.grid.cols54 if zone == 54 else colName in self.grid.cols55
        row = rowName in self.grid.rows54 if zone == 54 else rowName in self.grid.rows55
        assert col, f"usi column entry: {usi[0]} not found in zone: {zone}"
        assert row, f"usi row entry: {usi[1]} not found in zone: {zone}"
        assert 0 <= float(x) <= 10 ** precision, f"invalid MGRS x: {x}"
        assert 0 <= float(y) <= 10 ** precision, f"invalid MGRS y: {y}"

        def get_E(grid, zn, usi, x):
            lb = grid.cols54[colName][0] if zn == 54 else grid.cols55[colName][0]
            return lb + float(x)

        def get_N(grid, zn, usi, y):
            lb = grid.rows54[rowName][0] if zn == 54 else grid.rows55[rowName][0]
            return lb + float(y)

        E = get_E(self.grid, zone, usi, x)
        N = get_N(self.grid, zone, usi, y)

        super().__init__(E=E, N=N, grid=self.grid, zone=zone)
        self.x = self.__class__.get_x(E, precision)
        self.y = self.__class__.get_y(N, precision)
        self.precision = precision
        self.usi = usi

    @classmethod
    def from_6FIG(cls, zone, usi, GR6):
        """
        Allow creation from 6 fig grid reference with a usi
        """
        assert (
            isinstance(GR6, str) and len(GR6) == 6
        ), f"please specify GR {GR6} as a 6 digit string"
        assert 0 <= float(GR6) <= 999999, f"invalid grid reference: {GR6}"

        pt = cls(zone=zone, usi=usi, x=GR6[0:3] + "00", y=GR6[3:6] + "00", precision=5)
        return pt

    @classmethod
    def from_mga(cls, zone, E, N, precision=5):
        """
        Allow user to create from mga coords
        """

        assert 200000 <= E <= 800000, f"invalid easting: {E}"
        assert 5600000 <= N <= 6300000, f"invalid northing: {N}"
        assert zone in [54, 55], f"invalid zone: {zone}"
        assert 1 <= precision <= 5, f"invalid MGRS precision: {precision}"

        x = cls.get_x(E, precision)
        y = cls.get_y(N, precision)
        usi = cls.get_usi(grid=cls.grid, zone=zone, E=E, N=N)
        pt = cls(zone=zone, usi=usi, x=x, y=y, precision=precision)
        return pt

    @classmethod
    def get_usi(cls, grid, zone, E, N):
        cols = grid.cols54 if zone == 54 else grid.cols55
        rows = grid.rows54 if zone == 54 else grid.rows55
        X = next(code for code, (lb, ub) in cols.items() if lb <= E < ub)
        Y = next(code for code, (lb, ub) in rows.items() if lb <= N < ub)
        return f"{X}{Y}"

    @classmethod
    def get_x(cls, E, precision):
        """ strip the first digit off the MGA easting """
        val = round(E)
        start, end = 1, min(1 + precision, 6)
        return f"{val}"[start:end]

    @classmethod
    def get_y(cls, N, precision):
        """ strip the first two digits off the MGA northing """
        val = round(N)
        start, end = 2, min(2 + precision, 7)
        return f"{val}"[start:end]

    @property
    def display_coords(self):
        return (self.zone, self.usi, self.x, self.y)

    def __repr__(self):
        return (
            f"<MGRSPt_({self.zone}, {self.usi}, {self.x}, {self.y})_{self.grid.code}>"
        )
