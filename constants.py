# Choose the coord set
coordinate_set = "GDA20" # GDA2020/MGA2020


# Ellipsoid definition
# --------------------

# Semi major axis (a) (m)
semi_major_axis = {
    "GDA20": 6378137, 
    "GDA94": 6378137,
    "AGD": 6378160, 
    "ANG": 6378350.871924
}

# Inverse flattening (1/f)
inverse_flattening = {
    "GDA20": 298.257222101, 
    "GDA94": 298.257222101,
    "AGD": 298.25, 
    "ANG": 294.26
}


# Transverse Mercator Definition
# ------------------------------

# False easting (m)
false_easting = 500000

# False northing (m)
false_northing = 10000000

# Central Scale factor (K0)
central_scale_factor = 0.9996

# Zone width (degrees)
zone_width = 6

# Longitude of the central meridian of zone 1 (degrees)
central_meridian = -177
assert -180 < central_meridian <= 180, 'please specify central meridian in range (-180, 180]'

# in defined coords
a = semi_major_axis[coordinate_set]
_f = inverse_flattening[coordinate_set]