from vicmap import MGA94, MGAPoint, MGRSPoint

nsw_pt = MGAPoint(zone=56, E=250000, N=5600000, grid=MGA94)
mgrs_pt = MGRSPoint(zone=56, gzd='J', usi='WN', x='45600', y='345634')
print(nsw_pt)
print(mgrs_pt)
