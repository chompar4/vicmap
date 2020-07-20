# gda20
Cartographic tools for working with the MGA (Map Grid of Australia) & VICGRID94 coordinate systems.

## MGA

MGA (The Map Grid of Australia) is a UTM projection based on the GDA20 datum with the following properties:
```
E0 = 500,000m false easting
N0 = 10,000,000m false northing
m0 = 0.9996 central scale factor
```

Zone 1 is defined to have central meridian 177°S.

See the ICSM GDA2020 Technical Manual for reference
```
https://www.icsm.gov.au/sites/default/files/GDA2020TechnicalManualV1.1.1.pdf
```

## VICGRID94

VICGRID94 is a lambert conformal conic projection centered on Victoria with the following properties: 

```
E0 = 2,500,000m false easting
N0 = 2,500,000m false northing
φ1 = 36°S standard parralel 1
φ2 = 38°S standard parralel 2
(φ0, λ0) = (37°S, 145°E) true origin
```

<img src="assets/lambert-conic-illustration.png">

See the VICGRID94 Map Projection Specifications doc for reference

```
https://www.yumpu.com/en/document/view/11956152/vicgrid94-map-projection-introduction-specifications
```

## VICGRID

VICGRID is a lambert conformal conic projection identical to VICGRID94, but with the following properties:

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