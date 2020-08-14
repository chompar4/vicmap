from utils import dms_to_dd
import math
from pyproj import CRS, Transformer
from projections import lambert_conformal_conic
from geodesy.datums import GDA94, WGS84
from geodesy.grids import VICGRID94, MGAGrid


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
        dest = self.grid.datum
        (λ, φ) = self.transform_to(other=dest)
        _, _, _, γ = lambert_conformal_conic(λ, φ, dest.ellipsoid, self.grid)
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
    def grid_convergence(self, datum):
        # TODO
        pass

    @property
    def magnetic_declination(self, datum):
        # TODO
        pass

    @property
    def grid_magnetic_angle(self, datum):
        # TODO
        pass

    def __eq__(self, other):
        return self.grid == other.grid and self.coords == other.coords
