#Changes by release


## [0.6.1.dev0] - 2020-03-02

Bugfix and minor improvements

Fixed a bug which affected encoded data (lattice, vertices, normals and triangles).

* reverted presentation of `SFFVolume` subclasses to be ordered as (rows, cols, sections)
* now we store encoded data as unicode strings instead of bytes; otherwise, on export we write string with `'b"..."` formatting
* writing to JSON and HDF5 is not raw bytes but Unicode string
* version bump: v0.6.1.dev0


## [0.6.0.dev2] - 2020-02-25

* `-x/--exclude-geometry` for JSON output
* `--json-sort` and `--json-indent <+int>` to control JSON output
* now links to h5py documentation should work
* changed interface for v0.7.0 adapter HDF5 methods in line with sfftk-rw v0.6.0.dev0 changes
* now `args` passed through all classes for command-line contol/features

## [0.6.0.dev1] - 2020-02-24

* clean up of documentation to include correct examples, adapters and generateDS API
* now `from sfftkrw import SFFSegmentation` or `import sfftkrw as sff`
* new images for data model page
* new module `sfftkrw/conf.py` for settings; removed `sfftkrw/api.py`
* added new data files

## [0.6.0.dev0] - 2020-02-21

This is the first release to work with EMDB-SFF v0.8.0 files in addition to v0.7 files. When reading 
the API to use is determined from the version attribute. However, creating new files will only
be of v0.8.0.

* new `sfftkrw.api` provided a short path to v0.8 adapter e.g. `sfftkrw.api.SFFSegmentation`
* documentation improvements
* changed entry point to `sff` (from `sff-rw`)
* added references for Python version compatibility: `_FileNotFound`, `_classic_dict` 
* added missing field `attribute` to shapes
* changed `SFFSegmentation` container attributes to `*_list` e.g. `segment_list` instead of `segments`. 
However we retain `segments` as a property for backward compatibility.
* signature of HDF5 conversion methods (`as_hff` and `from_hff`) is now `*(parent_group, args, name=None)`
by default
* refactored `SFFSegmentation.from_file`
* new `SFFSegmentation.to_file` which is an alias for `SFFSegmentation.export`
* added test data under v0.8 schema

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


