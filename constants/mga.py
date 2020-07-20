# MGA Definition
# --------------
# UTM projection from GDA datum

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
