from vicmap import MGA94, MGAPoint, GeoPoint, GDA94

# nsw_pt = MGAPoint(zone=56, E=250000, N=5600000, grid=MGA94)
# mgrs_pt = MGRSPoint(zone=56, gzd='J', usi='WN', x='45600', y='345634')

# center of the map
geo_pt = GeoPoint(dLat=-29.25, dLng=142.25)

# these maps span MRGS squares, so there are potentially two squares on this map.
# which one is the 6 FIG GR relative to? There will only be one answer, but how
# do we work it out? Check surrounding squares and work out which is closest to centre.

zn, E, N = geo_pt.transform_to(MGA94)
centre_point = MGAPoint(zone=zn, E=E, N=N, grid=MGA94)

# take the GR6 and
GR6 = '991885'
gr_east = float(GR6[:3]) * 1e2
gr_north = float(GR6[3:]) * 1e2

# round easting & northing to start of the square for centre point
E1 = E - E % 1e5 + gr_east
N1 = N - N % 1e5 + gr_north

# work out coords in all surrounding mgrs squares
this = MGAPoint(zone=zn, E=E1, N=N1, grid=MGA94)
left = MGAPoint(zone=zn, E=E1 - 1e5, N=N1, grid=MGA94)
right = MGAPoint(zone=zn, E=E1 + 1e5, N=N1, grid=MGA94)
up = MGAPoint(zone=zn, E=E1, N=N1 + 1e5, grid=MGA94)
down = MGAPoint(zone=zn, E=E1, N=N1 - 1e5, grid=MGA94)
left_up = MGAPoint(zone=zn, E=E1 - 1e5, N=N1 + 1e5, grid=MGA94)
right_up = MGAPoint(zone=zn, E=E1 + 1e5, N=N1 + 1e5, grid=MGA94)
left_down = MGAPoint(zone=zn, E=E1 - 1e5, N=N1 - 1e5, grid=MGA94)
right_down = MGAPoint(zone=zn, E=E1 + 1e5, N=N1 - 1e5, grid=MGA94)

shortest = 9e9
point = None
for potential_pt in (left, right, up, down, left_up, left_down, right_up, right_down):
    distance = potential_pt.distance_to(centre_point)
    if distance < shortest:
        shortest = distance
        point = potential_pt

out_pt = point.transform_to(GDA94)
print(out_pt)