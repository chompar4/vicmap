# Ellipsoid definition
# --------------------

# Semi major axis (a) meters
semi_major_axis = {
    "WGS84": 6378137,
    "GDA20": 6378137, 
    "GDA94": 6378137,
    "AGD66": 6378160,
    "ANG": 6378350.871924
}

# Semi minor axis (b) meters
semi_minor_axis = {
    "WGS84": None,
    "GDA20": None,
    "GDA94": None,
    "AGD66": None,
    "ANG": None,
}

# Inverse flattening (1/f)
inverse_flattening = {
    "WGS84": 298.257223563,
    "GDA20": 298.257222101, 
    "GDA94": 298.257222101,
    "AGD66": 298.25, 
    "ANG": 294.26
}


# MGA Definition
# --------------
# UTM projection

MGA_datum = "GDA20"

# False easting (m)
E0 = 500000

# False northing (m)
N0 = 10000000

# Central Scale factor (m0)
m0 = 0.9996

# Zone width (degrees)
zone_width = 6

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


# VICGRID94 Definition 
# --------------------
# Lambert conformal conic projection

datum_vicgrid94 = "AGD66"

# standard parrallels 36°S & 38°S
φ1 = -36
φ2 = -38

# Central meridian - 145°E
cm_vicgrid94 = 145

# The origin of VICGRID coordinates is 2,500,000 metres west and
# 2,500,000 metres south of the intersection of the parallel of
# latitude 37°S and the central meridian.
 
# reference longitude - 2,500km west of (37°S, 145°E)
λ0 = 116.72
# λ0 = 0

# reference latitude - 2,500km south of (37°S, 145°E)
φ0 = -59.5
# φ0 = 0

