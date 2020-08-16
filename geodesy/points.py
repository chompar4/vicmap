import math
from pyproj import CRS, Transformer
from geodesy.projections import lambert_conformal_conic, utm
from geodesy.datums import GDA94, WGS84
from geodesy.grids import VICGRID94, MGAGrid
from geomag import declination


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


class GeoPoint(Point):
    def __init__(self, dLat, dLng, datum):
        self.dLat = dLat
        self.dLng = dLng
        self.datum = datum

    @property
    def coords(self):
        return (self.dLat, self.dLng)

    @property
    def crs(self):
        return self.datum.crs


class PlanePoint(Point):
    def __init__(self, u, v, grid):
        self.u = u
        self.v = v
        self.grid = grid
        self.datum = grid.datum

        self.λ = None
        self.φ = None

    def invert(self):
        if not self.λ or self.φ:
            self.λ, self.φ = self.transform_to(other=self.datum)
        return (self.λ, self.φ)

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
        (λ, φ) = self.invert()
        _, _, _, γ = lambert_conformal_conic(λ, φ, self.datum.ellipsoid, self.grid)
        return γ

    @property
    def magnetic_declination(self, datum):
        # TODO
        raise NotImplementedError

    @property
    def grid_magnetic_angle(self, datum):
        # TODO
        raise NotImplementedError

    def __eq__(self, other):
        return self.grid == other.grid and self.coords == other.coords


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
        (λ, φ) = self.invert()
        _, _, _, _, γ = utm(λ, φ, ellipsoid=self.datum.ellipsoid, grid=self.grid)
        return γ

    @property
    def magnetic_declination(self):
        return declination()

    @property
    def grid_magnetic_angle(self, datum):
        # TODO
        raise NotImplementedError

    def __eq__(self, other):
        return self.grid == other.grid and self.coords == other.coords
