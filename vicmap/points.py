import math
from pyproj import CRS, Transformer
from vicmap.projections import lambert_conformal_conic, utm
from vicmap.datums import GDA94, WGS84
from vicmap.grids import VICGRID94, MGAGrid
from geomag import declination
from datetime import date as datetime


class Point:
    def transform_to(self, other):
        """
        Transform between one point and another.
        """
        if isinstance(other, MGAGrid):
            # dont always know what MGA zone I'm in, project to wgs first
            to_wgs = Transformer.from_crs(self.crs, WGS84.crs)
            dLat, dLng = to_wgs.transform(*self.coords)

            zone = other.get_zone(dLng)
            other_crs = other.crs(zone)

        else:
            other_crs = other.crs

        if other_crs == self.crs:
            return self.coords
        transformer = Transformer.from_crs(self.crs, other_crs)
        return transformer.transform(*self.coords)

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
    def coords(self):
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
        self.u = u
        self.v = v
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
        (φ, λ) = self.invert()
        z = 0  # TODO: compute height using AHD/DTM
        date = datetime.today()
        return declination(φ, λ, z, date)

    @property
    def E(self):
        return self.u

    @property
    def N(self):
        return self.v

    @property
    def coords(self):
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
        return self.grid == other.grid and self.coords == other.coords

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
    def coords(self):
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
        return self.grid == other.grid and self.coords == other.coords

    def __repr__(self):
        return f"<MGAPt_({self.E},{self.N})_{self.grid.code}>"
