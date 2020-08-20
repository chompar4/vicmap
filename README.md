# Vicmap
Tools for working with common victorian map projections

## Installation
```
poetry install
```

Install the latest release of ```geomag``` from source at the following link if you need to run geomagnetic calculations.
```
https://github.com/chompar4/geomag_api
```

## Specifying Points

Points on ellipsoidal geoid surfaces are represented by ```GeoPoints```, while points in the 2d map plane are represented by the ```PlanePoints```. Each point requires a set of coordinates, and a datum or grid.

Class | Coordinates | Description
------|-------------|------------
```GeoPoint()```    |  (φ, λ)  | decimal geographic latitude and longitude on geoid
```MGAPoint()```  |    (E, N)   |    easting and northing meters in a Map Grid of Australia plane
```VICPoint()``` | (E, N) | easting and northing in meters in a VICGRID plane

To define a point, specify the coordinates and the datum/grid.
```python
geo_pt = GeoPoint(φ=-37, λ=145, datum=GDA20)
mga_pt = MGAPoint(zone=54, E=250,000, N=5,600,000, grid=MGA94)
```

## Declination / Grid Magnetic Angles
Every instance of a point class can evaluate the grid convergence, magnetic declination and grid magnetic angle of it's position.

```python
sf = 10,000
pt = MGAPoint(zone=54, E=24 * sf, N= 250 * sf, grid=MGA20)
print(pt.declination, pt.grid_convergence, pt.grid_magnetic_angle)
```

## Projections

Functions for performing forward transformations can be found in the ```vicmap.projections``` module. The following projections are relevant for victoria: 

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


```pyproj``` is used for reverse (inverse) transformations.
