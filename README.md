# vicmap
Cartographic tools for working with MGA & VICGRID coordinate systems.

## Installation
```
poetry install
```

## Point Transformations

Points on 3D Geoid surfaces are represented by the ```GeoPoint``` class, while points in the 2d plane are represented by the ```PlanePoint``` class. Each point requires a set of coordinates, and a datum. 

```python
pt = GeoPoint(dLat, dLng, datum=GDA20)
```

### MGA20
```MGA20``` is the pair of conformal UTM projections betwee the ```GDA20``` datum and the ```MGA``` grid.

Use ```geo_to_mga``` to perform a forward point projection from a ```GeoPoint``` in the GDA20 datum to a ```PlanePoint``` in the MGA grid.

```python
gda20_pt = GeoPoint(dLat, dLng, datum=GDA20)
mga_pt = geo_to_mga(gda20_pt)
```

Use ```mga_to_geo``` to perform a reverse point projection from a ```PlanePoint``` in the ```MGA``` grid to a ```GeoPoint``` in the required datum. By default, the output datum is ```GDA20```.

```python
mga_pt = PlanePoint(E, N, grid=MGA)
geo_pt = mga_to_geo(mga_pt) # default datum = GDA20
```

### MGA94
```MGA94``` is the pair of conformal UTM projections betwee the ```GDA94``` datum and the ```MGA``` grid. 
> NOTE: ```GDA94``` has been superceded by ```GDA20```.

Use ```geo_to_mga``` to perform a forward point projection from a ```GeoPoint``` in the ```GDA94``` datum to a ```PlanePoint``` in the MGA grid.

```python
gda20_pt = GeoPoint(dLat, dLng, datum=GDA20)
mga_pt = geo_to_mga(gda20_pt)
```

Use ```mga_to_geo``` to perform a reverse point projection from a ```PlanePoint``` in the ```MGA``` grid to a ```GeoPoint``` in the required datum. You must specify ```GDA94```

```python
mga_pt = PlanePoint(E, N, grid=MGA)
geo_pt = mga_to_geo(mga_pt, datum=GDA94)
```

### VICGRID20
??

### VICGRID94 

```VICGRID94``` is the pair of lambert conformal conic projections between the ```GDA94``` datum and the ```VICGRID94``` plane. 

Use ```geo_to_vicgrid94``` to perform a forward point projection from a ```GeoPoint``` in the ```GDA94``` datum to a ```PlanePoint``` in the ```VICGRID94``` plane.

```python 
gda94_pt = GeoPoint(dLat, dLng, datum=GDA94)
vic94_pt = geo_to_vicgrid94(gda94_pt)
```

Use ```vicgrid94_to_geo``` to perform a reverse point projection from a ```PlanePoint``` in the ```VICGRID94``` plabne to a ```GeoPoint``` in the required ```GDA94``` datum.

```python
vic_pt = PlanePoint(E, N, grid=VICGRID94)
geo_pt = vicgrid94_to_geo(mga_pt)
```

### VICGRID

```VICGRID``` is the pair of lambert conformal conic projections between the ```AGD66``` datum and the ```VICGRID``` plane. 
 > NOTE: ```VICGRID``` has been superceded by ```VICGRID94```.

Use ```geo_to_vicgrid``` to perform a forward point projection from a ```GeoPoint``` in the ```AGD66``` datum to a ```PlanePoint``` in the ```VICGRID``` plane.

```python 
agd_pt = GeoPoint(dLat, dLng, datum=AGD66)
vic_pt = geo_to_vicgrid(gda94_pt)
```

Use ```vicgrid_to_geo``` to perform a reverse point projection from a ```PlanePoint``` in the ```VICGRID``` plabne to a ```GeoPoint``` in the required ```AGD66``` datum.

```python
vic_pt = PlanePoint(E, N, grid=VICGRID)
agd_pt = vicgrid_to_geo(mga_pt)
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
