# gda20
Cartographic tools for working with MGA & VICGRID coordinate systems.


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


## MGA20

MGA (The Map Grid of Australia 2020) is a UTM projection based on the GDA20 datum with the following properties:
```
E0 = 500,000m false easting
N0 = 10,000,000m false northing
m0 = 0.9996 central scale factor
```

Zone 1 is defined to have central meridian 177°W and a zone width of 6°.

See the ICSM GDA2020 Technical Manual for reference
```
https://www.icsm.gov.au/sites/default/files/GDA2020TechnicalManualV1.1.1.pdf
```

## MGA94
MGA (The Map Grid of Australia 1994) is a UTM projection based on the GDA94 datum. It has been superceded by MGA20.


## VICGRID94

VICGRID94 is a lambert conformal conic projection with two standard parrellels, centered on Victoria which uses the GDA94 datum with the following properties:

```
E0 = 2,500,000m false easting
N0 = 2,500,000m false northing
φ1 = 36°S standard parralel 1
φ2 = 38°S standard parralel 2
(φ0, λ0) = (37°S, 145°E) true origin
```

<img src="assets/lambert-conic-illustration.png">

See the VICGRID94 Map Projection Specifications doc for reference.

```
https://www.yumpu.com/en/document/view/11956152/vicgrid94-map-projection-introduction-specifications
```

## VICGRID

VICGRID is a lambert conformal conic projection similar to VICGRID94, but uses the AGD66 datum. The VICGRID projection incorporates a different origin specification to VICGRID94 in order to avoid confusion between coordinates generated by the two projections. It has been superceeded by VICGRID94.

```
E0 = 2,500,000m false easting
N0 = 4,500,000m false northing
φ1 = 36°S standard parralel 1
φ2 = 38°S standard parralel 2
(φ0, λ0) = (37°S, 145°E) true origin
```

See the VICGRID94 Map Projection Specifications doc for reference

```
https://www.yumpu.com/en/document/view/11956152/vicgrid94-map-projection-introduction-specifications
```

## Installation
```
poetry install
```