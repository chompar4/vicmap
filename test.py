from vicmap import MGA94, MGAPoint, GeoPoint, GDA94

# nsw_pt = MGAPoint(zone=56, E=250000, N=5600000, grid=MGA94)
# mgrs_pt = MGRSPoint(zone=56, gzd='J', usi='WN', x='45600', y='345634')

pt = MGAPoint.from_brennan('537885', 'Mount Wilson')
dLat, dLng = pt.transform_to(pt.grid.datum)
print(dLat, dLng)