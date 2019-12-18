#Changes by release

## [0.5.2.dev1] - 2019-12-18

### List validations

* schema/base.py: `SFFListType` uses `min_length` attribute to check that minimum length constraint is satisfied
* schema/adapter.py: `min_length` attribute set for `SFFPolygonList` (1) and `SFFVertexList` (3)
* added unit test for the above
* deleted config stub file
* version bump: v0.5.2.dev1

## [0.5.2.dev0] - 2019-12-17

### Major improvements in handling of HDF5 and JSON

* fixed bug relating to having external references as `None`
* we now have validation; validation is only assessed on export/import otherwise users are free to build objects incrementally
with no fear of validation failures on creation or use; validation works by checking if an attribute is defined (on the 
`SFFType` subclass with `required=True` - if no value is found during export/import then a validation error is raised of
type `SFFValueError` (see below)
* also `SFFAttribute` now has a `default=<value>` attribute which will be used if no value is specified or found
* schema/base.py: added new error `SFFValueError` for failed validation
* validation is done using `inspect.getattr_static` which is not available in Python 2.7 so we just copied the code
from Python 3.8, which works OK
* schema/adapter.py: the following classes benefit from the validation checks above *only for JSON import/export*: `SFFRGBA`, 
`SFFBiologicalAnnotation`, `SFFExternalReference`, `SFFExternalReferenceList`, `SFFSegment`, `SFFBoundingBox`, `SFFSegmentation`
* schema/adapter.py: all relevant classes have mandatory arguments with `required=True` according to the EMDB-SFF data model
* moderately improved test coverage (83% to 85%)
* now `.xml`, `.hdf5`, and `.h5` are implicitly valid extensions
* `sff-rw view` now handles UniCode characters correctly
* version bump: v0.5.2.dev0

## [0.5.1.dev0] - 2019-11-11

Fixed Issue #2

## [0.5.0.dev1] - 2019-11-11

Fixed broken documentation due to unmocked modules

## [0.5.0.dev0] - 2019-11-08

First release of `sfftk-rw`


