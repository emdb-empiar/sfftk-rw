#Changes by release

## [0.8.0] - 2023-09-25

* added `SFFSubtomogramAverage` class

## [0.7.3] - 2023-01-27 Option to include source EMDB-SFF colours when merging

* In EMDB-SFF `v0.8.0.dev1` `SFFSegmentation.merge_annotation(other_seg, include_colour=False)` (*do not* merge colour by default)

## [0.7.2] - 2022-04-26

add Python3.10 support

* removed use of `os` package for exit codes (problems on Windows)
* fixed errors in `developing` documentation

## [0.7.1] - 2021-08-24

bugfix: reading from HDF5 retains some ids as `numpy.int64`

* tests added and pass

## [0.7.0] - 2021-06-17

add Python3.9 support; dropped Python2.7

* add official support for Python3.9
* dropped support for Python2.7 and Python3.5
* now in beta but stable
* new version: v0.7.0

## [0.6.7.dev1] - 2020-11-10

dropped py39 until time is available ;-)
version bump: v0.6.7.dev1

## [0.6.7.dev0] - 2020-11-09

h5py accommomdation

* h5py>3 has dropped py27 support; it now returns strings as bytes
* this release fixes reading of bytes as unicode strings
* also works with py39
* modified h5py version for py35
* version bump: v0.6.7.dev0

## [0.6.6.dev0] - 2020-05-15

Bugfix: saving excluding name, software and details

* merge_annotation method had these fields commented out; fixed
* unit tests updated to check the same
* version bump: v0.6.6.dev0

## [0.6.5.dev0] - 2020-05-15

Bugfix: index collision during append for new objects to lists

* during annotation in `sfftk` new objects e.g. `SFFSoftware` or `SFFExternalReference` objects, are
created with an `id=0`; an exception is raised during addition to the `SFFListType._id_dict` if the ID
already exists;
* fix: a new method `_get_next_id` has been added to `SFFListType` which determines the next best ID
to use to avoid collision; this also works when items with `id=None` are added - a new ID (starting from 1)
is issued to ensure the integrity of `SFFListType._id_dict`
* version bump: v0.6.5.dev0

## [0.6.4.dev0] - 2020-04-15

Bugfix: reading large XML files

* version bump: v0.6.4.dev0

## [0.6.3.dev0] - 2020-04-14

Bugfix: reading of empty bounding box in v0.7.0.dev0 files

* version bump: v0.6.3.dev0

## [0.6.2.dev6] - 2020-03-30

Development changes

* removed redudant `-t/--top-level-only` convert flag

## [0.6.2.dev5] - 2020-03-26

Development changes

* minor documentation corrections
* handling `MemoryError` when encoding large 3D volumes for travis
* version bump: v0.6.2.dev5

## [0.6.2.dev4] - 2020-08-18

Development bugfix

* utils.py: `get_path()` now returns `None` if path invalid
* version bump: v0.6.2.dev4

## [0.6.2.dev3] - 2020-08-18

Development bugfix

* `sfftk` will now use core tools from `sfftk-rw`
* use `iter*` methods from `_dict` (dictionary preserving insertion order) instead of from builtin dictionary
* version bump: v0.6.2.dev3

## [0.6.2.dev2] - 2020-03-13

Development changes

* view parser: check EMDB-SFF version with `--sff-version`
* handling of IMOD chunks deferred to `sfftk` package
* this change has no impact whatsover on function of the package

## [0.6.2.dev1] - 2020-03-13

Development changes

* convert parser argument `from_file` has `nargs='*'` for `sfftk` downstream
* this change has no impact whatsover on function of the package

## [0.6.2.dev0] - 2020-03-06

added methods for handling notes to `sfftkrw.SFFSegmentation`

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


