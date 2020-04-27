from convergence import gda20_convergence, gda20_grid_magnetic_angle
from declination.geomag import gda20_declination


def run_through_csv():

    x, y = float("-37.33192"), float("145.8669")
    new_conv = gda20_convergence(x, y)
    new_dec = gda20_declination(x, y)
    new_gma = gda20_grid_magnetic_angle(x, y)
    print("{}, {}, {}, {}".format("test", new_conv, new_dec, new_gma))


run_through_csv()
