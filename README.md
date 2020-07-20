# gda20
Cartographic tools for working with the MGA (Map Grid of Australia) & VICGRID94 coordinate systems.

# MGA

MGA is a UTM projection which uses the GDA20 datum and the following properties:
```
E0 = 500,000m false easting
N0 = 10,000,000m false northing
m0 = 0.9996 central scale factor 
cm0 = -177° central meridian of zone 1
```

See the ICSM GDA2020 Technical Manual for reference
```
https://www.icsm.gov.au/sites/default/files/GDA2020TechnicalManualV1.1.1.pdf
```

# VICGRID94

VICGRID94 is a lambert conformal conic projection centered on Victoria.

<img src="assets/lambert-conic-illustration.png">

See the VICGRID94 Map Projection Specifications doc for reference
```
https://www.yumpu.com/en/document/view/11956152/vicgrid94-map-projection-introduction-specifications
```


## Installation
```
poetry install
```