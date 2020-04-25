import csv

from convergence import gda20_convergence
from declination.geomag import gda20_declination


def run_through_csv():

    with open("Canyon_regions.csv") as csvfile:
        reader = csv.reader(csvfile)

        for X, Y, region, _ in reader:
            if X != "X":
                x, y = float(Y), float(X)  # TODO: fix me
                conv = gda20_convergence(x, y)
                dec = gda20_declination(x, y)
                print(region, conv, dec, dec - conv)


run_through_csv()
