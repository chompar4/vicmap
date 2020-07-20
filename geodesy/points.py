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
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid

    @property
    def E(self):
        return self.x

    @property
    def N(self):
        return self.y

    @property
    def coords(self):
        return (self.E, self.N)

    @property
    def point_scale_factor(self):
        # TODO
        pass

    @property
    def grid_convergence(self):
        # TODO
        pass


class UTMPoint(PlanePoint):
    def __init__(self, zone, E, N, grid="MGA"):
        super().__init__(x=E, y=N, grid=grid)
        self.zone = zone

    @property
    def coords(self):
        return (self.zone, self.E, self.N, self.grid)

