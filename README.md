# vicmap
python library of cartographic tools for projections and geodetic computations in victoria

## Installation
```
poetry install
```

## Points

Points on 3D Geoid surfaces are represented by ```GeoPoints```, while points in the 2d plane are represented by the ```PlanePoints```. Each point requires a set of coordinates, and a datum (or grid). Points have a default coordinate system, which you can transform between.

```
GeoPoint()   :    (dLat, dLng)  - decimal latitude and longitude in degrees (DEFAULT)
                  (x, y, z)     - cartesian coordinates in meters

PlanePoint() :    (E, N)        - easting and northing in meters (DEFAULT)
```

To define a point, specify the coordinates and the datum.
```python
pt = GeoPoint(dLat, dLng, datum=GDA20)
```

## Projections

### MGA20
Use ```geo_to_mga``` and ```mga_to_geo``` to perform forward or reverse projections between ```GeoPoints``` in the ```GDA20``` datum and ```PlanePoints``` in the ```MGA20```. Projection is a conformal UTM projection.

```python
gda20_pt = GeoPoint(dLat, dLng, datum=GDA20)
mga_pt = geo_to_mga(gda20_pt)
```

### MGA94
> NOTE: ```GDA94``` has been superceded by ```GDA20```.

Use ```geo_to_mga``` and ```mga_to_geo``` to perform forward/reverse projections between ```GeoPoints``` in ```GDA94``` datum and ```PlanePoints``` on the ```MGA``` grid. Projection is a [Conformal UTM Projection](https://github.com/chompar4/vicmap/blob/master/docs/A%20GUIDE%20TO%20MAP%20PROJECTIONS%20V3.pdf).

```python
gda20_pt = GeoPoint(dLat, dLng, datum=GDA94)
mga_pt = geo_to_mga(gda20_pt)
```

### VICGRID94

Use ```geo_to_vicgrid94``` and ```vicgrid94_to_geo``` to perform a forward / reverse projection from a ```GeoPoint``` in the ```GDA94``` datum to a ```PlanePoint``` in the ```VICGRID94``` plane. Projection used is [Lambert Conformal Conic](https://github.com/chompar4/vicmap/blob/master/docs/A%20GUIDE%20TO%20MAP%20PROJECTIONS%20V3.pdf).

```python 
gda94_pt = GeoPoint(dLat, dLng, datum=GDA94)
vic94_pt = geo_to_vicgrid94(gda94_pt)
```

### VICGRID

Use ```geo_to_vicgrid94``` and ```vicgrid94_to_geo``` to perform a forward / reverse lambert conformal conic projection from a ```GeoPoint``` in the ```AGD66``` datum to a ```PlanePoint``` in the ```VICGRID94``` plane.
 > NOTE: ```VICGRID``` has been superceded by ```VICGRID94```.

```python 
agd_pt = GeoPoint(dLat, dLng, datum=AGD66)
vic_pt = geo_to_vicgrid(gda94_pt)
```

### Converting between datums

Each datum has a conversion method.
> TODO

## Projections

#### Lambert Conformal Conic

```
Accepts:
    dLat: latitude in decimal degrees (-90, 90]
    dLng: longitude in decimal degrees (-180, 180]
    datum constants: (cm, a, b, 1/f, e, e2, n)
    grid constants: (λ0, φ0, E0, N0 φ1, φ2)
returns: 
    X: easting (m)
    Y: northing (m)
    m: point scale factor
    γ: grid convergence
```

#### Universal Transverse Mercator (UTM)

```
Accepts:
    dLat: latitude in decimal degrees (-90, 90]
    dLng: longitude in decimal degrees (-180, 180]
    cm: central meridian of zone containing (dLat, dLng)
    datum constants: (cm, a, b, 1/f, e, e2, n)
    grid constants: (m0, E0, N0)
returns: 
    z: zone
    E: UTM easting (m)
    N: UTM northing (m)
    m: point scale factor
    γ: grid convergence
```


### Reference Ellipsoids

Ellipsoid | Name| EPSG code | Semi-major-axis (a) | Reciprocal flattening
------------ | ------------- | ------------ | -------- | ------------
WGS80 | World Geodetic System 1984 Spheroid | ```7030``` | ```6,378,137m``` | ```298.257223563```
GRS80 | Geodetic Reference System 1980 Spheroid |  ```7019``` | ```6,378,137m``` | ```298.257222101```
ANS  | Australian National Spheroid |  ```7003``` | ```6,378,160m``` | ```298.25```
CLARKE | Clarke 1866 Spheroid | ```7008``` | ```6,378,350.871924m``` | ```294.26```

### Datums

Datum | Name | Ellipsoid | Reference Frame | EPSG code
------|------|-----------|-----------------|-----------
WGS84 | World Geodetic System 1984 | WGS84 | WGS84 | ```6326```
GDA20 | Geocentric Datum of Australia 2020 | GRS80 | ITRF2014 | ```1168```
GDA94 | Geocentric Datum of Australia 1994 | GRS80 | ITRF92 | ```6283```
AGD84 | Australian Geodetic Datum 1984 | ANS | | ```6203```
AGD66 | Australian Geodetic Datum 1966 | ANS | | ```6202```
ANG | | CLARKE | 
