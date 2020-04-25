import csv

from convergence import gda20_convergence, gda20_grid_magnetic_angle
from declination.geomag import gda20_declination


def run_through_csv():

    with open("canyons.csv") as csvfile:
        reader = csv.reader(csvfile)

        for c, g, i, s, _, _1, _2, _3, lat, lng, conv, decl, gma in reader:
            if c != "Canyon" and lat and lng:
                x, y = float(lat), float(lng)
                new_conv = gda20_convergence(x, y)
                new_dec = gda20_declination(x, y)
                new_gma = gda20_grid_magnetic_angle(x, y)
                print("{}, {}, {}, {}".format(c, new_conv, new_dec, new_gma))


run_through_csv()
