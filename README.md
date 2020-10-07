# Vicmap
[![Build status](https://badge.buildkite.com/82cfc45a6dfec63cdf429b9e2b2037fe2416b3729d1db9aa94.svg)](https://buildkite.com/thompsonfilm/vicmap)

Python tools for working with common victorian map projections

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
mga_pt = MGAPoint(zone=54, E=250,000, N=5,600,000, grid=MGA94)
```

or use some of the provided utils to specify points from common reference systems. 
(e.g a 6 figure GR)

```python
pt = MGRSPoint.from_6FIG(55, "fu", "275882")
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
pt = MGAPoint(zone=54, E=24 * sf, N= 250 * sf, grid=MGA20)
print(pt.declination, pt.grid_convergence, pt.grid_magnetic_angle)
```

## Projections

Functions for performing forward transformations can be found in the `vicmap.projections` module. The following projections are relevant for victoria:

#### Lambert Conformal Conic

```python
E, N, m, γ = lambert_conformal_conic(φ, λ, ellipsoidal_constants, grid_constants)
```

```
Accepts:
    φ: latitude in decimal degrees (-90, 90]
    λ: longitude in decimal degrees (-180, 180]
    ellipsoidal constants: (cm, a, b, 1/f, e, e2, n)
    grid constants: (λ0, φ0, E0, N0 φ1, φ2)
returns:
    X: easting (m)
    Y: northing (m)
    m: point scale factor
    γ: grid convergence
```

#### Universal Transverse Mercator (UTM)

```python
E, N, m, γ = utm(φ, λ, cm, ellipsoidal_constants, grid_constants)
```

```
Accepts:
    φ: latitude in decimal degrees (-90, 90]
    λ: longitude in decimal degrees (-180, 180]
    cm: central meridian of zone containing (dLat, dLng)
    ellipsoidal constants: (cm, a, b, 1/f, e, e2, n)
    grid constants: (m0, E0, N0)
returns:
    z: zone
    E: UTM easting (m)
    N: UTM northing (m)
    m: point scale factor
    γ: grid convergence
```

`pyproj` is used for reverse (inverse) transformations.

#### CI 
Run buildkite agent using ```buildkite-agent start```
