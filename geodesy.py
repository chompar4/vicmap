from constants import coordinate_set, a, _f, false_easting, false_northing, central_scale_factor, zone_width, central_meridian


def geographic_to_grid():
    print('performing conversion using {}'.format(coordinate_set))

    # Step 1: Compute ellipsiodal constants

    f = 1/_f            # flattening 
    e2 = f * (2-f)      # e^2
    n = f / (2-f)       # n 

    # Step 2a: Compute powers of n 
    n2 = n ** 2
    n3 = n ** 3
    n4 = n ** 4
    n5 = n ** 5
    n6 = n ** 6 
    n7 = n ** 7
    n8 = n ** 8

    # Step 2b: Compute rectifying radius A 
    A = a / (1 + n) * (
        1 
        + (1/4) * n2 
        + (1/64) * n4
        + (1/256) * n6 
        + (25/ 16384) * n8
    )

    assert round(A, 7)  == 6367449.145771




if __name__ == "__main__":
    geographic_to_grid()