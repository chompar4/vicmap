from utils import dms_to_dd


class GeoPoint:
    def __init__(self, dLat, dLng, datum):
        self.dLat = dLat
        self.dLng = dLng
        self.datum = datum

    @property
    def crs(self):
        return self.datum.reference_frame


class PlanePoint:
    def __init__(self, u, v, grid):
        self.u = u
        self.v = v
        self.grid = grid

    @property
    def point_scale_factor(self):
        raise NotImplementedError

    @property
    def grid_convergence(self):
        raise NotImplementedError

    @property
    def E(self):
        return self.u

    @property
    def N(self):
        return self.v


class VICPoint(PlanePoint):
    def __init__(self, E, N, grid):
        super().__init__(u=E, v=N, grid=grid)

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


class UTMPoint(PlanePoint):
    def __init__(self, zone, E, N, grid):
        super().__init__(u=E, v=N, grid=grid)
        self.zone = zone

    @property
    def coords(self):
        return (self.zone, self.E, self.N)

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
