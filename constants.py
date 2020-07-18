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
E0 = 500000

# False northing (m)
N0 = 10000000

# Central Scale factor (m0)
m0 = 0.9996

# Zone width (degrees)
zone_width = 6

# in defined coords
a = semi_major_axis[coordinate_set]
_f = inverse_flattening[coordinate_set]


# GDA / MGA Zones 
# ---------------

# Longitude of the central meridian of zone 1 (degrees)
cm_zone1 = -177 # (-180, 180)

# Longitude of western edge of zone zero
zone0_edge = cm_zone1 - (1.5*zone_width)

# Central meridian of zone zero
cm_zone0 = cm_zone1 + zone_width / 2

# Central meridian longitude of MGA zones
cm_mga_zone = {
    49: 111, 
    50: 117, 
    51: 123, 
    52: 129, 
    53: 135, 
    54: 141, 
    55: 147, 
    56: 153
}  