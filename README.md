# Vicmap
[![Build status](https://badge.buildkite.com/82cfc45a6dfec63cdf429b9e2b2037fe2416b3729d1db9aa94.svg)](https://buildkite.com/thompsonfilm/vicmap)

Python tools for working with common victorian (+ nsw) map projections

## Installation

```
poetry install
```

## Specifying Points

Points on ellipsoidal surfaces are represented by `GeoPoint` instances and points in the 2d x-y plane are represented by the `PlanePoint` instances. Each type of point requires a set of coordinates, and a datum or grid respectively. `GeoPoint` and `PlanePoint` objects are defined on topologically distinct surfaces and so require a forward or inverse point projection to transform one to the other.

| Class         | Coordinates    | Description                                                                                       |
| ------------- | -------------- | ------------------------------------------------------------------------------------------------- |
| `GeoPoint()`  | (φ, λ)         | decimal geographic latitude and longitude on geoid                                                |
| `MGAPoint()`  | (z, E, N)      | z: grid zone designator, easting and northing meters in a Map Grid of Australia plane             |
| `VICPoint()`  | (E, N)         | easting and northing in meters in a VICGRID plane                                                 |
| `MGRSPoint()` | (z, usi, x, y) | z: grid zone designator, usi: the 100,000-meter square identifier, easting and northing in meters |

To define a point, specify the coordinates and the datum/grid.

```python
geo_pt = GeoPoint(φ=-37, λ=145, datum=GDA20)
mga_pt = MGAPoint(zone=54, lat_band='H', E=250,000, N=5,600,000, grid=MGA94)
```

or use some of the provided utils to specify points from common reference systems. 
(e.g a 6 figure GR)

```python
pt = MGRSPoint.from_6FIG(55, "H", "fu", "275882")
pt.transform_to(WGS84)
```

## Geodesic Distance
Use the ```distance_to``` method on ```GeoPoint``` instances to compute geodesic distance across the surface of the reference ellipsoid. This method handles different datums by projecting to a common ellipsoid.
```python
p1 = GeoPoint(dLat=-37.95103342, dLng=144.4248679, datum=GDA20)
p2 = GeoPoint(dLat=-37.65282114, dLng=143.9264955, datum=GDA94)
p1.distance_to(p2) 
>>> 54972.274
```

## Grid Distance
Use the ```distance_to``` method on a ```PlanePoint``` to compute grid distances.

## Declination / Grid Magnetic Angles

Every instance of a point class can evaluate the grid convergence, magnetic declination and grid magnetic angle of it's position.

Install the latest release of `isogonic-api` from source at the following link if you need to run geomagnetic calculations. This is not required to use the rest of the functionality.

```
https://github.com/chompar4/isogonic-api
```

```python
sf = 10,000
pt = MGAPoint(zone=54, lat_band='H', E=24 * sf, N= 250 * sf, grid=MGA20)
print(pt.declination, pt.grid_convergence, pt.grid_magnetic_angle)
```

# NSW Topo Maps
The relevant data for these maps can be grabbed by running
```
https://portal.spatial.nsw.gov.au/server/rest/services/Hosted/Topo_Map_Index/FeatureServer/0/query?text=&geometry&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=&where=objectid%3E-1&time=&returnCountOnly=false&returnIdsOnly=false&returnGeometry=false&maxAllowableOffset=&outSR=&outFields=mapnumber%2Cmapname%2Cmapseries%2Cadjmapindexx%2Clabel%2Cadjmapindexy&f=pjson
```

## Brennan Coordinates
MGA Points can handle creation using the Brennan system of describing coordinates (see https://ozultimate.com/canyoning/track_notes/du_faur_creek.htm). These consist of a 6 Figure MGA Grid Reference and a Map Sheet Number (e.g '8930-1N' or 'Mount Wilson').
Only MGA coordinates are currently supported in this method. The following example gives the decimal coordinates of the start of Pipeline Canyon.

```
pt = MGAPoint.from_brennan('452278', '8931-1S')
dLat, dLng = pt.transform_to(pt.grid.datum)
```

#### CI 
Run buildkite agent using ```buildkite-agent start```
