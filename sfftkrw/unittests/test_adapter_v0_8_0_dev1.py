# -*- coding: utf-8 -*-
from __future__ import print_function

import importlib
import json
import os
import random
import re
import sys
import tempfile

import h5py
import numpy
from random_words import RandomWords, LoremIpsum

rw = RandomWords()
li = LoremIpsum()

from . import TEST_DATA_PATH, Py23FixTestCase, _random_integer, _random_float, _random_integers, _random_floats
from ..core import _str, _xrange, _decode, _bytes, _encode
from ..schema import base

EMDB_SFF_VERSION = u'0.8.0.dev1'

adapter_name = 'sfftkrw.schema.adapter_v{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_')
)
adapter = importlib.import_module(adapter_name)

# dynamically import the latest schema generateDS API
emdb_sff_name = 'sfftkrw.schema.v{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_')
)
emdb_sff = importlib.import_module(emdb_sff_name)


class TestSFFRGBA(Py23FixTestCase):
    def setUp(self):
        self.red = random.random()
        self.green = random.random()
        self.blue = random.random()
        self.alpha = random.random()

    def test_default(self):
        """Test default colour"""
        colour = adapter.SFFRGBA()
        colour.red = self.red
        colour.green = self.green
        colour.blue = self.blue
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        self.assertEqual(colour.alpha, 1.0)

    def test_kwarg_colour(self):
        """Test colour using kwargs"""
        colour = adapter.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        self.assertEqual(colour.alpha, self.alpha)

    def test_get_value(self):
        """Test colour.value"""
        colour = adapter.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        red, green, blue, alpha = colour.value
        self.assertEqual(colour.red, red)
        self.assertEqual(colour.green, green)
        self.assertEqual(colour.blue, blue)
        self.assertEqual(colour.alpha, alpha)

    def test_set_value(self):
        """Test colour.value = rgb(a)"""
        # rgb
        colour = adapter.SFFRGBA()
        colour.value = self.red, self.green, self.blue
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        # rgba
        colour.value = self.red, self.green, self.blue, self.alpha
        self.assertEqual(colour.red, self.red)
        self.assertEqual(colour.green, self.green)
        self.assertEqual(colour.blue, self.blue)
        self.assertEqual(colour.alpha, self.alpha)

    def test_as_hff(self):
        """Test convert to HDF5 group"""
        colour = adapter.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u"container")
            group = colour.as_hff(group)
            self.assertIn(u"colour", group)
            self.assertCountEqual(group[u'colour'][()], colour.value)

    def test_from_hff(self):
        """Test create from HDF5 group"""
        colour = adapter.SFFRGBA(
            red=self.red,
            green=self.green,
            blue=self.blue,
            alpha=self.alpha
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u"container")
            group = colour.as_hff(group)
            self.assertIn(u"colour", group)
            self.assertCountEqual(group[u'colour'][()], colour.value)
            colour2 = adapter.SFFRGBA.from_hff(h[u'container'])
            self.assertCountEqual(colour.value, colour2.value)

    def test_native_random_colour(self):
        """Test that using a kwarg random_colour will set random colours"""
        colour = adapter.SFFRGBA(random_colour=True)
        self.assertTrue(0 <= colour.red <= 1)
        self.assertTrue(0 <= colour.green <= 1)
        self.assertTrue(0 <= colour.blue <= 1)
        self.assertTrue(0 <= colour.alpha <= 1)

    def test_validation(self):
        """Test that validation works"""
        c = adapter.SFFRGBA(random_colour=True)
        self.assertTrue(c._is_valid())
        c = adapter.SFFRGBA()
        self.assertFalse(c._is_valid())

    def test_as_json(self):
        """Test export to JSON"""
        # empty
        c = adapter.SFFRGBA()
        with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
            c.export(sys.stderr)
        # populated
        c = adapter.SFFRGBA(random_colour=True)
        c_json = c.as_json()
        self.assertEqual(c_json, c.value)

    def test_from_json(self):
        """Test import from JSON"""
        c_json = (0.8000087483646712, 0.017170600210644427, 0.5992636068532492, 1.0)
        c = adapter.SFFRGBA.from_json(c_json)
        self.assertEqual(c.value, c_json)


class TestSFFExternalReference(Py23FixTestCase):
    def setUp(self):
        self.i = _random_integer()
        self.r = rw.random_word()
        self.u = rw.random_word()
        self.a = rw.random_word()
        self.l = u" ".join(rw.random_words(count=3))
        self.d = li.get_sentence()

    def tearDown(self):
        adapter.SFFExternalReference.reset_id()

    def test_default(self):
        """Test default settings"""
        e = adapter.SFFExternalReference(
            resource=self.r,
            url=self.u,
            accession=self.a,
            label=self.l,
            description=self.d
        )
        self.assertEqual(e.id, 0)
        self.assertEqual(e.resource, self.r)
        self.assertEqual(e.url, self.u)
        self.assertEqual(e.accession, self.a)
        self.assertEqual(e.label, self.l)
        self.assertEqual(e.description, self.d)
        self.assertEqual(
            _str(e),
            u"""SFFExternalReference(id={}, resource="{}", url="{}", accession="{}", label="{}", description="{}")""".format(
                0, self.r, self.u, self.a, self.l, self.d
            )
        )

    def test_from_gds_type(self):
        """Test that we can instantiate from gds_type"""
        _e = emdb_sff.external_reference_type(
            id=self.i,
            resource=self.r,
            url=self.u,
            accession=self.a,
            label=self.l,
            description=self.d,
        )
        e = adapter.SFFExternalReference.from_gds_type(_e)
        self.assertEqual(e.id, self.i)
        self.assertEqual(e.resource, self.r)
        self.assertEqual(e.url, self.u)
        self.assertEqual(e.accession, self.a)
        self.assertEqual(e.label, self.l)
        self.assertEqual(e.description, self.d)
        self.assertEqual(
            _str(e),
            u"""SFFExternalReference(id={}, resource="{}", url="{}", accession="{}", label="{}", description="{}")""".format(
                self.i, self.r, self.u, self.a, self.l, self.d
            )
        )

    def test_as_json(self):
        """Test that we can output as JSON"""
        e = adapter.SFFExternalReference()
        self.assertEqual(e.as_json(), {
            u"id": e.id,
            u"resource": None,
            u"url": None,
            u"accession": None,
            u"label": None,
            u"description": None,
        })
        e = adapter.SFFExternalReference(
            resource=self.r,
            url=self.u,
            accession=self.a,
            label=self.l,
            description=self.d,
        )
        e_json = e.as_json()
        self.assertEqual(e_json[u'id'], e.id)
        self.assertEqual(e_json[u'resource'], e.resource)
        self.assertEqual(e_json[u'url'], e.url)
        self.assertEqual(e_json[u'accession'], e.accession)
        self.assertEqual(e_json[u'label'], e.label)
        self.assertEqual(e_json[u'description'], e.description)
        # missing mandatory
        e = adapter.SFFExternalReference(
            # resource=self.r,
            # url=self.u,
            # accession=self.a,
            label=self.l,
            description=self.d,
        )
        with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
            e.export(sys.stderr)
        # missing non-mandatory
        e = adapter.SFFExternalReference(
            resource=self.r,
            url=self.u,
            accession=self.a,
            # label=self.l,
            # description=self.d,
        )
        self.assertEqual(e_json[u'resource'], e.resource)
        self.assertEqual(e_json[u'url'], e.url)
        self.assertEqual(e_json[u'accession'], e.accession)

    def test_from_json(self):
        """Test that we can recreate from JSON"""
        e_json = {'id': 0, 'resource': 'symptom', 'url': 'thin', 'accession': 'definitions',
                  'label': 'chairpersons swabs pools',
                  'description': 'Malesuada facilisinam elitduis mus dis facer, primis est pellentesque integer dapibus '
                                 'semper semvestibulum curae lacusnulla.'}
        e = adapter.SFFExternalReference.from_json(e_json)
        self.assertEqual(e_json[u'id'], e.id)
        self.assertEqual(e_json[u'resource'], e.resource)
        self.assertEqual(e_json[u'url'], e.url)
        self.assertEqual(e_json[u'accession'], e.accession)
        self.assertEqual(e_json[u'label'], e.label)
        self.assertEqual(e_json[u'description'], e.description)
        # missing mandatory
        e_json = {'id': 0, 'url': 'thin', 'accession': 'definitions',
                  'label': 'chairpersons swabs pools',
                  'description': 'Malesuada facilisinam elitduis mus dis facer, primis est pellentesque integer dapibus '
                                 'semper semvestibulum curae lacusnulla.'}
        adapter.SFFExternalReference.from_json(e_json)
        # missing non-mandatory
        e_json = {'resource': 'symptom', 'url': 'thin', 'accession': 'definitions',
                  'label': 'chairpersons swabs pools'}
        e = adapter.SFFExternalReference.from_json(e_json)
        self.assertIsNone(e.id)
        self.assertEqual(e_json[u'resource'], e.resource)
        self.assertEqual(e_json[u'url'], e.url)
        self.assertEqual(e_json[u'accession'], e.accession)
        self.assertEqual(e_json[u'label'], e.label)
        self.assertIsNone(e.description)

    def test_hff(self):
        """Interconversion to HDF5"""
        # empty
        e = adapter.SFFExternalReference()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = e.as_hff(group)
            self.assertIn(u'{}'.format(e.id), group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                e2 = adapter.SFFExternalReference.from_hff(group)
                self.assertEqual(e, e2)
        # empty with id=None
        e = adapter.SFFExternalReference(new_obj=False)
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = e.as_hff(group)
            self.assertIn(u'{}'.format(e.id), group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                e2 = adapter.SFFExternalReference.from_hff(group)
                self.assertEqual(e, e2)
        # pop'd
        e = adapter.SFFExternalReference(
            resource=self.r,
            url=self.u,
            accession=self.a,
            label=self.l,
            description=self.d,
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = e.as_hff(group)
            group_name = u'{}'.format(e.id)
            self.assertIn(group_name, group)
            self.assertIn(group_name + u'/resource', group)
            self.assertIn(group_name + u'/url', group)
            self.assertIn(group_name + u'/accession', group)
            self.assertIn(group_name + u'/label', group)
            self.assertIn(group_name + u'/description', group)
            self.assertEqual(group[group_name + u'/id'][()], e.id)
            self.assertEqual(group[group_name + u'/resource'][()], e.resource)
            self.assertEqual(group[group_name + u'/url'][()], e.url)
            self.assertEqual(group[group_name + u'/accession'][()], e.accession)
            self.assertEqual(group[group_name + u'/label'][()], e.label)
            self.assertEqual(group[group_name + u'/description'][()], e.description)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                e2 = adapter.SFFExternalReference.from_hff(group)
                self.assertEqual(e, e2)
        # missing non-mandatory
        e = adapter.SFFExternalReference(
            resource=self.r,
            url=self.u,
            accession=self.a,
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = e.as_hff(group)
            group_name = u'{}'.format(e.id)
            self.assertIn(group_name, group)
            self.assertIn(group_name + u'/resource', group)
            self.assertIn(group_name + u'/url', group)
            self.assertIn(group_name + u'/accession', group)
            self.assertNotIn(group_name + u'/label', group)
            self.assertNotIn(group_name + u'/description', group)
            self.assertEqual(group[group_name + u'/id'][()], e.id)
            self.assertEqual(group[group_name + u'/resource'][()], e.resource)
            self.assertEqual(group[group_name + u'/url'][()], e.url)
            self.assertEqual(group[group_name + u'/accession'][()], e.accession)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                e2 = adapter.SFFExternalReference.from_hff(group)
                self.assertEqual(e, e2)


class TestSFFExternalReferenceList(Py23FixTestCase):
    def setUp(self):
        self._no_items = _random_integer(start=2, stop=10)
        self.ii = list(_xrange(self._no_items))
        self.rr = [rw.random_word() for _ in _xrange(self._no_items)]
        self.uu = [rw.random_word() for _ in _xrange(self._no_items)]
        self.aa = [rw.random_word() for _ in _xrange(self._no_items)]
        self.ll = [" ".join(rw.random_words(count=3)) for _ in _xrange(self._no_items)]
        self.dd = [li.get_sentence() for _ in _xrange(self._no_items)]

    def tearDown(self):
        adapter.SFFExternalReference.reset_id()

    def test_default(self):
        """Test default settings"""
        ee = [adapter.SFFExternalReference(
            resource=self.rr[i],
            url=self.uu[i],
            accession=self.aa[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        E = adapter.SFFExternalReferenceList()
        [E.append(e) for e in ee]
        # str
        self.assertRegex(
            _str(E),
            r"""SFFExternalReferenceList\(\[.*\]\)"""
        )
        # length
        self.assertEqual(len(E), self._no_items)
        # get
        e = E[self._no_items - 1]
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, self._no_items - 1)
        self.assertEqual(e.resource, self.rr[self._no_items - 1])
        self.assertEqual(e.url, self.uu[self._no_items - 1])
        self.assertEqual(e.accession, self.aa[self._no_items - 1])
        self.assertEqual(e.label, self.ll[self._no_items - 1])
        self.assertEqual(e.description, self.dd[self._no_items - 1])
        # get_ids
        e_ids = E.get_ids()
        self.assertEqual(len(e_ids), self._no_items)
        # get_by_ids
        e_id = random.choice(list(e_ids))
        e = E.get_by_id(e_id)
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, e_id)
        self.assertEqual(e.resource, self.rr[e_id])
        self.assertEqual(e.url, self.uu[e_id])
        self.assertEqual(e.accession, self.aa[e_id])
        self.assertEqual(e.label, self.ll[e_id])
        self.assertEqual(e.description, self.dd[e_id])

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _ee = [emdb_sff.external_reference_type(
            id=self.ii[i],
            resource=self.rr[i],
            url=self.uu[i],
            accession=self.aa[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        _E = emdb_sff.external_referencesType()
        _E.set_ref(_ee)
        E = adapter.SFFExternalReferenceList.from_gds_type(_E)
        # str
        self.assertRegex(
            _str(E),
            r"""SFFExternalReferenceList\(\[.*\]\)"""
        )
        # length
        self.assertEqual(len(E), self._no_items)
        # get
        e = E[self._no_items - 1]
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, self._no_items - 1)
        self.assertEqual(e.resource, self.rr[self._no_items - 1])
        self.assertEqual(e.url, self.uu[self._no_items - 1])
        self.assertEqual(e.accession, self.aa[self._no_items - 1])
        self.assertEqual(e.label, self.ll[self._no_items - 1])
        self.assertEqual(e.description, self.dd[self._no_items - 1])
        # get_ids
        e_ids = E.get_ids()
        self.assertEqual(len(e_ids), self._no_items)
        # get_by_ids
        e_id = random.choice(list(e_ids))
        e = E.get_by_id(e_id)
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, e_id)
        self.assertEqual(e.resource, self.rr[e_id])
        self.assertEqual(e.url, self.uu[e_id])
        self.assertEqual(e.accession, self.aa[e_id])
        self.assertEqual(e.label, self.ll[e_id])
        self.assertEqual(e.description, self.dd[e_id])

    def test_as_json(self):
        """Test that we can export to JSON"""
        ee = adapter.SFFExternalReferenceList()
        self.assertEqual(ee.as_json(), [])
        ee = [adapter.SFFExternalReference(
            resource=self.rr[i],
            url=self.uu[i],
            accession=self.aa[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        E = adapter.SFFExternalReferenceList()
        [E.append(e) for e in ee]
        E_json = E.as_json()
        # _print(E_json)
        for i in _xrange(self._no_items):
            self.assertEqual(E[i].id, E_json[i][u'id'])
            self.assertEqual(E[i].resource, E_json[i][u'resource'])
            self.assertEqual(E[i].url, E_json[i][u'url'])
            self.assertEqual(E[i].accession, E_json[i][u'accession'])
            self.assertEqual(E[i].label, E_json[i][u'label'])
            self.assertEqual(E[i].description, E_json[i][u'description'])
        # empty
        E = adapter.SFFExternalReferenceList()
        E_json = E.as_json()
        self.assertEqual(len(E), len(E_json))

    def test_from_json(self):
        """Test that we can import from JSON"""
        E_json = [{'id': 0, 'resource': 'projectiles', 'url': 'blast', 'accession': 'injector',
                   'label': 'bricks breaches crawl',
                   'description': 'Est facilisicurabitur morbi dapibus volutpat, vestibulumnulla consecteturpraesent velit sempermorbi diaminteger taciti risusdonec accusam.'},
                  {'id': 1, 'resource': 'signals', 'url': 'wines', 'accession': 'experience',
                   'label': 'alibi defaults showers',
                   'description': 'Auctor habitasse amet temporsuspendisse, integer hendrerit nullasuspendisse.'},
                  {'id': 2, 'resource': 'openings', 'url': 'pack', 'accession': 'augmentations',
                   'label': 'outing rings tilling',
                   'description': 'Liberoduis esse nobis semvestibulum bibendumin non, sagittis eget eum massapellentesque eratproin nonummy massaphasellus.'},
                  {'id': 3, 'resource': 'blaze', 'url': 'contract', 'accession': 'diagrams',
                   'label': 'sewers weddings telecommunications',
                   'description': 'Ipsum no luctus ultricies enimsed antesuspendisse.'},
                  {'id': 4, 'resource': 'terms', 'url': 'blackboard', 'accession': 'nothing',
                   'label': 'depot trades strikers', 'description': 'Elitr hendrerit tortorvestibulum exerci.'},
                  {'id': 5, 'resource': 'carriage', 'url': 'screens', 'accession': 'apprehension',
                   'label': 'signalers hunk wagon', 'description': 'Consequatduis muspellentesque.'},
                  {'id': 6, 'resource': 'lot', 'url': 'gums', 'accession': 'rim', 'label': 'chatter north clearances',
                   'description': 'Nostra felis.'},
                  {'id': 7, 'resource': 'outlet', 'url': 'actions', 'accession': 'twists',
                   'label': 'compromises additives mirrors',
                   'description': 'Diaminteger phasellus mi sollicitudin laoreetphasellus possim, himenaeos semvestibulum egestasmauris clita elitnunc suscipit pulvinar.'},
                  {'id': 8, 'resource': 'shears', 'url': 'user', 'accession': 'view', 'label': 'cable diagram churns',
                   'description': 'Dolor laoreet adipiscing takimata neque dignissim velit enimaliquam, lobortisetiam mazim nunccurabitur aliquip praesent blandit.'},
                  {'id': 9, 'resource': 'jurisdiction', 'url': 'plug', 'accession': 'calibrations',
                   'label': 'oscillation baby males', 'description': 'Iusto aliquam quod orci, aaenean justo luctus.'}]
        E = adapter.SFFExternalReferenceList.from_json(E_json)
        for i, extref in enumerate(E_json):
            self.assertEqual(E[i].id, extref[u'id'])
            self.assertEqual(E[i].resource, extref[u'resource'])
            self.assertEqual(E[i].url, extref[u'url'])
            self.assertEqual(E[i].accession, extref[u'accession'])
            self.assertEqual(E[i].label, extref[u'label'])
            self.assertEqual(E[i].description, extref[u'description'])

    def test_hff(self):
        """Interconvert to HDF5"""
        # empty
        ee = adapter.SFFExternalReferenceList()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = ee.as_hff(group)
            self.assertIn(u'external_references', group)
            self.assertEqual(len(ee), 0)
            self.assertEqual(len(ee), len(group[u'external_references']))
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            ee2 = adapter.SFFExternalReferenceList.from_hff(h[u'container'])
            self.assertEqual(ee, ee2)
        # pop'd but empty extrefs
        ee = adapter.SFFExternalReferenceList()
        e = adapter.SFFExternalReference()
        ee.append(e)
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = ee.as_hff(group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            ee2 = adapter.SFFExternalReferenceList.from_hff(h[u'container'])
            self.assertEqual(ee, ee2)
        # pop'd
        ee = [adapter.SFFExternalReference(
            resource=self.rr[i],
            url=self.uu[i],
            accession=self.aa[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        E = adapter.SFFExternalReferenceList()
        [E.append(e) for e in ee]
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = E.as_hff(group)
            self.assertIn(u'external_references', group)
            self.assertTrue(len(ee) > 0)
            self.assertEqual(len(ee), len(group[u'external_references']))
            for er in E:
                self.assertEqual(er,
                                 adapter.SFFExternalReference.from_hff(group[u'external_references/{}'.format(er.id)]))
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            ee2 = adapter.SFFExternalReferenceList.from_hff(h[u'container'])


class TestSFFGlobalExternalReferenceList(Py23FixTestCase):
    """Test the SFFGlobalExternalReferenceList class"""

    def setUp(self):
        self._no_items = _random_integer(start=2, stop=10)
        self.ii = list(_xrange(self._no_items))
        self.rr = [rw.random_word() for _ in _xrange(self._no_items)]
        self.uu = [rw.random_word() for _ in _xrange(self._no_items)]
        self.aa = [rw.random_word() for _ in _xrange(self._no_items)]
        self.ll = [" ".join(rw.random_words(count=3)) for _ in _xrange(self._no_items)]
        self.dd = [li.get_sentence() for _ in _xrange(self._no_items)]

    def tearDown(self):
        adapter.SFFExternalReference.reset_id()

    def test_default(self):
        """Test default settings"""
        ee = [adapter.SFFExternalReference(
            resource=self.rr[i],
            url=self.uu[i],
            accession=self.aa[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        G = adapter.SFFGlobalExternalReferenceList()
        [G.append(e) for e in ee]
        # str
        self.assertRegex(
            _str(G),
            r"""SFFGlobalExternalReferenceList\(\[.*\]\)"""
        )
        # length
        self.assertEqual(len(G), self._no_items)
        # get
        e = G[self._no_items - 1]
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, self._no_items - 1)
        self.assertEqual(e.resource, self.rr[self._no_items - 1])
        self.assertEqual(e.url, self.uu[self._no_items - 1])
        self.assertEqual(e.accession, self.aa[self._no_items - 1])
        self.assertEqual(e.label, self.ll[self._no_items - 1])
        self.assertEqual(e.description, self.dd[self._no_items - 1])
        # get_ids
        e_ids = G.get_ids()
        self.assertEqual(len(e_ids), self._no_items)
        # get_by_ids
        e_id = random.choice(list(e_ids))
        e = G.get_by_id(e_id)
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, e_id)
        self.assertEqual(e.resource, self.rr[e_id])
        self.assertEqual(e.url, self.uu[e_id])
        self.assertEqual(e.accession, self.aa[e_id])
        self.assertEqual(e.label, self.ll[e_id])
        self.assertEqual(e.description, self.dd[e_id])

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _ee = [emdb_sff.external_reference_type(
            id=self.ii[i],
            resource=self.rr[i],
            url=self.uu[i],
            accession=self.aa[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        _G = emdb_sff.global_external_referencesType()
        _G.set_ref(_ee)
        G = adapter.SFFGlobalExternalReferenceList.from_gds_type(_G)
        # str
        self.assertRegex(
            _str(G),
            r"""SFFGlobalExternalReferenceList\(\[.*\]\)"""
        )
        # length
        self.assertEqual(len(G), self._no_items)
        # get
        e = G[self._no_items - 1]
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, self._no_items - 1)
        self.assertEqual(e.resource, self.rr[self._no_items - 1])
        self.assertEqual(e.url, self.uu[self._no_items - 1])
        self.assertEqual(e.accession, self.aa[self._no_items - 1])
        self.assertEqual(e.label, self.ll[self._no_items - 1])
        self.assertEqual(e.description, self.dd[self._no_items - 1])
        # get_ids
        e_ids = G.get_ids()
        self.assertEqual(len(e_ids), self._no_items)
        # get_by_ids
        e_id = random.choice(list(e_ids))
        e = G.get_by_id(e_id)
        self.assertIsInstance(e, adapter.SFFExternalReference)
        self.assertEqual(e.id, e_id)
        self.assertEqual(e.resource, self.rr[e_id])
        self.assertEqual(e.url, self.uu[e_id])
        self.assertEqual(e.accession, self.aa[e_id])
        self.assertEqual(e.label, self.ll[e_id])
        self.assertEqual(e.description, self.dd[e_id])

    def test_as_json(self):
        """Test that we can export to JSON"""
        ge = adapter.SFFGlobalExternalReferenceList()
        self.assertEqual(ge.as_json(), [])
        ge = [adapter.SFFExternalReference(
            resource=self.rr[i],
            url=self.uu[i],
            accession=self.aa[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        G = adapter.SFFGlobalExternalReferenceList()
        [G.append(g) for g in ge]
        G_json = G.as_json()
        for i in _xrange(self._no_items):
            self.assertEqual(G[i].id, G_json[i][u'id'])
            self.assertEqual(G[i].resource, G_json[i][u'resource'])
            self.assertEqual(G[i].url, G_json[i][u'url'])
            self.assertEqual(G[i].accession, G_json[i][u'accession'])
            self.assertEqual(G[i].label, G_json[i][u'label'])
            self.assertEqual(G[i].description, G_json[i][u'description'])
        # empty
        G = adapter.SFFGlobalExternalReferenceList()
        G_json = G.as_json()
        self.assertEqual(len(G), len(G_json))

    def test_from_json(self):
        """Test that we can import from JSON"""
        G_json = [{'id': 0, 'resource': 'projectiles', 'url': 'blast', 'accession': 'injector',
                   'label': 'bricks breaches crawl',
                   'description': 'Est facilisicurabitur morbi dapibus volutpat, vestibulumnulla consecteturpraesent velit sempermorbi diaminteger taciti risusdonec accusam.'},
                  {'id': 1, 'resource': 'signals', 'url': 'wines', 'accession': 'experience',
                   'label': 'alibi defaults showers',
                   'description': 'Auctor habitasse amet temporsuspendisse, integer hendrerit nullasuspendisse.'},
                  {'id': 2, 'resource': 'openings', 'url': 'pack', 'accession': 'augmentations',
                   'label': 'outing rings tilling',
                   'description': 'Liberoduis esse nobis semvestibulum bibendumin non, sagittis eget eum massapellentesque eratproin nonummy massaphasellus.'},
                  {'id': 3, 'resource': 'blaze', 'url': 'contract', 'accession': 'diagrams',
                   'label': 'sewers weddings telecommunications',
                   'description': 'Ipsum no luctus ultricies enimsed antesuspendisse.'},
                  {'id': 4, 'resource': 'terms', 'url': 'blackboard', 'accession': 'nothing',
                   'label': 'depot trades strikers', 'description': 'Elitr hendrerit tortorvestibulum exerci.'},
                  {'id': 5, 'resource': 'carriage', 'url': 'screens', 'accession': 'apprehension',
                   'label': 'signalers hunk wagon', 'description': 'Consequatduis muspellentesque.'},
                  {'id': 6, 'resource': 'lot', 'url': 'gums', 'accession': 'rim', 'label': 'chatter north clearances',
                   'description': 'Nostra felis.'},
                  {'id': 7, 'resource': 'outlet', 'url': 'actions', 'accession': 'twists',
                   'label': 'compromises additives mirrors',
                   'description': 'Diaminteger phasellus mi sollicitudin laoreetphasellus possim, himenaeos semvestibulum egestasmauris clita elitnunc suscipit pulvinar.'},
                  {'id': 8, 'resource': 'shears', 'url': 'user', 'accession': 'view', 'label': 'cable diagram churns',
                   'description': 'Dolor laoreet adipiscing takimata neque dignissim velit enimaliquam, lobortisetiam mazim nunccurabitur aliquip praesent blandit.'},
                  {'id': 9, 'resource': 'jurisdiction', 'url': 'plug', 'accession': 'calibrations',
                   'label': 'oscillation baby males', 'description': 'Iusto aliquam quod orci, aaenean justo luctus.'}]
        G = adapter.SFFGlobalExternalReferenceList.from_json(G_json)
        for i, extref in enumerate(G_json):
            self.assertEqual(G[i].id, extref[u'id'])
            self.assertEqual(G[i].resource, extref[u'resource'])
            self.assertEqual(G[i].url, extref[u'url'])
            self.assertEqual(G[i].accession, extref[u'accession'])
            self.assertEqual(G[i].label, extref[u'label'])
            self.assertEqual(G[i].description, extref[u'description'])

    def test_hff(self):
        """Interconvert to HDF5"""
        # empty
        G = adapter.SFFGlobalExternalReferenceList()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = G.as_hff(group)
            self.assertIn(u'global_external_references', group)
            self.assertEqual(len(G), 0)
            self.assertEqual(len(G), len(group[u'global_external_references']))
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            G2 = adapter.SFFGlobalExternalReferenceList.from_hff(h[u'container'])
            self.assertEqual(G, G2)
        # pop'd
        G = adapter.SFFGlobalExternalReferenceList()
        [G.append(adapter.SFFExternalReference(
            resource=self.rr[i],
            url=self.uu[i],
            accession=self.aa[i],
            label=self.ll[i],
            description=self.dd[i]
        )) for i in _xrange(self._no_items)]
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = G.as_hff(group)
            # self.stderrh(h)
            self.assertIn(u'global_external_references', group)
            self.assertTrue(len(G) > 0)
            self.assertEqual(len(G), len(group[u'global_external_references']))
            for er in G:
                self.assertEqual(er, adapter.SFFExternalReference.from_hff(
                    group[u'global_external_references/{}'.format(er.id)]))
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            G2 = adapter.SFFGlobalExternalReferenceList.from_hff(h[u'container'])
            self.assertEqual(G, G2)


class TestSFFBiologicalAnnotation(Py23FixTestCase):
    def setUp(self):
        self.name = " ".join(rw.random_words(count=3))
        self.description = li.get_sentence()
        self._no_items = _random_integer(start=2, stop=10)
        self.ii = list(_xrange(self._no_items))
        self.rr = [rw.random_word() for _ in _xrange(self._no_items)]
        self.uu = [rw.random_word() for _ in _xrange(self._no_items)]
        self.aa = [rw.random_word() for _ in _xrange(self._no_items)]
        self.ll = [" ".join(rw.random_words(count=3)) for _ in _xrange(self._no_items)]
        self.dd = [li.get_sentence() for _ in _xrange(self._no_items)]
        self.ee = [adapter.SFFExternalReference(
            resource=self.rr[i],
            url=self.uu[i],
            accession=self.aa[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        self._ee = [emdb_sff.external_reference_type(
            resource=self.rr[i],
            url=self.uu[i],
            accession=self.aa[i],
            label=self.ll[i],
            description=self.dd[i]
        ) for i in _xrange(self._no_items)]
        E = adapter.SFFExternalReferenceList()
        [E.append(e) for e in self.ee]
        _E = emdb_sff.external_referencesType()
        _E.set_ref(self._ee)
        self.external_references = E
        self._external_references = _E
        self.no = _random_integer()

    def test_default(self):
        """Test default settings"""
        b = adapter.SFFBiologicalAnnotation(
            name=self.name,
            description=self.description,
            external_references=self.external_references,
            number_of_instances=self.no,
        )
        self.assertRegex(
            _str(b),
            r"""SFFBiologicalAnnotation\(""" \
            r"""name="{}", description="{}", """ \
            r"""number_of_instances={}, """ \
            r"""external_references=SFFExternalReferenceList\(\[.*\]\)\)""".format(
                self.name,
                self.description,
                self.no
            )
        )
        self.assertEqual(b.name, self.name)
        self.assertEqual(b.description, self.description)
        self.assertEqual(b.number_of_instances, self.no)
        self.assertEqual(b.external_references, self.external_references)

    def test_create_from_gds_type(self):
        """Test that we can create from a gds_type"""
        _b = emdb_sff.biological_annotationType(
            name=self.name,
            description=self.description,
            number_of_instances=self.no,
            external_references=self._external_references
        )
        b = adapter.SFFBiologicalAnnotation.from_gds_type(_b)
        self.assertRegex(
            _str(b),
            r"""SFFBiologicalAnnotation\(""" \
            r"""name="{}", description="{}", """ \
            r"""number_of_instances={}, """ \
            r"""external_references=SFFExternalReferenceList\(\[.*\]\)\)""".format(
                self.name,
                self.description,
                self.no
            )
        )
        self.assertEqual(b.name, self.name)
        self.assertEqual(b.description, self.description)
        self.assertEqual(b.number_of_instances, self.no)
        self.assertEqual(b.external_references, self.external_references)

    def test_as_json(self):
        """Test conversion to and from JSON"""
        # empty case
        b_empty = adapter.SFFBiologicalAnnotation()
        b_json = b_empty.as_json()
        self.assertEqual(b_json, {
            u"name": None,
            u"description": None,
            u"external_references": [],
            u"number_of_instances": 1,
        })
        b2_empty = adapter.SFFBiologicalAnnotation.from_json(b_json)
        self.assertEqual(b_empty, b2_empty)
        # non-empty case
        b_full = adapter.SFFBiologicalAnnotation()
        b_full.name = ' '.join(rw.random_words(count=2))
        b_full.description = li.get_sentence()
        es = adapter.SFFExternalReferenceList()
        no_es = _random_integer(2, 10)
        for _ in _xrange(no_es):
            e = adapter.SFFExternalReference()
            e.resource = rw.random_word()
            e.url = rw.random_word()
            e.accession = rw.random_word()
            e.label = ' '.join(rw.random_words(count=3))
            e.description = li.get_sentence()
            es.append(e)
        b_full.external_references = es
        b_json = b_full.as_json()
        b2_full = adapter.SFFBiologicalAnnotation.from_json(b_json)
        self.assertEqual(b_full, b2_full)

    def test_from_json(self):
        """Test that we can import from JSON"""
        b_json = {'name': 'returns agent', 'description': 'Lacus leopraesent risusdonec tempus congue.',
                  'external_references': [{'id': 0, 'resource': 'listing', 'url': 'antennas', 'accession': 'weddings',
                                           'label': 'times selection deployment',
                                           'description': 'Facilisicurabitur mi sanctus fames dignissim autem.'},
                                          {'id': 1, 'resource': 'basis', 'url': 'leaks', 'accession': 'cups',
                                           'label': 'yaw workloads house', 'description': 'Nequeetiam habitasse.'},
                                          {'id': 2, 'resource': 'chance', 'url': 'theory', 'accession': 'allegation',
                                           'label': 'maps chairwomen flashes',
                                           'description': 'Suscipit eos pulvinar zzril doming dolores.'}]}
        b_full = adapter.SFFBiologicalAnnotation.from_json(b_json)
        self.assertEqual(b_full.name, b_json[u'name'])
        self.assertEqual(b_full.description, b_json[u'description'])
        try:
            self.assertEqual(b_full.number_of_instances, b_json[u'number_of_instances'])
        except KeyError:
            self.assertEqual(b_full.number_of_instances, 1)
        for i, extref in enumerate(b_json[u'external_references']):
            self.assertEqual(b_full.external_references[i].id, extref[u'id'])
            self.assertEqual(b_full.external_references[i].resource, extref[u'resource'])
            self.assertEqual(b_full.external_references[i].url, extref[u'url'])
            self.assertEqual(b_full.external_references[i].accession, extref[u'accession'])
            self.assertEqual(b_full.external_references[i].label, extref[u'label'])
            self.assertEqual(b_full.external_references[i].description, extref[u'description'])

    def test_hff(self):
        """Interconvert to HDF5"""
        # empty case
        b_empty = adapter.SFFBiologicalAnnotation()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = b_empty.as_hff(group)
            self.assertIn(u'biological_annotation', group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            b_empty2 = adapter.SFFBiologicalAnnotation.from_hff(h[u'container'])
            self.assertEqual(b_empty, b_empty2)
        # non-empty case
        b_full = adapter.SFFBiologicalAnnotation()
        b_full.name = ' '.join(rw.random_words(count=2))
        b_full.description = li.get_sentence()
        es = adapter.SFFExternalReferenceList()
        no_es = _random_integer(2, 10)
        for _ in _xrange(no_es):
            e = adapter.SFFExternalReference()
            e.resource = rw.random_word()
            e.url = rw.random_word()
            e.accession = rw.random_word()
            e.label = ' '.join(rw.random_words(count=3))
            e.description = li.get_sentence()
            es.append(e)
        b_full.external_references = es
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = b_full.as_hff(group)
            self.assertIn(u'biological_annotation', group)
            self.assertIn(u'name', group[u'biological_annotation'])
            self.assertEqual(group[u'biological_annotation/name'][()], b_full.name)
            self.assertIn(u'description', group[u'biological_annotation'])
            self.assertEqual(group[u'biological_annotation/description'][()], b_full.description)
            self.assertIn(u'number_of_instances', group[u'biological_annotation'])
            self.assertEqual(group[u'biological_annotation/number_of_instances'][()], b_full.number_of_instances)
            self.assertIn(u'external_references', group[u'biological_annotation'])
            self.assertEqual(len(group[u'biological_annotation/external_references']),
                             len(b_full.external_references))
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            b_full2 = adapter.SFFBiologicalAnnotation.from_hff(h[u'container'])
            self.assertEqual(b_full, b_full2)


class TestSFFThreeDVolume(Py23FixTestCase):
    def setUp(self):
        self.lattice_id = _random_integer()
        self.value = _random_integer()
        self.transform_id = _random_integer()

    def test_default(self):
        """Test default settings"""
        v = adapter.SFFThreeDVolume(
            lattice_id=self.lattice_id,
            value=self.value,
            transform_id=self.transform_id,
        )
        self.assertEqual(
            _str(v),
            """SFFThreeDVolume(lattice_id={}, value={}, transform_id={})""".format(
                self.lattice_id,
                self.value,
                self.transform_id
            )
        )
        self.assertEqual(v.lattice_id, self.lattice_id)
        self.assertEqual(v.value, self.value)
        self.assertEqual(v.transform_id, self.transform_id)

    def test_create_from_gds_type(self):
        """Test that we can create from a gds_type"""
        _v = emdb_sff.three_d_volume_type(
            lattice_id=self.lattice_id,
            value=self.value,
            transform_id=self.transform_id
        )
        v = adapter.SFFThreeDVolume.from_gds_type(_v)
        self.assertEqual(
            _str(v),
            """SFFThreeDVolume(lattice_id={}, value={}, transform_id={})""".format(
                self.lattice_id,
                self.value,
                self.transform_id
            )
        )
        self.assertEqual(v.lattice_id, self.lattice_id)
        self.assertEqual(v.value, self.value)
        self.assertEqual(v.transform_id, self.transform_id)

    def test_json(self):
        lattice_id = _random_integer(start=1)
        value = _random_integer(start=1)
        transform_id = _random_integer(start=0)
        vol_full = adapter.SFFThreeDVolume(lattice_id=lattice_id, value=value, transform_id=transform_id)
        vol_json = vol_full.as_json()
        vol_full2 = adapter.SFFThreeDVolume.from_json(vol_json)
        self.assertEqual(vol_full, vol_full2)
        # empty
        vol_empty = adapter.SFFThreeDVolume()
        vol_empty_json = vol_empty.as_json()
        self.assertIsNone(vol_empty_json[u'lattice_id'])
        self.assertIsNone(vol_empty_json[u'value'])
        vol_empty2 = adapter.SFFThreeDVolume.from_json(vol_empty_json)
        self.assertEqual(vol_empty, vol_empty2)

    def test_hff(self):
        lattice_id = _random_integer(start=1)
        value = _random_integer(start=1)
        transform_id = _random_integer(start=0)
        vol_full = adapter.SFFThreeDVolume(lattice_id=lattice_id, value=value, transform_id=transform_id)
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = vol_full.as_hff(group)
            self.assertIn(u'three_d_volume', group)
            self.assertEqual(group[u'three_d_volume/lattice_id'][()], vol_full.lattice_id)
            self.assertEqual(group[u'three_d_volume/value'][()], vol_full.value)
            self.assertEqual(group[u'three_d_volume/transform_id'][()], vol_full.transform_id)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            vol_full2 = adapter.SFFThreeDVolume.from_hff(h[u'container'])
            self.assertEqual(vol_full, vol_full2)
        # empty
        vol_empty = adapter.SFFThreeDVolume()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = vol_empty.as_hff(group)
            self.assertIn(u'three_d_volume', group)
            self.assertNotIn(u'lattice_id', group[u'three_d_volume'])
            self.assertNotIn(u'value', group[u'three_d_volume'])
            self.assertNotIn(u'transform_id', group[u'three_d_volume'])
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            vol_empty2 = adapter.SFFThreeDVolume.from_hff(h[u'container'])
            self.assertEqual(vol_empty, vol_empty2)


class TestSFFVolumeStructure(Py23FixTestCase):
    def setUp(self):
        self.cols = _random_integer()
        self.rows = _random_integer()
        self.sections = _random_integer()

    def test_default(self):
        """Test default settings"""
        vs = adapter.SFFVolumeStructure(cols=self.cols, rows=self.rows, sections=self.sections)
        self.assertRegex(_str(vs), r"SFFVolumeStructure\(cols.*rows.*sections.*\)")
        self.assertEqual(vs.cols, self.cols)
        self.assertEqual(vs.rows, self.rows)
        self.assertEqual(vs.sections, self.sections)
        self.assertEqual(vs.voxel_count, self.cols * self.rows * self.sections)

    def test_get_set_value(self):
        """Test the .value attribute"""
        vs = adapter.SFFVolumeStructure(cols=self.cols, rows=self.rows, sections=self.sections)
        self.assertEqual(vs.cols, self.cols)
        self.assertEqual(vs.rows, self.rows)
        self.assertEqual(vs.sections, self.sections)
        self.assertEqual(vs.value, (self.cols, self.rows, self.sections))
        _c, _r, _s = _random_integer(), _random_integer(), _random_integer()
        vs.value = _c, _r, _s
        self.assertEqual(vs.value, (_c, _r, _s))
        self.assertEqual(vs.cols, _c)
        self.assertEqual(vs.rows, _r)
        self.assertEqual(vs.sections, _s)

    def test_create_from_gds_type(self):
        """Test that we can create from a gds_type"""
        _vs = emdb_sff.volume_structure_type(cols=self.cols, rows=self.rows, sections=self.sections)
        vs = adapter.SFFVolumeStructure.from_gds_type(_vs)
        self.assertRegex(_str(vs), r"SFFVolumeStructure\(cols.*rows.*sections.*\)")
        self.assertEqual(vs.cols, self.cols)
        self.assertEqual(vs.rows, self.rows)
        self.assertEqual(vs.sections, self.sections)
        self.assertEqual(vs.voxel_count, self.cols * self.rows * self.sections)

    def test_json(self):
        # empty
        s = adapter.SFFVolumeStructure()
        s_json = s.as_json()
        s2 = adapter.SFFVolumeStructure.from_json(s_json)
        self.assertEqual(s, s2)
        # pop'd
        rows, cols, sections = _random_integers(start=100, stop=1000, count=3)
        s = adapter.SFFVolumeStructure(rows=rows, cols=cols, sections=sections)
        s_json = s.as_json()
        s2 = adapter.SFFVolumeStructure.from_json(s_json)
        self.assertEqual(s, s2)

    def test_hff(self):
        # empty
        vs = adapter.SFFVolumeStructure()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = vs.as_hff(group)
            self.assertIn(u'size', group)
            self.assertNotIn(u'size/rows', group)
            self.assertNotIn(u'size/cols', group)
            self.assertNotIn(u'size/sections', group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            vs2 = adapter.SFFVolumeStructure.from_hff(h[u'container'])
            self.assertEqual(vs, vs2)
        # non-empty
        rows, cols, sections = _random_integers(count=3)
        vs = adapter.SFFVolumeStructure(rows=rows, cols=cols, sections=sections)
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = vs.as_hff(group)
            self.assertIn(u'size', group)
            self.assertIn(u'size/rows', group)
            self.assertIn(u'size/cols', group)
            self.assertIn(u'size/sections', group)
            self.assertEqual(group[u'size/rows'][()], rows)
            self.assertEqual(group[u'size/cols'][()], cols)
            self.assertEqual(group[u'size/sections'][()], sections)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            vs2 = adapter.SFFVolumeStructure.from_hff(h[u'container'])
            self.assertEqual(vs, vs2)


class TestSFFVolumeIndex(Py23FixTestCase):
    def setUp(self):
        self.cols = _random_integer()
        self.rows = _random_integer()
        self.sections = _random_integer()

    def test_default(self):
        """Test default settings"""
        vi = adapter.SFFVolumeIndex(cols=self.cols, rows=self.rows, sections=self.sections)
        self.assertRegex(_str(vi), r"SFFVolumeIndex\(rows.*cols.*sections.*\)")
        self.assertEqual(vi.cols, self.cols)
        self.assertEqual(vi.rows, self.rows)
        self.assertEqual(vi.sections, self.sections)

    def test_create_from_gds_type(self):
        """Test that we can create from a gds_type"""
        _vi = emdb_sff.volume_index_type(cols=self.cols, rows=self.rows, sections=self.sections)
        vi = adapter.SFFVolumeIndex.from_gds_type(_vi)
        self.assertRegex(_str(vi), r"SFFVolumeIndex\(rows.*cols.*sections.*\)")
        self.assertEqual(vi.cols, self.cols)
        self.assertEqual(vi.rows, self.rows)
        self.assertEqual(vi.sections, self.sections)

    def test_json(self):
        # empty
        s = adapter.SFFVolumeIndex()
        s_json = s.as_json()
        s2 = adapter.SFFVolumeIndex.from_json(s_json)
        self.assertEqual(s, s2)
        # pop'd
        rows, cols, sections = _random_integers(start=100, stop=1000, count=3)
        s = adapter.SFFVolumeIndex(rows=rows, cols=cols, sections=sections)
        s_json = s.as_json()
        s2 = adapter.SFFVolumeIndex.from_json(s_json)
        self.assertEqual(s, s2)


class TestSFFLattice(Py23FixTestCase):
    def setUp(self):
        adapter.SFFLattice.reset_id()
        self.r, self.c, self.s = _random_integer(start=2, stop=10), _random_integer(start=2, stop=10), _random_integer(
            start=2, stop=10)
        self.l_mode = u'float64'
        self.l_endian = u'little'
        self.l_size = adapter.SFFVolumeStructure(rows=self.r, cols=self.c, sections=self.s)
        self.l_start = adapter.SFFVolumeIndex(rows=0, cols=0, sections=0)
        self.l_data = numpy.random.rand(self.r, self.c, self.s)
        self.l_bytes = adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian)
        self.l_unicode = _decode(self.l_bytes, u'utf-8')

    def tearDown(self):
        adapter.SFFLattice.reset_id()

    def test_create_init_array(self):
        """Test that we can create from a numpy array using __init__"""
        l = adapter.SFFLattice(
            mode=self.l_mode,
            endianness=self.l_endian,
            size=self.l_size,
            start=self.l_start,
            data=self.l_data
        )
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, 0)
        self.assertEqual(l.mode, self.l_mode)
        self.assertEqual(l.endianness, self.l_endian)
        self.assertEqual(l.size.voxel_count, self.r * self.c * self.s)
        self.assertEqual(l.start.value, (0, 0, 0))
        self.assertEqual(l.data, adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian))
        self.assertEqual(l.data_array.flatten().tolist(), self.l_data.flatten().tolist())
        self.assertRegex(
            _str(l),
            r"""SFFLattice\(id=\d+, mode=".*", endianness=".*", size=SFFVolumeStructure\(.*\), start=SFFVolumeIndex\(.*\), data=".*"\)"""
        )
        import sys
        # self.stderr(type(l.data))
        l.export(sys.stderr)

    def test_create_init_bytes(self):
        """Test that we can create from bytes using __init__"""
        l = adapter.SFFLattice(
            mode=self.l_mode,
            endianness=self.l_endian,
            size=self.l_size,
            start=self.l_start,
            data=self.l_bytes
        )
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, 0)
        self.assertEqual(l.mode, self.l_mode)
        self.assertEqual(l.endianness, self.l_endian)
        self.assertEqual(l.size.voxel_count, self.r * self.c * self.s)
        self.assertEqual(l.start.value, (0, 0, 0))
        self.assertEqual(l.data, adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian))
        self.assertEqual(l.data_array.flatten().tolist(), self.l_data.flatten().tolist())
        self.assertRegex(
            _str(l),
            r"""SFFLattice\(id=\d+, mode=".*", endianness=".*", size=SFFVolumeStructure\(.*\), start=SFFVolumeIndex\(.*\), data=".*"\)"""
        )

    def test_create_init_unicode(self):
        """Test that we can create from unicode using __init__"""
        l = adapter.SFFLattice(
            mode=self.l_mode,
            endianness=self.l_endian,
            size=self.l_size,
            start=self.l_start,
            data=self.l_unicode
        )
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, 0)
        self.assertEqual(l.mode, self.l_mode)
        self.assertEqual(l.endianness, self.l_endian)
        self.assertEqual(l.size.voxel_count, self.r * self.c * self.s)
        self.assertEqual(l.start.value, (0, 0, 0))
        self.assertEqual(l.data, adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian))
        self.assertEqual(l.data_array.flatten().tolist(), self.l_data.flatten().tolist())
        self.assertRegex(
            _str(l),
            r"""SFFLattice\(id=\d+, mode=".*", endianness=".*", size=SFFVolumeStructure\(.*\), start=SFFVolumeIndex\(.*\), data=".*"\)"""
        )

    def test_create_classmethod_array(self):
        """Test that we can create an object using the classmethod"""
        l = adapter.SFFLattice.from_array(
            mode=self.l_mode,
            endianness=self.l_endian,
            size=self.l_size,
            start=self.l_start,
            data=self.l_data
        )
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, 0)
        self.assertEqual(l.mode, self.l_mode)
        self.assertEqual(l.endianness, self.l_endian)
        self.assertEqual(l.size.voxel_count, self.r * self.c * self.s)
        self.assertEqual(l.start.value, (0, 0, 0))
        self.assertEqual(_decode(l.data, u'utf-8'), adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian))
        self.assertEqual(l.data_array.flatten().tolist(), self.l_data.flatten().tolist())
        self.stderr(l)
        self.assertRegex(
            _str(l),
            r"""SFFLattice\(id=\d+, mode=".*", endianness=".*", size=SFFVolumeStructure\(.*\), start=SFFVolumeIndex\(.*\), data=".*"\)"""
        )

    def test_create_classmethod_bytes(self):
        """Test that we can create an object using the classmethod"""
        l = adapter.SFFLattice.from_bytes(
            self.l_bytes,
            self.l_size,
            mode=self.l_mode,
            endianness=self.l_endian,
            start=self.l_start,
        )
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, 0)
        self.assertEqual(l.mode, self.l_mode)
        self.assertEqual(l.endianness, self.l_endian)
        self.assertEqual(l.size.voxel_count, self.r * self.c * self.s)
        self.assertEqual(l.start.value, (0, 0, 0))
        self.assertEqual(l.data, adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian))
        self.assertEqual(l.data_array.flatten().tolist(), self.l_data.flatten().tolist())
        self.assertRegex(
            _str(l),
            r"""SFFLattice\(id=\d+, mode=".*", endianness=".*", size=SFFVolumeStructure\(.*\), start=SFFVolumeIndex\(.*\), data=".*"\)"""
        )
        with self.assertRaisesRegex(base.SFFTypeError, r".*is not object of type.*"):
            l = adapter.SFFLattice.from_bytes(
                self.l_bytes,
                (self.r, self.c, self.s),
                mode=self.l_mode,
                endianness=self.l_endian,
                start=self.l_start,
            )

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        r, c, s = _random_integer(start=3, stop=10), _random_integer(start=3, stop=10), _random_integer(start=3,
                                                                                                        stop=10)
        _data = numpy.random.randint(low=0, high=100, size=(r, c, s))
        mode_ = u'uint8'
        _bytes = adapter.SFFLattice._encode(_data, endianness=u'big', mode=mode_)
        _l = emdb_sff.lattice_type(
            mode=mode_,
            endianness=u'big',
            size=emdb_sff.volume_structure_type(cols=c, rows=r, sections=s),
            start=emdb_sff.volume_index_type(cols=0, rows=0, sections=0),
            data=_bytes
        )
        l = adapter.SFFLattice.from_gds_type(_l)
        self.assertTrue(hasattr(l, u'data_array'))

    def test_json(self):
        # empty
        l = adapter.SFFLattice()
        l_json = l.as_json()
        with self.assertRaises(base.SFFTypeError):
            l2 = adapter.SFFLattice.from_json(l_json)
        # self.assertEqual(l, l2)
        # pop'd
        rows, cols, sections = _random_integers(start=2, stop=5, count=3)
        array = numpy.random.randint(0, 20, size=(rows, cols, sections))
        l = adapter.SFFLattice.from_array(array)
        l_json = l.as_json()
        l2 = adapter.SFFLattice.from_json(l_json)
        self.assertEqual(l, l2)

    def test_hff(self):
        # empty case
        l = adapter.SFFLattice()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = l.as_hff(group)
            self.assertIn(u'{}'.format(l.id), group)
            self.assertIn(u'{}/id'.format(l.id), group)
            self.assertIn(u'{}/mode'.format(l.id), group)
            self.assertIn(u'{}/endianness'.format(l.id), group)
            self.assertNotIn(u'{}/size'.format(l.id), group)
            self.assertIn(u'{}/start'.format(l.id), group)
            self.assertNotIn(u'{}/data'.format(l.id), group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            l2 = adapter.SFFLattice.from_hff(h[u'container'])
            self.assertEqual(l, l2)
        # non-empty case
        rows, cols, sections = _random_integers(count=3, start=5, stop=10)
        array = numpy.random.randint(0, 10, size=(rows, cols, sections))
        l = adapter.SFFLattice.from_array(array)
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = l.as_hff(group)
            self.assertIn(u'{}'.format(l.id), group)
            self.assertIn(u'{}/id'.format(l.id), group)
            self.assertIn(u'{}/mode'.format(l.id), group)
            self.assertIn(u'{}/endianness'.format(l.id), group)
            self.assertIn(u'{}/size'.format(l.id), group)
            self.assertIn(u'{}/start'.format(l.id), group)
            self.assertIn(u'{}/data'.format(l.id), group)
            self.assertEqual(group[u'{}/id'.format(l.id)][()], l.id)
            self.assertEqual(group[u'{}/mode'.format(l.id)][()], l.mode)
            self.assertEqual(group[u'{}/endianness'.format(l.id)][()], l.endianness)
            self.assertEqual(adapter.SFFVolumeStructure.from_hff(group[u'{}'.format(l.id)]), l.size)
            self.assertEqual(adapter.SFFVolumeIndex.from_hff(group[u'{}'.format(l.id)]), l.start)
            self.assertEqual(group[u'{}/data'.format(l.id)][()], l.data)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                l2 = adapter.SFFLattice.from_hff(group)
                self.assertEqual(l, l2)


class TestSFFLatticeList(Py23FixTestCase):
    """Test the SFFLatticeList class"""

    @staticmethod
    def generate_sff_data(
            rows=_random_integer(start=10, stop=20),
            cols=_random_integer(start=10, stop=20),
            sections=_random_integer(start=10, stop=20)
    ):
        mode = random.choice(list(adapter.FORMAT_CHARS.keys()))
        endianness = random.choice(list(adapter.ENDIANNESS.keys()))
        size = adapter.SFFVolumeStructure(rows=rows, cols=cols, sections=sections)
        start = adapter.SFFVolumeIndex(rows=0, cols=0, sections=0)
        if re.match(r".*int.*", mode):
            data = numpy.random.randint(0, 100, size=(rows, cols, sections))
        elif re.match(r".*float.*", mode):
            data = numpy.random.rand(rows, cols, sections)
        return mode, endianness, size, start, data

    @staticmethod
    def generate_gds_data(
            rows=_random_integer(start=10, stop=20),
            cols=_random_integer(start=10, stop=20),
            sections=_random_integer(start=10, stop=20)
    ):
        mode = random.choice(list(adapter.FORMAT_CHARS.keys()))
        endianness = random.choice(list(adapter.ENDIANNESS.keys()))
        size = emdb_sff.volume_structure_type(rows=rows, cols=cols, sections=sections)
        start = emdb_sff.volume_index_type(rows=0, cols=0, sections=0)
        if re.match(r".*int.*", mode):
            _data = numpy.random.randint(0, 100, size=(rows, cols, sections))
        elif re.match(r".*float.*", mode):
            _data = numpy.random.rand(rows, cols, sections)
        data = adapter.SFFLattice._encode(_data, mode=mode, endianness=endianness)
        return mode, endianness, size, start, data

    def test_default(self):
        """Test default settings"""
        L = adapter.SFFLatticeList()
        self.assertRegex(
            _str(L),
            r"""SFFLatticeList\(\[.*\]\)"""
        )
        self.assertEqual(len(L), 0)
        _no_items = _random_integer(start=2, stop=5)
        for _ in _xrange(_no_items):
            _mode, _endianness, _size, _start, _data = TestSFFLatticeList.generate_sff_data()
            L.append(
                adapter.SFFLattice(
                    mode=_mode,
                    endianness=_endianness,
                    size=_size,
                    start=_start,
                    data=_data
                )
            )
        self.assertRegex(
            _str(L),
            r"""SFFLatticeList\(\[SFFLattice\(.*\]\)"""
        )
        self.assertEqual(len(L), _no_items)
        self.assertEqual(list(L.get_ids()), list(_xrange(_no_items)))
        l_id = random.choice(list(L.get_ids()))
        l = L.get_by_id(l_id)
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, l_id)
        self.assertIn(l.mode, list(adapter.FORMAT_CHARS.keys()))
        self.assertIn(l.endianness, list(adapter.ENDIANNESS.keys()))
        self.assertIsInstance(l.size, adapter.SFFVolumeStructure)
        self.assertIsInstance(l.start, adapter.SFFVolumeIndex)
        self.assertIsInstance(l.data, _str)
        self.assertIsInstance(l.data_array, numpy.ndarray)
        self.assertTrue(len(l.data) > 0)

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _L = emdb_sff.lattice_listType()
        _no_items = _random_integer(start=2, stop=5)
        _l = list()
        for i in _xrange(_no_items):
            _mode, _endianness, _size, _start, _data = TestSFFLatticeList.generate_gds_data()
            _l.append(
                emdb_sff.lattice_type(
                    id=i,
                    mode=_mode,
                    endianness=_endianness,
                    size=_size,
                    start=_start,
                    data=_data
                )
            )
        _L.set_lattice(_l)
        L = adapter.SFFLatticeList.from_gds_type(_L)
        self.assertRegex(
            _str(L),
            r"""SFFLatticeList\(\[SFFLattice\(.*\]\)"""
        )
        self.assertEqual(len(L), _no_items)
        self.assertEqual(list(L.get_ids()), list(_xrange(_no_items)))
        l_id = random.choice(list(L.get_ids()))
        l = L.get_by_id(l_id)
        self.assertIsInstance(l, adapter.SFFLattice)
        self.assertEqual(l.id, l_id)
        self.assertIn(l.mode, list(adapter.FORMAT_CHARS.keys()))
        self.assertIn(l.endianness, list(adapter.ENDIANNESS.keys()))
        self.assertIsInstance(l.size, adapter.SFFVolumeStructure)
        self.assertIsInstance(l.start, adapter.SFFVolumeIndex)
        self.assertIsInstance(l.data, _str)
        self.assertIsInstance(l.data_array, numpy.ndarray)
        self.assertTrue(len(l.data) > 0)

    def test_json(self):
        """Test that we can convert back and forth into JSON"""
        L = adapter.SFFLatticeList()
        _no_lats = _random_integer(start=2, stop=5)
        for _ in _xrange(_no_lats):
            _mode, _endianness, _size, _start, _data = TestSFFLatticeList.generate_sff_data()
            L.append(
                adapter.SFFLattice(
                    mode=_mode,
                    endianness=_endianness,
                    size=_size,
                    start=_start,
                    data=_data
                )
            )
        L_json = L.as_json()
        L2 = adapter.SFFLatticeList.from_json(L_json)
        self.assertEqual(L, L2)

    def test_hff(self):
        # empty case
        L = adapter.SFFLatticeList()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = L.as_hff(group)
            self.assertIn(u'lattice_list', group)
            self.assertEqual(len(group[u'lattice_list']), 0)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            L2 = adapter.SFFLatticeList.from_hff(h[u'container'])
            self.assertEqual(L, L2)
        # non-empty case
        L = adapter.SFFLatticeList()
        _no_lats = _random_integer(start=2, stop=15)
        for _ in _xrange(_no_lats):
            _mode, _endianness, _size, _start, _data = TestSFFLatticeList.generate_sff_data()
            L.append(
                adapter.SFFLattice(
                    mode=_mode,
                    endianness=_endianness,
                    size=_size,
                    start=_start,
                    data=_data
                )
            )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = L.as_hff(group)
            self.assertIn(u'lattice_list', group)
            self.assertEqual(len(group[u'lattice_list']), len(L))
            for i in _xrange(_no_lats):
                self.assertEqual(L[i].mode, _decode(group[u'lattice_list'][_str(i)][u'mode'][()], 'utf-8'))
                self.assertEqual(L[i].endianness, _decode(group[u'lattice_list'][_str(i)][u'endianness'][()], 'utf-8'))
                self.assertEqual(L[i].size, adapter.SFFVolumeStructure.from_hff(group[u'lattice_list/{}'.format(i)]))
                self.assertEqual(L[i].start, adapter.SFFVolumeIndex.from_hff(group[u'lattice_list/{}'.format(i)]))
                self.assertEqual(L[i].data, group[u'lattice_list'][_str(i)][u'data'][()])
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            L2 = adapter.SFFLatticeList.from_hff(h[u'container'])
            self.assertEqual(L, L2)


class TestSFFVertices(Py23FixTestCase):
    """SFFVertices tests"""

    def setUp(self):
        self.num_vertices = _random_integer(start=2, stop=10)
        self.mode = u'float64'
        self.endian = u'little'
        self.data = numpy.random.rand(self.num_vertices, 3)
        self.bytes = adapter.SFFVertices._encode(self.data, mode=self.mode, endianness=self.endian)
        self.unicode = _decode(self.bytes, u'utf-8')

    def test_create_init_array(self):
        """Default configuration"""
        v = adapter.SFFVertices(
            num_vertices=self.num_vertices,
            mode=self.mode,
            endianness=self.endian,
            data=self.data
        )
        self.assertIsInstance(v, adapter.SFFVertices)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertIsInstance(v.data, _str)
        self.assertEqual(v.data, adapter.SFFVertices._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFVertices(num_vertices={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_vertices,
                self.mode,
                self.endian,
                _data
            )
        )
        with self.assertRaisesRegex(ValueError, r".invalid dimensions.*"):
            adapter.SFFVertices(
                num_vertices=self.num_vertices,
                data=numpy.random.rand(self.num_vertices, 4)
            )

    def test_create_init_bytes(self):
        """Test that we can create from bytes using __init__"""
        v = adapter.SFFVertices(
            num_vertices=self.num_vertices,
            mode=self.mode,
            endianness=self.endian,
            data=self.bytes
        )
        self.assertIsInstance(v, adapter.SFFVertices)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertEqual(v.data, adapter.SFFVertices._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFVertices(num_vertices={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_vertices,
                self.mode,
                self.endian,
                _data
            )
        )
        with self.assertRaisesRegex(ValueError, r".*mismatch.*stated.*retrieved.*"):
            v = adapter.SFFVertices(
                num_vertices=self.num_vertices * 2,
                mode=self.mode,
                endianness=self.endian,
                data=self.bytes
            )

    def test_create_init_unicode(self):
        """Test that we can create from unicode using __init__"""
        v = adapter.SFFVertices(
            num_vertices=self.num_vertices,
            mode=self.mode,
            endianness=self.endian,
            data=self.unicode
        )
        self.assertIsInstance(v, adapter.SFFVertices)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertEqual(v.data, adapter.SFFVertices._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFVertices(num_vertices={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_vertices,
                self.mode,
                self.endian,
                _data
            )
        )
        with self.assertRaisesRegex(ValueError, r".*mismatch.*stated.*retrieved.*"):
            v = adapter.SFFVertices(
                num_vertices=self.num_vertices * 2,
                mode=self.mode,
                endianness=self.endian,
                data=self.bytes
            )

    def test_create_classmethod_array(self):
        """Test that we can create an object using the classmethod"""
        v = adapter.SFFVertices.from_array(
            data=self.data,
            mode=self.mode,
            endianness=self.endian,
        )
        self.assertIsInstance(v, adapter.SFFVertices)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertEqual(v.data, adapter.SFFVertices._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFVertices(num_vertices={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_vertices,
                self.mode,
                self.endian,
                _data,
            )
        )

    def test_create_classmethod_bytes(self):
        """Test that we can create an object using the classmethod"""
        v = adapter.SFFVertices.from_bytes(
            self.bytes,
            self.num_vertices,
            mode=self.mode,
            endianness=self.endian,
        )
        self.assertIsInstance(v, adapter.SFFVertices)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertEqual(v.data, adapter.SFFVertices._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFVertices(num_vertices={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_vertices,
                self.mode,
                self.endian,
                _data
            )
        )

    def test_dict_interface(self):
        """Test the dictionary interface"""
        v = adapter.SFFVertices(
            num_vertices=self.num_vertices,
            mode=self.mode,
            endianness=self.endian,
            data=self.data
        )
        index = _random_integer(start=0, stop=self.num_vertices - 1)
        self.assertTrue(numpy.array_equal(self.data[index], v[index]))

    def test_from_gds_type(self):
        """Test that we can create an object direct from gds_type"""
        _v = emdb_sff.vertices_type(
            num_vertices=self.num_vertices,
            mode=self.mode,
            endianness=self.endian,
            data=self.bytes
        )
        v = adapter.SFFVertices.from_gds_type(_v)
        self.assertEqual(v.num_vertices, self.num_vertices)
        self.assertTrue(hasattr(v, u'data_array'))
        self.assertIsInstance(v.data_array, numpy.ndarray)

    def test_json(self):
        """Interconversion to JSON"""
        v = adapter.SFFVertices(
            num_vertices=self.num_vertices,
            mode=self.mode,
            endianness=self.endian,
            data=self.data
        )
        v_json = v.as_json()
        self.assertEqual(v_json, {
            u'num_vertices': self.num_vertices,
            u'mode': self.mode,
            u'endianness': self.endian,
            u'data': _decode(self.bytes, 'ASCII'),
        })
        v2 = adapter.SFFVertices.from_json(v_json)
        self.assertEqual(v, v2)

    def test_hff(self):
        # empty
        v = adapter.SFFVertices()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = v.as_hff(group)
            self.assertIn(u'vertices', group)
            self.assertNotIn(u'vertices/num_vertices', group)
            self.assertIn(u'vertices/mode', group)
            self.assertIn(u'vertices/endianness', group)
            self.assertNotIn(u'vertices/data', group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            v2 = adapter.SFFVertices.from_hff(h[u'container'])
            self.assertEqual(v, v2)
        # non-empty
        v = adapter.SFFVertices(
            num_vertices=self.num_vertices,
            mode=self.mode,
            endianness=self.endian,
            data=self.data
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = v.as_hff(group)
            self.assertIn(u'vertices', group)
            self.assertIn(u'vertices/num_vertices', group)
            self.assertEqual(group[u'vertices/num_vertices'][()], v.num_vertices)
            self.assertIn(u'vertices/mode', group)
            self.assertEqual(_decode(group[u'vertices/mode'][()], 'utf-8'), v.mode)
            self.assertIn(u'vertices/endianness', group)
            self.assertEqual(_decode(group[u'vertices/endianness'][()], 'utf-8'), v.endianness)
            self.assertIn(u'vertices/data', group)
            self.assertEqual(group[u'vertices/data'][()], v.data)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            v2 = adapter.SFFVertices.from_hff(h[u'container'])
            self.assertEqual(v, v2)


class TestSFFNormals(Py23FixTestCase):
    """SFFNormals tests"""

    def setUp(self):
        self.num_normals = _random_integer(start=2, stop=10)
        self.mode = u'float64'
        self.endian = u'little'
        self.data = numpy.random.rand(self.num_normals, 3)
        self.bytes = adapter.SFFNormals._encode(self.data, mode=self.mode, endianness=self.endian)
        self.unicode = _decode(self.bytes, u'utf-8')

    def test_create_init_array(self):
        """Default configuration"""
        v = adapter.SFFNormals(
            num_normals=self.num_normals,
            mode=self.mode,
            endianness=self.endian,
            data=self.data
        )
        self.assertIsInstance(v, adapter.SFFNormals)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertIsInstance(v.data, _str)
        self.assertEqual(v.data, adapter.SFFNormals._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFNormals(num_normals={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_normals,
                self.mode,
                self.endian,
                _data
            )
        )
        with self.assertRaisesRegex(ValueError, r".invalid dimensions.*"):
            adapter.SFFNormals(
                num_normals=self.num_normals,
                data=numpy.random.rand(self.num_normals, 4)
            )

    def test_create_init_bytes(self):
        """Test that we can create from bytes using __init__"""
        v = adapter.SFFNormals(
            num_normals=self.num_normals,
            mode=self.mode,
            endianness=self.endian,
            data=self.bytes
        )
        self.assertIsInstance(v, adapter.SFFNormals)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertEqual(v.data, adapter.SFFNormals._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFNormals(num_normals={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_normals,
                self.mode,
                self.endian,
                _data
            )
        )
        with self.assertRaisesRegex(ValueError, r".*mismatch.*stated.*retrieved.*"):
            v = adapter.SFFNormals(
                num_normals=self.num_normals * 2,
                mode=self.mode,
                endianness=self.endian,
                data=self.bytes
            )

    def test_create_init_unicode(self):
        """Test that we can create from unicode using __init__"""
        v = adapter.SFFNormals(
            num_normals=self.num_normals,
            mode=self.mode,
            endianness=self.endian,
            data=self.unicode
        )
        self.assertIsInstance(v, adapter.SFFNormals)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertEqual(v.data, adapter.SFFNormals._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFNormals(num_normals={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_normals,
                self.mode,
                self.endian,
                _data
            )
        )
        with self.assertRaisesRegex(ValueError, r".*mismatch.*stated.*retrieved.*"):
            v = adapter.SFFNormals(
                num_normals=self.num_normals * 2,
                mode=self.mode,
                endianness=self.endian,
                data=self.bytes
            )

    def test_create_classmethod_array(self):
        """Test that we can create an object using the classmethod"""
        v = adapter.SFFNormals.from_array(
            data=self.data,
            mode=self.mode,
            endianness=self.endian,
        )
        self.assertIsInstance(v, adapter.SFFNormals)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertEqual(v.data, adapter.SFFNormals._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFNormals(num_normals={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_normals,
                self.mode,
                self.endian,
                _data,
            )
        )

    def test_create_classmethod_bytes(self):
        """Test that we can create an object using the classmethod"""
        v = adapter.SFFNormals.from_bytes(
            self.bytes,
            self.num_normals,
            mode=self.mode,
            endianness=self.endian,
        )
        self.assertIsInstance(v, adapter.SFFNormals)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertEqual(v.data, adapter.SFFNormals._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFNormals(num_normals={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_normals,
                self.mode,
                self.endian,
                _data
            )
        )

    def test_dict_interface(self):
        """Test the dictionary interface"""
        v = adapter.SFFNormals(
            num_normals=self.num_normals,
            mode=self.mode,
            endianness=self.endian,
            data=self.data
        )
        index = _random_integer(start=0, stop=self.num_normals - 1)
        self.assertTrue(numpy.array_equal(self.data[index], v[index]))

    def test_from_gds_type(self):
        """Test that we can create an object direct from gds_type"""
        _n = emdb_sff.normals_type(
            num_normals=self.num_normals,
            mode=self.mode,
            endianness=self.endian,
            data=self.bytes
        )
        n = adapter.SFFNormals.from_gds_type(_n)
        self.assertEqual(n.num_normals, self.num_normals)
        self.assertTrue(hasattr(n, u'data_array'))
        self.assertIsInstance(n.data_array, numpy.ndarray)

    def test_json(self):
        """Interconversion to JSON"""
        n = adapter.SFFNormals(
            num_normals=self.num_normals,
            mode=self.mode,
            endianness=self.endian,
            data=self.data
        )
        n_json = n.as_json()
        self.assertEqual(n_json, {
            u'num_normals': self.num_normals,
            u'mode': self.mode,
            u'endianness': self.endian,
            u'data': _decode(self.bytes, 'ASCII'),
        })
        n2 = adapter.SFFNormals.from_json(n_json)
        self.assertEqual(n, n2)

    def test_hff(self):
        # empty
        n = adapter.SFFNormals()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = n.as_hff(group)
            self.assertIn(u'normals', group)
            self.assertNotIn(u'normals/num_normals', group)
            self.assertIn(u'normals/mode', group)
            self.assertIn(u'normals/endianness', group)
            self.assertNotIn(u'normals/data', group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            n2 = adapter.SFFNormals.from_hff(h[u'container'])
            self.assertEqual(n, n2)
        # non-empty
        n = adapter.SFFNormals(
            num_normals=self.num_normals,
            mode=self.mode,
            endianness=self.endian,
            data=self.data
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = n.as_hff(group)
            self.assertIn(u'normals', group)
            self.assertIn(u'normals/num_normals', group)
            self.assertEqual(group[u'normals/num_normals'][()], n.num_normals)
            self.assertIn(u'normals/mode', group)
            self.assertEqual(_decode(group[u'normals/mode'][()], 'utf-8'), n.mode)
            self.assertIn(u'normals/endianness', group)
            self.assertEqual(_decode(group[u'normals/endianness'][()], 'utf-8'), n.endianness)
            self.assertIn(u'normals/data', group)
            self.assertEqual(group[u'normals/data'][()], n.data)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            n2 = adapter.SFFNormals.from_hff(h[u'container'])
            self.assertEqual(n, n2)


class TestSFFTriangles(Py23FixTestCase):
    """SFFTriangles tests"""

    def setUp(self):
        self.num_triangles = _random_integer(start=2, stop=10)
        self.mode = u'uint32'
        self.endian = u'little'
        self.data = numpy.random.randint(0, 100, size=(self.num_triangles, 3))
        self.bytes = adapter.SFFTriangles._encode(self.data, mode=self.mode, endianness=self.endian)
        self.unicode = _decode(self.bytes, u'utf-8')

    def test_create_init_array(self):
        """Default configuration"""
        v = adapter.SFFTriangles(
            num_triangles=self.num_triangles,
            mode=self.mode,
            endianness=self.endian,
            data=self.data
        )
        self.assertIsInstance(v, adapter.SFFTriangles)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertIsInstance(v.data, _str)
        self.assertEqual(v.data, adapter.SFFTriangles._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFTriangles(num_triangles={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_triangles,
                self.mode,
                self.endian,
                _data
            )
        )
        with self.assertRaisesRegex(ValueError, r".invalid dimensions.*"):
            adapter.SFFTriangles(
                num_triangles=self.num_triangles,
                data=numpy.random.rand(self.num_triangles, 4)
            )

    def test_create_init_bytes(self):
        """Test that we can create from bytes using __init__"""
        v = adapter.SFFTriangles(
            num_triangles=self.num_triangles,
            mode=self.mode,
            endianness=self.endian,
            data=self.bytes
        )
        self.assertIsInstance(v, adapter.SFFTriangles)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertEqual(v.data, adapter.SFFTriangles._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFTriangles(num_triangles={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_triangles,
                self.mode,
                self.endian,
                _data
            )
        )
        with self.assertRaisesRegex(ValueError, r".*mismatch.*stated.*retrieved.*"):
            v = adapter.SFFTriangles(
                num_triangles=self.num_triangles * 2,
                mode=self.mode,
                endianness=self.endian,
                data=self.bytes
            )

    def test_create_init_unicode(self):
        """Test that we can create from unicode using __init__"""
        v = adapter.SFFTriangles(
            num_triangles=self.num_triangles,
            mode=self.mode,
            endianness=self.endian,
            data=self.unicode
        )
        self.assertIsInstance(v, adapter.SFFTriangles)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertEqual(v.data, adapter.SFFTriangles._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFTriangles(num_triangles={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_triangles,
                self.mode,
                self.endian,
                _data,
            )
        )
        with self.assertRaisesRegex(ValueError, r".*mismatch.*stated.*retrieved.*"):
            v = adapter.SFFTriangles(
                num_triangles=self.num_triangles * 2,
                mode=self.mode,
                endianness=self.endian,
                data=self.bytes
            )

    def test_create_classmethod_array(self):
        """Test that we can create an object using the classmethod"""
        v = adapter.SFFTriangles.from_array(
            data=self.data,
            mode=self.mode,
            endianness=self.endian,
        )
        self.assertIsInstance(v, adapter.SFFTriangles)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertEqual(v.data, adapter.SFFTriangles._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFTriangles(num_triangles={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_triangles,
                self.mode,
                self.endian,
                _data,
            )
        )

    def test_create_classmethod_bytes(self):
        """Test that we can create an object using the classmethod"""
        v = adapter.SFFTriangles.from_bytes(
            self.bytes,
            self.num_triangles,
            mode=self.mode,
            endianness=self.endian,
        )
        self.assertIsInstance(v, adapter.SFFTriangles)
        self.assertEqual(v.mode, self.mode)
        self.assertEqual(v.endianness, self.endian)
        self.assertEqual(v.data, adapter.SFFTriangles._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        if len(v.data) < 100:
            _data = _decode(v.data, u"utf-8")
        else:
            _data = _decode(v.data[:100] + u"...", u"utf-8")
        self.assertEqual(
            _str(v),
            u"""SFFTriangles(num_triangles={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_triangles,
                self.mode,
                self.endian,
                _data
            )
        )

    def test_dict_interface(self):
        """Test the dictionary interface"""
        v = adapter.SFFTriangles(
            num_triangles=self.num_triangles,
            mode=self.mode,
            endianness=self.endian,
            data=self.data
        )
        index = _random_integer(start=0, stop=self.num_triangles - 1)
        self.assertTrue(numpy.array_equal(self.data[index], v[index]))

    def test_from_gds_type(self):
        """Test that we can create an object direct from gds_type"""
        _t = emdb_sff.triangles_type(
            num_triangles=self.num_triangles,
            mode=self.mode,
            endianness=self.endian,
            data=self.bytes
        )
        t = adapter.SFFTriangles.from_gds_type(_t)
        self.assertTrue(hasattr(t, u'data_array'))
        self.assertIsInstance(t.data_array, numpy.ndarray)

    def test_json(self):
        """Interconversion to JSON"""
        t = adapter.SFFTriangles(
            num_triangles=self.num_triangles,
            mode=self.mode,
            endianness=self.endian,
            data=self.data
        )
        t_json = t.as_json()
        self.assertEqual(t_json, {
            u'num_triangles': self.num_triangles,
            u'mode': self.mode,
            u'endianness': self.endian,
            u'data': _decode(self.bytes, 'ASCII'),
        })
        t2 = adapter.SFFTriangles.from_json(t_json)
        self.assertEqual(t, t2)

    def test_hff(self):
        # empty
        n = adapter.SFFTriangles()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = n.as_hff(group)
            self.assertIn(u'triangles', group)
            self.assertNotIn(u'triangles/num_triangles', group)
            self.assertIn(u'triangles/mode', group)
            self.assertIn(u'triangles/endianness', group)
            self.assertNotIn(u'triangles/data', group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            n2 = adapter.SFFTriangles.from_hff(h[u'container'])
            self.assertEqual(n, n2)
        # non-empty
        n = adapter.SFFTriangles(
            num_triangles=self.num_triangles,
            mode=self.mode,
            endianness=self.endian,
            data=self.data
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = n.as_hff(group)
            self.assertIn(u'triangles', group)
            self.assertIn(u'triangles/num_triangles', group)
            self.assertEqual(group[u'triangles/num_triangles'][()], n.num_triangles)
            self.assertIn(u'triangles/mode', group)
            self.assertEqual(_decode(group[u'triangles/mode'][()], 'utf-8'), n.mode)
            self.assertIn(u'triangles/endianness', group)
            self.assertEqual(_decode(group[u'triangles/endianness'][()], 'utf-8'), n.endianness)
            self.assertIn(u'triangles/data', group)
            self.assertEqual(group[u'triangles/data'][()], n.data)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            n2 = adapter.SFFTriangles.from_hff(h[u'container'])
            self.assertEqual(n, n2)


class TestSFFMesh(Py23FixTestCase):
    """Test the SFFMesh class"""

    def setUp(self):
        self.num_vertices = _random_integer(start=3, stop=10)
        self.vertices_data = numpy.random.rand(self.num_vertices, 3)
        self.vertices_bytes = adapter.SFFVertices._encode(self.vertices_data)
        self.normals_data = numpy.random.rand(self.num_vertices, 3)
        self.normals_bytes = adapter.SFFNormals._encode(self.normals_data)
        self.triangles_data = numpy.random.randint(0, self.num_vertices - 1, size=(self.num_vertices, 3))
        self.triangles_bytes = adapter.SFFTriangles._encode(self.triangles_data, mode=u'uint32')

    def tearDown(self):
        adapter.SFFMesh.reset_id()

    def test_default(self):
        """Test default operation"""
        m = adapter.SFFMesh(
            vertices=adapter.SFFVertices.from_array(self.vertices_data),
            normals=adapter.SFFNormals.from_array(self.normals_data),
            triangles=adapter.SFFTriangles.from_array(self.triangles_data)
        )
        self.assertEqual(
            _str(m),
            u"""SFFMesh(id={}, vertices={}, normals={}, triangles={})""".format(
                m.id,
                m.vertices,
                m.normals,
                m.triangles,
            )
        )
        self.assertEqual(m.id, 0)
        self.assertTrue(numpy.allclose(m.vertices.data_array, self.vertices_data))
        self.assertTrue(numpy.allclose(m.normals.data_array, self.normals_data))
        self.assertTrue(numpy.allclose(m.triangles.data_array, self.triangles_data))
        with self.assertRaisesRegex(ValueError, r".*vertex list and normal list are of different lengths.*"):
            m = adapter.SFFMesh(
                vertices=adapter.SFFVertices.from_array(self.vertices_data),
                normals=adapter.SFFNormals.from_array(self.normals_data[:-1]),
                triangles=adapter.SFFTriangles.from_array(self.triangles_data)
            )

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _v = emdb_sff.vertices_type(
            num_vertices=self.num_vertices,
            mode=adapter.SFFVertices.default_mode,
            endianness=adapter.SFFVertices.default_endianness,
            data=self.vertices_bytes,
        )
        _n = emdb_sff.normals_type(
            num_normals=self.num_vertices,
            mode=adapter.SFFNormals.default_mode,
            endianness=adapter.SFFNormals.default_endianness,
            data=self.normals_bytes,
        )
        _t = emdb_sff.triangles_type(
            num_triangles=self.num_vertices,
            mode=adapter.SFFTriangles.default_mode,
            endianness=adapter.SFFTriangles.default_endianness,
            data=self.triangles_bytes,
        )
        _m = emdb_sff.mesh_type(
            vertices=_v,
            normals=_n,
            triangles=_t
        )
        m = adapter.SFFMesh.from_gds_type(_m)
        self.assertRegex(
            _str(m),
            r"""SFFMesh\(id=(\d+|None), vertices=SFFVertices\(.*\), normals=SFFNormals\(.*\), triangles=SFFTriangles\(.*\)\)"""
        )
        self.assertIsNone(m.id)
        self.assertEqual(m.vertices, adapter.SFFVertices.from_gds_type(_v))
        self.assertEqual(m.normals, adapter.SFFNormals.from_gds_type(_n))
        self.assertEqual(m.triangles, adapter.SFFTriangles.from_gds_type(_t))
        self.assertTrue(numpy.allclose(m.vertices.data_array, self.vertices_data))
        self.assertTrue(numpy.allclose(m.normals.data_array, self.normals_data))
        self.assertTrue(numpy.allclose(m.triangles.data_array, self.triangles_data))

    def test_json(self):
        """Interconvert to JSON"""
        m = adapter.SFFMesh(
            vertices=adapter.SFFVertices.from_array(self.vertices_data),
            normals=adapter.SFFNormals.from_array(self.normals_data),
            triangles=adapter.SFFTriangles.from_array(self.triangles_data)
        )
        m_json = m.as_json()
        self.assertEqual(m_json, {
            u'id': m.id,
            u'vertices': m.vertices.as_json(),
            u'normals': m.normals.as_json(),
            u'triangles': m.triangles.as_json()
        })
        m2 = adapter.SFFMesh.from_json(m_json)
        self.assertEqual(m, m2)

    def test_hff(self):
        # empty
        m = adapter.SFFMesh()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = m.as_hff(group)
            self.assertIn(u'{}'.format(m.id), group)
            self.assertIn(u'{}/id'.format(m.id), group)
            self.assertNotIn(u'{}/vertices'.format(m.id), group)
            self.assertNotIn(u'{}/normals'.format(m.id), group)
            self.assertNotIn(u'{}/triangles'.format(m.id), group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                m2 = adapter.SFFMesh.from_hff(group)
                self.assertEqual(m, m2)
        # non-empty
        m = adapter.SFFMesh(
            vertices=adapter.SFFVertices.from_array(self.vertices_data),
            normals=adapter.SFFNormals.from_array(self.normals_data),
            triangles=adapter.SFFTriangles.from_array(self.triangles_data)
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = m.as_hff(group)
            self.assertIn(u'{}'.format(m.id), group)
            self.assertIn(u'{}/id'.format(m.id), group)
            self.assertIn(u'{}/vertices'.format(m.id), group)
            self.assertIn(u'{}/normals'.format(m.id), group)
            self.assertIn(u'{}/triangles'.format(m.id), group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                m2 = adapter.SFFMesh.from_hff(group)
                self.assertEqual(m, m2)


class TestSFFMeshList(Py23FixTestCase):
    """Test the SFFMeshList class"""

    def tearDown(self):
        adapter.SFFMesh.reset_id()

    @staticmethod
    def generate_sff_data(num_vertices=_random_integer(start=2, stop=20),
                          num_triangles=_random_integer(start=2, stop=20)):
        vertices = adapter.SFFVertices(
            num_vertices=num_vertices,
            data=numpy.random.rand(num_vertices, 3),
        )
        triangles = adapter.SFFTriangles(
            num_triangles=num_triangles,
            data=numpy.random.randint(0, num_triangles - 1, size=(num_triangles, 3))
        )
        return vertices, triangles

    @staticmethod
    def generate_gds_data(num_vertices=_random_integer(start=2, stop=20),
                          num_triangles=_random_integer(start=2, stop=20)):
        vertices = emdb_sff.vertices_type(
            num_vertices=num_vertices,
            mode=u'float32',
            endianness=u'little',
            data=adapter.SFFVertices._encode(
                numpy.random.rand(num_vertices, 3),
                mode=u'float32',
                endianness=u'little',
            )
        )
        triangles = emdb_sff.triangles_type(
            num_triangles=num_triangles,
            mode=u'uint32',
            endianness=u'little',
            data=adapter.SFFTriangles._encode(
                numpy.random.randint(0, num_triangles - 1, size=(num_triangles, 3)),
                mode=u'uint32',
                endianness=u'little',
            )
        )
        return vertices, triangles

    def test_default(self):
        """Test default settings"""
        _no_items = _random_integer(start=2, stop=10)
        M = adapter.SFFMeshList()
        for _ in _xrange(_no_items):
            vs, ts = TestSFFMeshList.generate_sff_data()
            M.append(
                adapter.SFFMesh(
                    vertices=vs,
                    triangles=ts
                )
            )
        self.assertRegex(
            _str(M),
            r"""SFFMeshList\(\[.*\]\)"""
        )
        self.assertEqual(len(M), _no_items)
        self.assertEqual(list(M.get_ids()), list(_xrange(_no_items)))
        m_id = random.choice(list(M.get_ids()))
        m = M.get_by_id(m_id)
        self.assertIsInstance(m, adapter.SFFMesh)
        self.assertEqual(m.id, m_id)
        self.assertTrue(m.vertices.num_vertices > 0)
        self.assertTrue(m.triangles.num_triangles > 0)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _no_items = _random_integer(start=2, stop=10)
        _M = emdb_sff.mesh_listType()
        for i in _xrange(_no_items):
            vs, ts = TestSFFMeshList.generate_gds_data()
            _M.add_mesh(
                emdb_sff.mesh_type(
                    id=i, vertices=vs, triangles=ts
                )
            )
        M = adapter.SFFMeshList.from_gds_type(_M)
        self.assertRegex(
            _str(M),
            r"""SFFMeshList\(\[.*\]\)"""
        )
        self.assertEqual(len(M), _no_items)
        self.assertEqual(list(M.get_ids()), list(_xrange(_no_items)))
        m_id = random.choice(list(M.get_ids()))
        m = M.get_by_id(m_id)
        self.assertIsInstance(m, adapter.SFFMesh)
        self.assertEqual(m.id, m_id)
        self.assertTrue(m.vertices.num_vertices > 0)
        self.assertTrue(m.triangles.num_triangles > 0)

    def test_json(self):
        """Interconvert to JSON"""
        _no_items = _random_integer(start=2, stop=10)
        M = adapter.SFFMeshList()
        for _ in _xrange(_no_items):
            vs, ts = TestSFFMeshList.generate_sff_data()
            M.append(
                adapter.SFFMesh(
                    vertices=vs,
                    triangles=ts
                )
            )
        M_json = M.as_json()
        self.assertEqual(M_json, [
            {
                u'id': m.id,
                u'vertices': m.vertices.as_json(),
                u'normals': None,
                u'triangles': m.triangles.as_json()
            } for m in M
        ])
        M2 = adapter.SFFMeshList.from_json(M_json)
        self.assertEqual(M, M2)

    def test_hff(self):
        """Interconvert to HDF5"""
        # empty
        M = adapter.SFFMeshList()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = M.as_hff(group)
            self.assertIn(u'mesh_list', group)
            self.assertEqual(len(group[u'mesh_list']), 0)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            M2 = adapter.SFFMeshList.from_hff(h[u'container'])
            self.assertEqual(M, M2)
        # non-empty
        _no_items = _random_integer(start=2, stop=14)
        M = adapter.SFFMeshList()
        for _ in _xrange(_no_items):
            vs, ts = TestSFFMeshList.generate_sff_data()
            M.append(
                adapter.SFFMesh(
                    vertices=vs,
                    triangles=ts
                )
            )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = M.as_hff(group)
            self.assertIn(u'mesh_list', group)
            self.assertEqual(len(group[u'mesh_list']), len(M))
            # check that each mesh is exactly the same as in the HDF5 file
            for i in _xrange(_no_items):
                self.assertEqual(M[i], adapter.SFFMesh.from_hff(group[u'mesh_list/{}'.format(i)]))
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            M2 = adapter.SFFMeshList.from_hff(h[u'container'])
            self.assertEqual(M, M2)


class TestSFFBoundingBox(Py23FixTestCase):
    """Test the SFFBoundingBox class"""

    def test_default(self):
        """Test default settings"""
        B = adapter.SFFBoundingBox()
        self.assertRegex(
            _str(B),
            r"""SFFBoundingBox\(xmin={}, xmax={}, ymin={}, ymax={}, zmin={}, zmax={}\)""".format(
                B.xmin, B.xmax,
                B.ymin, B.ymax,
                B.zmin, B.zmax,
            )
        )
        self.assertEqual(B.xmin, 0)
        self.assertIsNone(B.xmax)
        self.assertEqual(B.ymin, 0)
        self.assertIsNone(B.ymax)
        self.assertEqual(B.zmin, 0)
        self.assertIsNone(B.zmax)
        _xmin = _random_float(1)
        _xmax = _random_float(1000)
        _ymin = _random_float(1)
        _ymax = _random_float(1000)
        _zmin = _random_float(1)
        _zmax = _random_float(1000)
        B = adapter.SFFBoundingBox(
            xmin=_xmin,
            xmax=_xmax,
            ymin=_ymin,
            ymax=_ymax,
            zmin=_zmin,
            zmax=_zmax,
        )
        self.assertEqual(B.xmin, _xmin)
        self.assertEqual(B.xmax, _xmax)
        self.assertEqual(B.ymin, _ymin)
        self.assertEqual(B.ymax, _ymax)
        self.assertEqual(B.zmin, _zmin)
        self.assertEqual(B.zmax, _zmax)

    def test_mandatory_fields(self):
        """Test that *max fields are mandatory"""
        bb = adapter.SFFBoundingBox()
        with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
            bb.export(sys.stderr)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _B = emdb_sff.bounding_box_type()
        B = adapter.SFFBoundingBox.from_gds_type(_B)
        self.assertRegex(
            _str(B),
            r"""SFFBoundingBox\(xmin={}, xmax={}, ymin={}, ymax={}, zmin={}, zmax={}\)""".format(
                B.xmin, B.xmax,
                B.ymin, B.ymax,
                B.zmin, B.zmax,
            )
        )
        self.assertEqual(B.xmin, 0)
        self.assertIsNone(B.xmax)
        self.assertEqual(B.ymin, 0)
        self.assertIsNone(B.ymax)
        self.assertEqual(B.zmin, 0)
        self.assertIsNone(B.zmax)
        _xmin = _random_float(1)
        _xmax = _random_float(1000)
        _ymin = _random_float(1)
        _ymax = _random_float(1000)
        _zmin = _random_float(1)
        _zmax = _random_float(1000)
        _B = emdb_sff.bounding_box_type(
            xmin=_xmin,
            xmax=_xmax,
            ymin=_ymin,
            ymax=_ymax,
            zmin=_zmin,
            zmax=_zmax,
        )
        B = adapter.SFFBoundingBox.from_gds_type(_B)
        self.assertEqual(B.xmin, _xmin)
        self.assertEqual(B.xmax, _xmax)
        self.assertEqual(B.ymin, _ymin)
        self.assertEqual(B.ymax, _ymax)
        self.assertEqual(B.zmin, _zmin)
        self.assertEqual(B.zmax, _zmax)

    def test_as_json(self):
        """Test export to JSON"""
        # full
        x0, x1, y0, y1, z0, z1 = _random_integers(count=6)
        bb = adapter.SFFBoundingBox(
            xmin=x0, xmax=x1,
            ymin=y0, ymax=y1,
            zmin=z0, zmax=z1
        )
        bb_json = bb.as_json()
        self.assertEqual(bb.xmin, bb_json[u'xmin'])
        self.assertEqual(bb.xmax, bb_json[u'xmax'])
        self.assertEqual(bb.ymin, bb_json[u'ymin'])
        self.assertEqual(bb.ymax, bb_json[u'ymax'])
        self.assertEqual(bb.zmin, bb_json[u'zmin'])
        self.assertEqual(bb.zmax, bb_json[u'zmax'])
        # empty
        bb = adapter.SFFBoundingBox()
        bb_json = bb.as_json()
        self.assertEqual(bb.xmin, bb_json[u'xmin'])
        self.assertIsNone(bb.xmax)
        self.assertEqual(bb.ymin, bb_json[u'ymin'])
        self.assertIsNone(bb.ymax)
        self.assertEqual(bb.zmin, bb_json[u'zmin'])
        self.assertIsNone(bb.zmax)

    def test_from_json(self):
        """Test import from JSON"""
        # full
        bb_json = {'xmin': 640.0, 'xmax': 348.0, 'ymin': 401.0, 'ymax': 176.0, 'zmin': 491.0, 'zmax': 349.0}
        bb = adapter.SFFBoundingBox.from_json(bb_json)
        self.assertEqual(bb.xmin, bb_json[u'xmin'])
        self.assertEqual(bb.xmax, bb_json[u'xmax'])
        self.assertEqual(bb.ymin, bb_json[u'ymin'])
        self.assertEqual(bb.ymax, bb_json[u'ymax'])
        self.assertEqual(bb.zmin, bb_json[u'zmin'])
        self.assertEqual(bb.zmax, bb_json[u'zmax'])
        # empty
        bb_json = None
        bb = adapter.SFFBoundingBox.from_json(bb_json)
        self.assertEqual(bb.xmin, 0)
        self.assertIsNone(bb.xmax)
        self.assertEqual(bb.ymin, 0)
        self.assertIsNone(bb.ymax)
        self.assertEqual(bb.zmin, 0)
        self.assertIsNone(bb.zmax)

    def test_hff(self):
        """Interconvert to HDF5"""
        # default
        bb = adapter.SFFBoundingBox()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = bb.as_hff(group)
            self.assertIn(u'bounding_box', group)
            self.assertEqual(group[u'bounding_box/xmin'][()], 0)
            self.assertNotIn(u'bounding_box/xmax', group)
            self.assertEqual(group[u'bounding_box/ymin'][()], 0)
            self.assertNotIn(u'bounding_box/ymax', group)
            self.assertEqual(group[u'bounding_box/zmin'][()], 0)
            self.assertNotIn(u'bounding_box/zmax', group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            bb2 = adapter.SFFBoundingBox.from_hff(h[u'container'])
            self.assertEqual(bb, bb2)
        # non-default
        xmin, ymin, zmin = _random_floats(count=3, multiplier=1)
        xmax, ymax, zmax = _random_floats(count=3, multiplier=1000)
        bb = adapter.SFFBoundingBox(
            xmin=xmin,
            xmax=xmax,
            ymin=ymin,
            ymax=ymax,
            zmin=zmin,
            zmax=zmax
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = bb.as_hff(group)
            self.assertIn(u'bounding_box', group)
            self.assertEqual(group[u'bounding_box/xmin'][()], xmin)
            self.assertEqual(group[u'bounding_box/xmax'][()], xmax)
            self.assertEqual(group[u'bounding_box/ymin'][()], ymin)
            self.assertEqual(group[u'bounding_box/ymax'][()], ymax)
            self.assertEqual(group[u'bounding_box/zmin'][()], zmin)
            self.assertEqual(group[u'bounding_box/zmax'][()], zmax)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            bb2 = adapter.SFFBoundingBox.from_hff(h[u'container'])
            self.assertEqual(bb, bb2)


class TestSFFCone(Py23FixTestCase):
    """Test the SFFCone class"""

    def setUp(self):
        adapter.SFFShape.reset_id()

    def tearDown(self):
        adapter.SFFShape.reset_id()

    def test_default(self):
        """Test default settings"""
        C = adapter.SFFCone()
        self.assertRegex(
            _str(C),
            r"""SFFCone\(id={}, height={}, bottom_radius={}, transform_id={}, attribute={}\)""".format(
                0, None, None, None, None
            )
        )
        _height, _bottom_radius, _transform_id = _random_float(10), _random_float(10), _random_integer(start=0)
        C = adapter.SFFCone(
            height=_height, bottom_radius=_bottom_radius, transform_id=_transform_id
        )
        self.assertRegex(
            _str(C),
            r"""SFFCone\(id={}, height={}, bottom_radius={}, transform_id={}, attribute={}\)""".format(
                1, _height, _bottom_radius, _transform_id, None
            )
        )
        self.assertEqual(C.id, 1)  # the second one we have created
        self.assertEqual(C.height, _height)
        self.assertEqual(C.bottom_radius, _bottom_radius)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _C = emdb_sff.cone()
        C = adapter.SFFCone.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCone\(id={}, height={}, bottom_radius={}, transform_id={}, attribute={}\)""".format(
                None, None, None, None, None
            )
        )
        _height, _bottom_radius, _transform_id = _random_float(10), _random_float(10), _random_integer(start=0)
        _C = emdb_sff.cone(
            height=_height, bottom_radius=_bottom_radius, transform_id=_transform_id
        )
        C = adapter.SFFCone.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCone\(id={}, height={}, bottom_radius={}, transform_id={}, attribute={}\)""".format(
                None, _height, _bottom_radius, _transform_id, None
            )
        )
        self.assertIsNone(C.id)
        self.assertEqual(C.height, _height)
        self.assertEqual(C.bottom_radius, _bottom_radius)

    def test_json(self):
        """Interconvert to JSON"""
        height, bottom_radius = _random_floats(count=2, multiplier=10)
        c = adapter.SFFCone(height=height, bottom_radius=bottom_radius)
        c_json = c.as_json()
        self.assertEqual(c_json, {
            u'id': c.id,
            u'shape': u'cone',
            u'height': c.height,
            u'bottom_radius': c.bottom_radius,
            u'transform_id': None
        })
        c2 = adapter.SFFCone.from_json(c_json)
        self.assertEqual(c, c2)

    def test_hff(self):
        # empty case
        cone = adapter.SFFCone()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = cone.as_hff(group)
            group_name = u'{}'.format(cone.id)
            self.assertIn(group_name, group)
            self.assertIn(u'id', group[group_name])
            self.assertIn(u'shape', group[group_name])
            self.assertEqual(group[group_name + '/shape'][()], u'cone')
            self.assertNotIn(u'height', group[group_name])
            self.assertNotIn(u'bottom_radius', group[group_name])
            self.assertNotIn(u'transform_id', group[group_name])
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                cone2 = adapter.SFFCone.from_hff(group)
                self.assertEqual(cone, cone2)
        # non-empty case
        height, bottom_radius = _random_floats(count=2, multiplier=10)
        transform_id = _random_integer(start=0)
        cone = adapter.SFFCone(
            height=height,
            bottom_radius=bottom_radius,
            transform_id=transform_id
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = cone.as_hff(group)
            group_name = u'{}'.format(cone.id)
            self.assertIn(group_name, group)
            self.assertIn(u'id', group[group_name])
            self.assertIn(u'shape', group[group_name])
            self.assertEqual(group[u'{}/height'.format(cone.id)][()], height)
            self.assertEqual(group[u'{}/bottom_radius'.format(cone.id)][()], bottom_radius)
            self.assertEqual(group[u'{}/transform_id'.format(cone.id)][()], transform_id)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                cone2 = adapter.SFFCone.from_hff(group)
                self.assertEqual(cone, cone2)


class TestSFFCuboid(Py23FixTestCase):
    """Test the SFFCuboid class"""

    def tearDown(self):
        adapter.SFFShape.reset_id()

    def test_default(self):
        """Test default settings"""
        C = adapter.SFFCuboid()
        self.assertRegex(
            _str(C),
            r"""SFFCuboid\(id={}, x={}, y={}, z={}, transform_id={}, attribute={}\)""".format(
                0, None, None, None, None, None
            )
        )
        _x, _y, _z, _transform_id = _random_float(10), _random_float(10), _random_float(10), _random_integer()
        C = adapter.SFFCuboid(x=_x, y=_y, z=_z, transform_id=_transform_id)
        self.assertRegex(
            _str(C),
            r"""SFFCuboid\(id={}, x={}, y={}, z={}, transform_id={}, attribute={}\)""".format(
                1, _x, _y, _z, _transform_id, None
            )
        )
        self.assertEqual(C.id, 1)  # the second one we have created
        self.assertEqual(C.x, _x)
        self.assertEqual(C.y, _y)
        self.assertEqual(C.z, _z)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _C = emdb_sff.cuboid()
        C = adapter.SFFCuboid.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCuboid\(id={}, x={}, y={}, z={}, transform_id={}\, attribute={}\)""".format(
                None, None, None, None, None, None
            )
        )
        _x, _y, _z, _transform_id = _random_float(10), _random_float(10), _random_float(10), _random_integer()
        _C = emdb_sff.cuboid(x=_x, y=_y, z=_z, transform_id=_transform_id)
        C = adapter.SFFCuboid.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCuboid\(id={}, x={}, y={}, z={}, transform_id={}, attribute={}\)""".format(
                None, _x, _y, _z, _transform_id, None
            )
        )
        self.assertEqual(C.x, _x)
        self.assertEqual(C.y, _y)
        self.assertEqual(C.z, _z)

    def test_json(self):
        """Interconvert to JSON"""
        x, y, z = _random_floats(count=3, multiplier=10)
        c = adapter.SFFCuboid(x=x, y=y, z=z)
        c_json = c.as_json()
        self.assertEqual(c_json, {
            u'id': c.id,
            u'shape': u'cuboid',
            u'x': c.x,
            u'y': c.y,
            u'z': c.z,
            u'transform_id': None
        })
        c2 = adapter.SFFCuboid.from_json(c_json)
        self.assertEqual(c, c2)

    def test_hff(self):
        # empty case
        cuboid = adapter.SFFCuboid()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = cuboid.as_hff(group)
            group_name = u'{}'.format(cuboid.id)
            self.assertIn(group_name, group)
            self.assertIn(u'id', group[group_name])
            self.assertIn(u'shape', group[group_name])
            self.assertEqual(group[group_name + u'/shape'][()], u'cuboid')
            self.assertNotIn(u'x', group[group_name])
            self.assertNotIn(u'y', group[group_name])
            self.assertNotIn(u'z', group[group_name])
            self.assertNotIn(u'transform_id', group[group_name])
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                cuboid2 = adapter.SFFCuboid.from_hff(group)
                self.assertEqual(cuboid, cuboid2)
        # non-empty case
        x, y, z = _random_floats(count=3, multiplier=10)
        transform_id = _random_integer(start=0)
        cuboid = adapter.SFFCuboid(
            x=x,
            y=y,
            z=z,
            transform_id=transform_id
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = cuboid.as_hff(group)
            group_name = u'{}'.format(cuboid.id)
            self.assertIn(group_name, group)
            self.assertIn(u'id', group[group_name])
            self.assertIn(u'shape', group[group_name])
            self.assertEqual(group[group_name + u'/shape'][()], u'cuboid')
            self.assertEqual(group[u'{}/x'.format(cuboid.id)][()], x)
            self.assertEqual(group[u'{}/y'.format(cuboid.id)][()], y)
            self.assertEqual(group[u'{}/z'.format(cuboid.id)][()], z)
            self.assertEqual(group[u'{}/transform_id'.format(cuboid.id)][()], transform_id)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                cuboid2 = adapter.SFFCuboid.from_hff(group)
                self.assertEqual(cuboid, cuboid2)


class TestSFFCylinder(Py23FixTestCase):
    """Test the SFFCylinder class"""

    def tearDown(self):
        adapter.SFFShape.reset_id()

    def test_default(self):
        """Test default settings"""
        C = adapter.SFFCylinder()
        self.assertRegex(
            _str(C),
            r"""SFFCylinder\(id={}, height={}, diameter={}, transform_id={}, attribute={}\)""".format(
                0, None, None, None, None
            )
        )
        _height, _diameter, _transform_id = _random_float(10), _random_float(10), _random_integer()
        C = adapter.SFFCylinder(
            height=_height, diameter=_diameter, transform_id=_transform_id
        )
        self.assertRegex(
            _str(C),
            r"""SFFCylinder\(id={}, height={}, diameter={}, transform_id={}, attribute={}\)""".format(
                1, _height, _diameter, _transform_id, None
            )
        )
        self.assertEqual(C.id, 1)  # the second one we have created
        self.assertEqual(C.height, _height)
        self.assertEqual(C.diameter, _diameter)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _C = emdb_sff.cylinder()
        C = adapter.SFFCylinder.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCylinder\(id={}, height={}, diameter={}, transform_id={}, attribute={}\)""".format(
                None, None, None, None, None
            )
        )
        _height, _diameter, _transform_id = _random_float(10), _random_float(10), _random_integer(start=0)
        _C = emdb_sff.cylinder(
            height=_height, diameter=_diameter, transform_id=_transform_id
        )
        C = adapter.SFFCylinder.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCylinder\(id={}, height={}, diameter={}, transform_id={}, attribute={}\)""".format(
                None, _height, _diameter, _transform_id, None
            )
        )
        self.assertIsNone(C.id)
        self.assertEqual(C.height, _height)
        self.assertEqual(C.diameter, _diameter)

    def test_json(self):
        """Interconvert to JSON"""
        height, diameter = _random_floats(count=2, multiplier=10)
        c = adapter.SFFCylinder(height=height, diameter=diameter)
        c_json = c.as_json()
        self.assertEqual(c_json, {
            u'id': c.id,
            u'shape': u'cylinder',
            u'height': c.height,
            u'diameter': c.diameter,
            u'transform_id': None
        })
        c2 = adapter.SFFCylinder.from_json(c_json)
        self.assertEqual(c, c2)

    def test_hff(self):
        # empty case
        cylinder = adapter.SFFCylinder()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = cylinder.as_hff(group)
            group_name = u'{}'.format(cylinder.id)
            self.assertIn(group_name, group)
            self.assertIn(u'id', group[group_name])
            self.assertIn(u'shape', group[group_name])
            self.assertEqual(group[group_name + u'/shape'][()], u'cylinder')
            self.assertNotIn(u'height', group[group_name])
            self.assertNotIn(u'diameter', group[group_name])
            self.assertNotIn(u'transform_id', group[group_name])
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                cylinder2 = adapter.SFFCylinder.from_hff(group)
                self.assertEqual(cylinder, cylinder2)
        # non-empty case
        height, diameter = _random_floats(count=2, multiplier=10)
        transform_id = _random_integer(start=0)
        cylinder = adapter.SFFCylinder(
            height=height,
            diameter=diameter,
            transform_id=transform_id
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = cylinder.as_hff(group)
            group_name = u'{}'.format(cylinder.id)
            self.assertIn(group_name, group)
            self.assertIn(u'id', group[group_name])
            self.assertIn(u'shape', group[group_name])
            self.assertEqual(group[group_name + u'/shape'][()], u'cylinder')
            self.assertEqual(group[u'{}/height'.format(cylinder.id)][()], height)
            self.assertEqual(group[u'{}/diameter'.format(cylinder.id)][()], diameter)
            self.assertEqual(group[u'{}/transform_id'.format(cylinder.id)][()], transform_id)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                cylinder2 = adapter.SFFCylinder.from_hff(group)
                self.assertEqual(cylinder, cylinder2)


class TestSFFEllipsoid(Py23FixTestCase):
    """Test the SFFEllipsoid class"""

    def tearDown(self):
        adapter.SFFShape.reset_id()

    def test_default(self):
        """Test default settings"""
        E = adapter.SFFEllipsoid()
        self.assertRegex(
            _str(E),
            r"""SFFEllipsoid\(id={}, x={}, y={}, z={}, transform_id={}, attribute={}\)""".format(
                0, None, None, None, None, None
            )
        )
        _x, _y, _z, _transform_id = _random_float(10), _random_float(10), _random_float(10), _random_integer()
        E = adapter.SFFEllipsoid(x=_x, y=_y, z=_z, transform_id=_transform_id)
        self.assertRegex(
            _str(E),
            r"""SFFEllipsoid\(id={}, x={}, y={}, z={}, transform_id={}, attribute={}\)""".format(
                1, _x, _y, _z, _transform_id, None
            )
        )
        self.assertEqual(E.id, 1)  # the second one we have created
        self.assertEqual(E.x, _x)
        self.assertEqual(E.y, _y)
        self.assertEqual(E.z, _z)

    def test_from_gds_type(self):
        """Test that all attributes exists when we start with a gds_type"""
        _C = emdb_sff.ellipsoid()
        C = adapter.SFFEllipsoid.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFEllipsoid\(id={}, x={}, y={}, z={}, transform_id={}, attribute={}\)""".format(
                None, None, None, None, None, None
            )
        )
        _x, _y, _z, _transform_id = _random_float(10), _random_float(10), _random_float(10), _random_integer()
        _C = emdb_sff.ellipsoid(x=_x, y=_y, z=_z, transform_id=_transform_id)
        C = adapter.SFFEllipsoid.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFEllipsoid\(id={}, x={}, y={}, z={}, transform_id={}, attribute={}\)""".format(
                None, _x, _y, _z, _transform_id, None
            )
        )
        self.assertEqual(C.x, _x)
        self.assertEqual(C.y, _y)
        self.assertEqual(C.z, _z)

    def test_json(self):
        """Interconvert to JSON"""
        x, y, z = _random_floats(count=3, multiplier=10)
        e = adapter.SFFEllipsoid(x=x, y=y, z=z)
        e_json = e.as_json()
        self.assertEqual(e_json, {
            u'id': e.id,
            u'shape': u'ellipsoid',
            u'x': e.x,
            u'y': e.y,
            u'z': e.z,
            u'transform_id': None
        })
        e2 = adapter.SFFEllipsoid.from_json(e_json)
        self.assertEqual(e, e2)

    def test_hff(self):
        # empty case
        ellipsoid = adapter.SFFEllipsoid()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = ellipsoid.as_hff(group)
            group_name = u'{}'.format(ellipsoid.id)
            self.assertIn(group_name, group)
            self.assertIn(u'id', group[group_name])
            self.assertIn(u'shape', group[group_name])
            self.assertEqual(group[group_name + u'/shape'][()], u'ellipsoid')
            self.assertNotIn(u'x', group[group_name])
            self.assertNotIn(u'y', group[group_name])
            self.assertNotIn(u'z', group[group_name])
            self.assertNotIn(u'transform_id', group[group_name])
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                ellipsoid2 = adapter.SFFEllipsoid.from_hff(group)
                self.assertEqual(ellipsoid, ellipsoid2)
        # non-empty case
        x, y, z = _random_floats(count=3, multiplier=10)
        transform_id = _random_integer(start=0)
        ellipsoid = adapter.SFFEllipsoid(
            x=x,
            y=y,
            z=z,
            transform_id=transform_id
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = ellipsoid.as_hff(group)
            group_name = u'{}'.format(ellipsoid.id)
            self.assertIn(group_name, group)
            self.assertIn(u'id', group[group_name])
            self.assertIn(u'shape', group[group_name])
            self.assertEqual(group[group_name + u'/shape'][()], u'ellipsoid')
            self.assertEqual(group[u'{}/x'.format(ellipsoid.id)][()], x)
            self.assertEqual(group[u'{}/y'.format(ellipsoid.id)][()], y)
            self.assertEqual(group[u'{}/z'.format(ellipsoid.id)][()], z)
            self.assertEqual(group[u'{}/transform_id'.format(ellipsoid.id)][()], transform_id)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                ellipsoid2 = adapter.SFFEllipsoid.from_hff(group)
                self.assertEqual(ellipsoid, ellipsoid2)


class TestSFFShapePrimitiveList(Py23FixTestCase):
    """Test the SFFShapePrimitiveList class"""

    def tearDown(self):
        adapter.SFFShape.reset_id()

    @staticmethod
    def get_sff_shapes(counts=_random_integers(count=4, start=2, stop=10)):
        no_cones, no_cuboids, no_cylinders, no_ellipsoids = counts
        cones = [adapter.SFFCone(
            height=_random_float(10),
            bottom_radius=_random_float(10),
        ) for _ in _xrange(no_cones)]
        cuboids = [
            adapter.SFFCuboid(
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            ) for _ in _xrange(no_cuboids)]
        cylinders = [
            adapter.SFFCylinder(
                height=_random_float(10),
                diameter=_random_float(10),
            ) for _ in _xrange(no_cylinders)]
        ellipsoids = [
            adapter.SFFEllipsoid(
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            )
        ]
        return cones, cuboids, cylinders, ellipsoids

    @staticmethod
    def get_gds_shapes(counts=_random_integers(count=4, start=2, stop=10)):
        no_cones, no_cuboids, no_cylinders, no_ellipsoids = counts
        cones = [emdb_sff.cone(
            height=_random_float(10),
            bottom_radius=_random_float(10),
        ) for _ in _xrange(no_cones)]
        cuboids = [
            emdb_sff.cuboid(
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            ) for _ in _xrange(no_cuboids)]
        cylinders = [
            emdb_sff.cylinder(
                height=_random_float(10),
                diameter=_random_float(10),
            ) for _ in _xrange(no_cylinders)]
        ellipsoids = [
            emdb_sff.ellipsoid(
                x=_random_float(10),
                y=_random_float(10),
                z=_random_float(10),
            )
        ]
        return cones, cuboids, cylinders, ellipsoids

    def test_default(self):
        """Test default settings"""
        S = adapter.SFFShapePrimitiveList()
        cones, cuboids, cylinders, ellipsoids = TestSFFShapePrimitiveList.get_sff_shapes()
        [S.append(c) for c in cones]
        [S.append(c) for c in cuboids]
        [S.append(c) for c in cylinders]
        [S.append(c) for c in ellipsoids]
        self.assertRegex(
            _str(S),
            r"""SFFShapePrimitiveList\(\[.*\]\)"""
        )
        total_shapes = len(cones) + len(cuboids) + len(cylinders) + len(ellipsoids)
        self.assertEqual(len(S), total_shapes)
        self.assertEqual(list(S.get_ids()), list(_xrange(total_shapes)))
        s_id = random.choice(list(_xrange(total_shapes)))
        s = S.get_by_id(s_id)
        self.assertIsInstance(s, (adapter.SFFCone, adapter.SFFCuboid, adapter.SFFCylinder, adapter.SFFEllipsoid))

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _S = emdb_sff.shape_primitive_listType()
        cones, cuboids, cylinders, ellipsoids = TestSFFShapePrimitiveList.get_gds_shapes()
        [_S.add_shape_primitive(c) for c in cones]
        [_S.add_shape_primitive(c) for c in cuboids]
        [_S.add_shape_primitive(c) for c in cylinders]
        [_S.add_shape_primitive(c) for c in ellipsoids]
        S = adapter.SFFShapePrimitiveList.from_gds_type(_S)
        self.assertRegex(
            _str(S),
            r"""SFFShapePrimitiveList\(\[.*\]\)"""
        )
        total_shapes = len(cones) + len(cuboids) + len(cylinders) + len(ellipsoids)
        self.assertEqual(len(S), total_shapes)
        self.assertEqual(list(S.get_ids()), list())
        s_id = random.choice(list(_xrange(total_shapes)))
        s = S[s_id]
        self.assertIsInstance(s, (adapter.SFFCone, adapter.SFFCuboid, adapter.SFFCylinder, adapter.SFFEllipsoid))

    def test_json(self):
        """Interconvert to JSON"""
        S = adapter.SFFShapePrimitiveList()

        def _meld(*args):
            melded = list()
            for arg in args:
                melded += arg
            return melded

        shapes = _meld(*self.get_sff_shapes())
        for shape in shapes:
            S.append(shape)
        S_json = S.as_json()
        S2 = adapter.SFFShapePrimitiveList.from_json(S_json)
        self.assertEqual(S, S2)

    def test_hff(self):
        """Interconvert to HDF5"""
        # empty
        S = adapter.SFFShapePrimitiveList()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = S.as_hff(group)
            self.assertIn(u'shape_primitive_list', group)
            self.assertEqual(len(group[u'shape_primitive_list']), 0)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            S2 = adapter.SFFShapePrimitiveList.from_hff(h[u'container'])
            self.assertEqual(S, S2)
        # non-empty
        S = adapter.SFFShapePrimitiveList()
        no_cones = _random_integer(start=2, stop=10)
        height, bottom_radius = _random_floats(count=2, multiplier=10)
        transform_id = _random_integer()
        [S.append(
            adapter.SFFCone(
                height=height,
                bottom_radius=bottom_radius,
                transform_id=transform_id,
            )
        ) for _ in _xrange(no_cones)]
        no_cylinders = _random_integer(start=2, stop=10)
        transform_id = _random_integer()
        [S.append(
            adapter.SFFCylinder(
                height=height,
                diameter=bottom_radius,
                transform_id=transform_id,
            )
        ) for _ in _xrange(no_cylinders)]
        x, y, z = _random_floats(count=3, multiplier=100)
        no_cuboids = _random_integer(start=2, stop=10)
        transform_id = _random_integer()
        [S.append(
            adapter.SFFCuboid(
                x=x,
                y=y,
                z=z,
                transform_id=transform_id,
            )
        ) for _ in _xrange(no_cuboids)]
        no_ellipsoids = _random_integer(start=2, stop=10)
        transform_id = _random_integer()
        [S.append(
            adapter.SFFEllipsoid(
                x=x,
                y=y,
                z=z,
                transform_id=transform_id,
            )
        ) for _ in _xrange(no_ellipsoids)]
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = S.as_hff(group)
            self.assertIn(u'shape_primitive_list', group)
            self.assertEqual(len(group[u'shape_primitive_list']), len(S))
            for i, s in enumerate(S):
                self.assertEqual(s.id, group[u'shape_primitive_list/{}/id'.format(i)][()])
                if isinstance(s, adapter.SFFCone):
                    self.assertEqual(s.height, group[u'shape_primitive_list/{}/height'.format(i)][()])
                    self.assertEqual(s.bottom_radius, group[u'shape_primitive_list/{}/bottom_radius'.format(i)][()])
                elif isinstance(s, adapter.SFFCylinder):
                    self.assertEqual(s.height, group[u'shape_primitive_list/{}/height'.format(i)][()])
                    self.assertEqual(s.diameter, group[u'shape_primitive_list/{}/diameter'.format(i)][()])
                elif isinstance(s, (adapter.SFFCuboid, adapter.SFFEllipsoid)):
                    self.assertEqual(s.x, group[u'shape_primitive_list/{}/x'.format(i)][()])
                    self.assertEqual(s.y, group[u'shape_primitive_list/{}/y'.format(i)][()])
                    self.assertEqual(s.z, group[u'shape_primitive_list/{}/z'.format(i)][()])
                self.assertEqual(s.transform_id, group[u'shape_primitive_list/{}/transform_id'.format(i)][()])
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            S2 = adapter.SFFShapePrimitiveList.from_hff(h[u'container'])
            self.assertEqual(S, S2)


class TestSFFSegment(Py23FixTestCase):
    """Test the SFFSegment class"""

    def tearDown(self):
        adapter.SFFSegment.reset_id()

    def test_default(self):
        """Test default settings"""
        s = adapter.SFFSegment()
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=1, parent_id=0, biological_annotation=None, colour=None, """ \
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)"""
        )
        # change ID
        _id = _random_integer()
        s = adapter.SFFSegment(id=_id)
        self.assertEqual(s.id, _id)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parent_id=0, biological_annotation=None, colour=None, """ \
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
                _id)
        )
        # change parent_id
        _parent_id = _random_integer()
        s = adapter.SFFSegment(parent_id=_parent_id)
        self.assertEqual(s.id, _id + 1)  # we have an increment from the previous set value
        self.assertEqual(s.parent_id, _parent_id)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parent_id={}, biological_annotation=None, colour=None, """ \
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
                _id + 1,
                _parent_id
            )
        )
        # change biological_annotation
        B = adapter.SFFBiologicalAnnotation(
            name=" ".join(rw.random_words(count=3)),
            description=li.get_sentence(),
        )
        s = adapter.SFFSegment(biological_annotation=B)
        self.assertEqual(s.id, _id + 2)  # we have an increment from the previous set value
        self.assertEqual(s.biological_annotation, B)
        _segment_regex = r"""SFFSegment\(id={}, parent_id={}, biological_annotation={}, colour=None, """ \
                         r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
            _id + 2, 0, _str(B).replace(r"(", r"\(").replace(r")", r"\)").replace(r"[", r"\[").replace(r"]", r"\]"))
        self.assertRegex(
            _str(s),
            _segment_regex
        )
        # change colour
        R = adapter.SFFRGBA(random_colour=True)
        s = adapter.SFFSegment(colour=R)
        self.assertEqual(s.id, _id + 3)  # we have an increment from the previous set value
        self.assertEqual(s.colour, R)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parent_id={}, biological_annotation=None, colour={}, """ \
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
                _id + 3,
                0,
                _str(R).replace(r"(", r"\(").replace(r")", r"\)")
            )
        )
        # 3D volume\
        _l = _random_integer(start=0)
        _v = _random_integer()
        _t = _random_integer(start=0)
        V = adapter.SFFThreeDVolume(
            latticeId=_l,
            value=_v,
            transformId=_t
        )
        s = adapter.SFFSegment(three_d_volume=V)
        self.assertEqual(s.id, _id + 4)
        self.assertEqual(s.three_d_volume, V)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parent_id={}, biological_annotation=None, colour=None, """ \
            r"""three_d_volume={}, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
                _id + 4,
                0,
                _str(V).replace(r"(", r"\(").replace(r")", r"\)")
            )
        )
        # meshes
        M = adapter.SFFMeshList()
        s = adapter.SFFSegment(mesh_list=M)
        self.assertEqual(s.id, _id + 5)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parent_id={}, biological_annotation=None, colour=None, """ \
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
                _id + 5,
                0,
            )
        )
        # shapes
        S = adapter.SFFShapePrimitiveList()
        s = adapter.SFFSegment(shape_primitive_list=S)
        self.assertEqual(s.id, _id + 6)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parent_id={}, biological_annotation=None, colour=None, """ \
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
                _id + 6,
                0,
            )
        )

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _s = emdb_sff.segment_type()
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=None, parent_id=\d+, biological_annotation=None, colour=None, """ \
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), """ \
            r"""shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)"""
        )
        # change ID
        _id = _random_integer()
        _s = emdb_sff.segment_type(id=_id)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertEqual(s.id, _id)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parent_id=\d+, biological_annotation=None, colour=None, """ \
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
                _id)
        )
        # change parent_id
        _parent_id = _random_integer()
        _s = emdb_sff.segment_type(parent_id=_parent_id)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        self.assertEqual(s.parent_id, _parent_id)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id={}, parent_id={}, biological_annotation=None, colour=None, """ \
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
                None,
                _parent_id
            )
        )
        # change biological_annotation
        _B = emdb_sff.biological_annotationType(
            name=" ".join(rw.random_words(count=3)),
            description=li.get_sentence(),
        )
        _s = emdb_sff.segment_type(biological_annotation=_B)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        B = adapter.SFFBiologicalAnnotation.from_gds_type(_B)
        self.assertEqual(s.biological_annotation, B)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=None, parent_id=\d+, biological_annotation={}, colour=None, """
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
                _str(B).replace(r"(", r"\(").replace(r")", r"\)").replace(r"[", r"\[").replace(r"]", r"\]")
            )
        )
        # change colour
        _R = emdb_sff.rgba_type(red=_random_float(), green=_random_float(), blue=_random_float())
        R = adapter.SFFRGBA.from_gds_type(_R)
        _s = emdb_sff.segment_type(colour=_R)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        self.assertEqual(s.colour, R)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=None, parent_id=\d+, biological_annotation=None, colour={}, """ \
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
                _str(R).replace(r"(", r"\(").replace(r")", r"\)")
            )
        )
        # 3D volume
        _l = _random_integer(start=0)
        _v = _random_integer()
        _t = _random_integer(start=0)
        _V = emdb_sff.three_d_volume_type(
            latticeId=_l,
            value=_v,
            transformId=_t
        )
        V = adapter.SFFThreeDVolume.from_gds_type(_V)
        _s = emdb_sff.segment_type(three_d_volume=_V)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        self.assertEqual(s.three_d_volume, V)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=None, parent_id=\d+, biological_annotation=None, colour=None, """ \
            r"""three_d_volume={}, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
                _str(V).replace(r"(", r"\(").replace(r")", r"\)")
            )
        )
        # meshes
        _M = emdb_sff.mesh_listType()
        M = adapter.SFFMeshList.from_gds_type(_M)
        _s = emdb_sff.segment_type(mesh_list=_M)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=None, parent_id=\d+, biological_annotation=None, colour=None, """ \
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)"""
        )
        # shapes
        _S = emdb_sff.shape_primitive_listType()
        S = adapter.SFFShapePrimitiveList.from_gds_type(_S)
        _s = emdb_sff.segment_type(shape_primitive_list=_S)
        s = adapter.SFFSegment.from_gds_type(_s)
        self.assertIsNone(s.id)
        self.assertRegex(
            _str(s),
            r"""SFFSegment\(id=None, parent_id=\d+, biological_annotation=None, colour=None, """ \
            r"""three_d_volume=None, mesh_list=SFFMeshList\(\[.*\]\), shape_primitive_list=SFFShapePrimitiveList\(\[.*\]\)\)""".format(
            )
        )

    def test_as_json(self):
        """Test that we can export as JSON"""
        # at least colour needed
        s = adapter.SFFSegment()
        s.colour = adapter.SFFRGBA(random_colour=True)
        s_json = s.as_json()
        self.assertEqual(s_json[u'id'], s.id)
        self.assertEqual(s_json[u'parent_id'], s.parent_id)
        self.assertEqual(s_json[u'colour'], s.colour.value)
        # _print(s_json)
        # self.assertTrue(False)
        # with annotation
        s = adapter.SFFSegment(
            biological_annotation=adapter.SFFBiologicalAnnotation(
                name=rw.random_word(),
                description=li.get_sentence(),
            )
        )
        s.colour = adapter.SFFRGBA(random_colour=True)
        s_json = s.as_json()
        self.assertEqual(s_json[u'id'], s.id)
        self.assertEqual(s_json[u'parent_id'], s.parent_id)
        self.assertEqual(s_json[u'colour'], s.colour.value)
        self.assertEqual(s_json[u'biological_annotation'][u'name'], s.biological_annotation.name)
        self.assertEqual(s_json[u'biological_annotation'][u'description'], s.biological_annotation.description)

    def test_from_json(self):
        """Test that we can import from JSON"""
        # minimal
        s_json = {'id': 2, 'parent_id': 0, 'colour': (0.3480471169539232, 0.9354618836165659, 0.7017431484633613, 1.0)}
        s = adapter.SFFSegment.from_json(s_json)
        self.assertEqual(s.id, s_json[u'id'])
        self.assertEqual(s.parent_id, s_json[u'parent_id'])
        self.assertEqual(s.colour.value, s_json[u'colour'])
        # more
        s_json = {
            'id': 3,
            'parent_id': 0,
            'biological_annotation': {
                'name': 'preserver',
                'description': 'Dictumstvivamus proin purusvestibulum turpis sociis assum.',
                'number_of_instances': 1},
            'colour': (0.3284280279067431, 0.8229825614708411, 0.07590219333941295, 1.0)
        }
        s = adapter.SFFSegment.from_json(s_json)
        self.assertEqual(s_json[u'id'], s.id)
        self.assertEqual(s_json[u'parent_id'], s.parent_id)
        self.assertEqual(s_json[u'colour'], s.colour.value)
        self.assertEqual(s_json[u'biological_annotation'][u'name'], s.biological_annotation.name)
        self.assertEqual(s_json[u'biological_annotation'][u'description'], s.biological_annotation.description)
        self.assertEqual(s_json[u'biological_annotation'][u'number_of_instances'],
                         s.biological_annotation.number_of_instances)

    def test_hff(self):
        """Interconvert to HDF5"""
        # empty
        s = adapter.SFFSegment()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = s.as_hff(group)
            group_name = u'{}'.format(s.id)
            self.assertIn(group_name, group)
            self.assertIn(group_name + '/id', group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                s2 = adapter.SFFSegment.from_hff(group)
                self.assertEqual(s, s2)
        # non-empty
        external_references = adapter.SFFExternalReferenceList()
        [external_references.append(
            adapter.SFFExternalReference(
                resource=rw.random_word(),
                url='https://{}.com/{}/{}'.format(*rw.random_words(count=3)),
                accession=rw.random_word(),
                label=' '.join(rw.random_words(count=2)),
                description=li.get_sentence(),
            )
        ) for _ in _xrange(_random_integer(start=2, stop=5))]
        biological_annotation = adapter.SFFBiologicalAnnotation(
            name=' '.join(rw.random_words(count=3)),
            description=li.get_sentence(),
            external_references=external_references,
        )
        mesh_list = adapter.SFFMeshList()
        [mesh_list.append(
            adapter.SFFMesh(
                vertices=adapter.SFFVertices.from_array(numpy.random.rand(4, 3)),
                triangles=adapter.SFFTriangles.from_array(numpy.random.randint(0, 4, size=(4, 3)))
            )
        ) for _ in _xrange(_random_integer(start=3, stop=5))]
        shape_primitive_list = adapter.SFFShapePrimitiveList()
        [shape_primitive_list.append(
            random.choice([
                adapter.SFFCone(height=_random_float(multiplier=10), bottom_radius=_random_float(multiplier=10)),
                adapter.SFFCylinder(height=_random_float(multiplier=10), diameter=_random_float(multiplier=10)),
                adapter.SFFCuboid(x=_random_float(multiplier=10), y=_random_float(multiplier=10),
                                  z=_random_float(multiplier=10)),
                adapter.SFFEllipsoid(x=_random_float(multiplier=10), y=_random_float(multiplier=10),
                                     z=_random_float(multiplier=10))
            ])
        ) for _ in _xrange(_random_integer(start=3, stop=6))]
        s = adapter.SFFSegment(
            colour=adapter.SFFRGBA(random_colour=True),
            biological_annotation=biological_annotation,
            mesh_list=mesh_list,
            three_d_volume=adapter.SFFThreeDVolume(
                lattice_id=_random_integer(),
                value=_random_integer(),
            ),
            shape_primitive_list=shape_primitive_list,
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = s.as_hff(group)
            group_name = u'{}'.format(s.id)
            self.assertIn(group_name, group)
            self.assertIn(group_name + '/id', group)
            self.assertIn(group_name + '/parent_id', group)
            self.assertIn(group_name + '/biological_annotation', group)
            self.assertIn(group_name + '/colour', group)
            self.assertIn(group_name + '/mesh_list', group)
            self.assertIn(group_name + '/three_d_volume', group)
            self.assertIn(group_name + '/shape_primitive_list', group)
            self.assertEqual(group[group_name + '/id'][()], s.id)
            self.assertEqual(group[group_name + '/parent_id'][()], s.parent_id)
            self.assertCountEqual(group[group_name + '/colour'][()], s.colour.value)
            self.assertEqual(adapter.SFFBiologicalAnnotation.from_hff(group[group_name]), s.biological_annotation)
            self.assertEqual(adapter.SFFMeshList.from_hff(group[group_name]), s.mesh_list)
            self.assertEqual(adapter.SFFThreeDVolume.from_hff(group[group_name]), s.three_d_volume)
            self.assertEqual(adapter.SFFShapePrimitiveList.from_hff(group[group_name]), s.shape_primitive_list)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                s2 = adapter.SFFSegment.from_hff(group)
                self.assertEqual(s, s2)


class TestSFFSegmentList(Py23FixTestCase):
    """Test the SFFSegmentList class"""

    def test_default(self):
        """Test default settings"""
        S = adapter.SFFSegmentList()
        _no_items = _random_integer(start=2, stop=10)
        [S.append(adapter.SFFSegment()) for _ in _xrange(_no_items)]
        self.assertRegex(
            _str(S),
            r"""SFFSegmentList\(\[SFFSegment\(.*\)\]\)"""
        )
        self.assertEqual(len(S), _no_items)
        self.assertEqual(list(S.get_ids()), list(_xrange(1, _no_items + 1)))
        # adding a segment without ID does not change the number of IDs (because it has ID=None)
        S.append(adapter.SFFSegment.from_gds_type(
            emdb_sff.segment_type()
        ))
        self.assertEqual(list(S.get_ids()), list(_xrange(1, _no_items + 1)))
        # exception when trying to overwrite an ID in `_id_dict`
        with self.assertRaisesRegex(KeyError, r".*already present.*"):
            S.append(adapter.SFFSegment.from_gds_type((
                emdb_sff.segment_type(id=1)
            )))

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _S = emdb_sff.segment_listType()
        _no_items = _random_integer(start=2, stop=10)
        _S.set_segment([
            emdb_sff.segment_type(
                id=i,
            ) for i in _xrange(1, _no_items + 1)]
        )
        S = adapter.SFFSegmentList.from_gds_type(_S)
        self.assertRegex(
            _str(S),
            r"""SFFSegmentList\(\[SFFSegment\(.*\)\]\)"""
        )
        self.assertEqual(len(S), _no_items)
        self.assertEqual(list(S.get_ids()), list(_xrange(1, _no_items + 1)))

    def test_json(self):
        """Interconversion to JSON"""
        S = adapter.SFFSegmentList()
        no_s = _random_integer(start=2, stop=5)
        for _ in _xrange(no_s):
            no_er = _random_integer(start=2, stop=10)
            external_references = adapter.SFFExternalReferenceList()
            [external_references.append(
                adapter.SFFExternalReference(
                    resource=rw.random_word(),
                    url=rw.random_word(),
                    accession=rw.random_word(),
                    label=rw.random_word(),
                    description=li.get_sentence(),
                )
            ) for _ in _xrange(no_er)]
            S.append(
                adapter.SFFSegment(
                    biological_annotation=adapter.SFFBiologicalAnnotation(
                        name=rw.random_word(),
                        description=li.get_sentence(),
                        external_references=external_references,
                    ),
                    colour=adapter.SFFRGBA(random_colour=True),
                    three_d_volume=adapter.SFFThreeDVolume(
                        lattice_id=_random_integer(stop=5),
                        value=_random_integer()
                    ),
                    # mesh_list=,
                    # shape_primitive_list=shape_primitive_list,
                )
            )
        S_json = S.as_json()
        self.assertEqual(S_json, [{
            u'id': s.id,
            u'parent_id': s.parent_id,
            u'biological_annotation': s.biological_annotation.as_json() if s.biological_annotation is not None else None,
            u'colour': s.colour.as_json(),
            u'three_d_volume': s.three_d_volume.as_json(),
            u'mesh_list': s.mesh_list.as_json(),
            u'shape_primitive_list': s.shape_primitive_list.as_json()
        } for s in S])
        S2 = adapter.SFFSegmentList.from_json(S_json)
        self.assertEqual(S, S2)

    def test_hff(self):
        """Interconvert to HDF5"""
        # empty
        S = adapter.SFFSegmentList()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = S.as_hff(group)
            self.assertIn(u'segment_list', group)
            self.assertEqual(len(group[u'segment_list']), 0)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            S2 = adapter.SFFSegmentList.from_hff(h[u'container'])
            self.assertEqual(S, S2)
        # non-empty
        S = adapter.SFFSegmentList()
        for _ in _xrange(_random_integer(start=3, stop=5)):
            external_references = adapter.SFFExternalReferenceList()
            [external_references.append(
                adapter.SFFExternalReference(
                    resource=rw.random_word(),
                    url='https://{}.com/{}/{}'.format(*rw.random_words(count=3)),
                    accession=rw.random_word(),
                    label=' '.join(rw.random_words(count=2)),
                    description=li.get_sentence(),
                )
            ) for _ in _xrange(_random_integer(start=2, stop=5))]
            biological_annotation = adapter.SFFBiologicalAnnotation(
                name=' '.join(rw.random_words(count=3)),
                description=li.get_sentence(),
                external_references=external_references,
            )
            mesh_list = adapter.SFFMeshList()
            [mesh_list.append(
                adapter.SFFMesh(
                    vertices=adapter.SFFVertices.from_array(numpy.random.rand(4, 3)),
                    triangles=adapter.SFFTriangles.from_array(numpy.random.randint(0, 4, size=(4, 3)))
                )
            ) for _ in _xrange(_random_integer(start=3, stop=5))]
            shape_primitive_list = adapter.SFFShapePrimitiveList()
            [shape_primitive_list.append(
                random.choice([
                    adapter.SFFCone(height=_random_float(multiplier=10), bottom_radius=_random_float(multiplier=10)),
                    adapter.SFFCylinder(height=_random_float(multiplier=10), diameter=_random_float(multiplier=10)),
                    adapter.SFFCuboid(x=_random_float(multiplier=10), y=_random_float(multiplier=10),
                                      z=_random_float(multiplier=10)),
                    adapter.SFFEllipsoid(x=_random_float(multiplier=10), y=_random_float(multiplier=10),
                                         z=_random_float(multiplier=10))
                ])
            ) for _ in _xrange(_random_integer(start=3, stop=6))]
            s = adapter.SFFSegment(
                colour=adapter.SFFRGBA(random_colour=True),
                biological_annotation=biological_annotation,
                mesh_list=mesh_list,
                three_d_volume=adapter.SFFThreeDVolume(
                    lattice_id=_random_integer(),
                    value=_random_integer(),
                ),
                shape_primitive_list=shape_primitive_list,
            )
            S.append(s)
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = S.as_hff(group)
            self.assertIn(u'segment_list', group)
            self.assertEqual(len(group[u'segment_list']), len(S))
            for i, segment in enumerate(S, start=1):
                self.assertEqual(segment, adapter.SFFSegment.from_hff(group['segment_list/{}'.format(i)]))
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            S2 = adapter.SFFSegmentList.from_hff(h[u'container'])
            self.assertEqual(S, S2)


class TestSFFSoftware(Py23FixTestCase):
    """Test the SFFSoftware class"""

    def tearDown(self):
        adapter.SFFSoftware.reset_id()

    def test_default(self):
        """Test default settings"""
        S = adapter.SFFSoftware()
        self.assertRegex(
            _str(S),
            r"""SFFSoftware\(id={}, name={}, version={}, processing_details={}\)""".format(
                S.id, None, None, None
            )
        )
        self.assertEqual(S.id, 0)
        self.assertIsNone(S.name)
        self.assertIsNone(S.version)
        self.assertIsNone(S.processing_details)
        # change ID
        _id = _random_integer()
        name = rw.random_word()
        version = rw.random_word()
        S = adapter.SFFSoftware(id=_id, name=name, version=version)
        self.assertEqual(S.id, _id)
        self.assertRegex(
            _str(S),
            r"""SFFSoftware\(id={}, name="{}", version="{}", processing_details={}\)""".format(
                S.id, name, version, None
            )
        )
        # set values
        name = ' '.join(rw.random_words(count=3))
        version = rw.random_word()
        processing_details = li.get_sentences(sentences=10)
        S = adapter.SFFSoftware(
            name=name,
            version=version,
            processing_details=processing_details,
        )
        self.assertRegex(
            _str(S),
            r"""SFFSoftware\(id={}, name="{}", version="{}", processing_details="{}"\)""".format(
                S.id, name, version, processing_details
            )
        )
        self.assertEqual(S.name, name)
        self.assertEqual(S.version, version)
        self.assertEqual(S.processing_details, processing_details)

    def test_create_from_gds_type(self):
        """Test that we can create from gds_type"""
        _S = emdb_sff.software_type()
        S = adapter.SFFSoftware.from_gds_type(_S)
        self.assertRegex(
            _str(S),
            r"""SFFSoftware\(id={}, name={}, version={}, processing_details={}\)""".format(
                S.id, None, None, None
            )
        )
        self.assertIsNone(S.id)
        self.assertIsNone(S.name)
        self.assertIsNone(S.version)
        self.assertIsNone(S.processing_details)
        # no id
        name = rw.random_word()
        version = rw.random_word()
        processing_details = li.get_sentences(sentences=_random_integer(start=2, stop=5))
        _S = emdb_sff.software_type(
            name=name,
            version=version,
            processing_details=processing_details
        )
        S = adapter.SFFSoftware.from_gds_type(_S)
        self.assertRegex(
            _str(S),
            r"""SFFSoftware\(id=None, name=".+", version=".+", processing_details=".+"\)"""
        )
        self.assertIsNone(S.id)
        self.assertEqual(S.name, name)
        self.assertEqual(S.version, version)
        self.assertEqual(S.processing_details, processing_details)
        # with id
        _id = _random_integer()
        name = rw.random_word()
        version = rw.random_word()
        processing_details = li.get_sentences(sentences=_random_integer(start=2, stop=5))
        _S = emdb_sff.software_type(
            id=_id,
            name=name,
            version=version,
            processing_details=processing_details
        )
        S = adapter.SFFSoftware.from_gds_type(_S)
        self.assertRegex(
            _str(S),
            r"""SFFSoftware\(id=\d+, name=".+", version=".+", processing_details=".+"\)"""
        )
        self.assertEqual(S.id, _id)
        self.assertEqual(S.name, name)
        self.assertEqual(S.version, version)
        self.assertEqual(S.processing_details, processing_details)

    def test_json(self):
        """Interconvert to JSON"""
        s = adapter.SFFSoftware(
            name=rw.random_word(),
            version=rw.random_word(),
            processing_details=li.get_sentences(sentences=5)
        )
        s_json = s.as_json()
        self.assertEqual(s.name, s_json[u'name'])
        self.assertEqual(s.version, s_json[u'version'])
        self.assertEqual(s.processing_details, s_json[u'processing_details'])
        s2 = adapter.SFFSoftware.from_json(s_json)
        self.assertEqual(s, s2)

    def test_hff(self):
        """Interconvert HDF5"""
        # empty
        s = adapter.SFFSoftware()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = s.as_hff(group)
            group_name = u'{}'.format(s.id)
            self.assertIn(group_name, group)
            self.assertIn(group_name + u'/id', group)
            self.assertNotIn(group_name + u'/name', group)
            self.assertNotIn(group_name + u'/version', group)
            self.assertNotIn(group_name + u'/processing_details', group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                s2 = adapter.SFFSoftware.from_hff(group)
                self.assertEqual(s, s2)
        # non-empty
        s = adapter.SFFSoftware(
            name=rw.random_word(),
            version='v{}.{}.{}'.format(*_random_integers(count=3, start=1, stop=10)),
            processing_details=li.get_sentences(sentences=3),
        )
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = s.as_hff(group)
            group_name = u'{}'.format(s.id)
            self.assertIn(group_name, group)
            self.assertIn(group_name + u'/id', group)
            self.assertIn(group_name + u'/name', group)
            self.assertIn(group_name + u'/version', group)
            self.assertIn(group_name + u'/processing_details', group)
            self.assertEqual(group[group_name + u'/id'][()], s.id)
            self.assertEqual(group[group_name + u'/name'][()], s.name)
            self.assertEqual(group[group_name + u'/version'][()], s.version)
            self.assertEqual(group[group_name + u'/processing_details'][()], s.processing_details)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                s2 = adapter.SFFSoftware.from_hff(group)
                self.assertEqual(s, s2)


class TestSFFSoftwareList(Py23FixTestCase):
    """Test the SFFSoftwareList class"""

    def test_default(self):
        """Default use case"""
        S = adapter.SFFSoftwareList()
        _no_items = _random_integer(start=2, stop=10)
        [S.append(adapter.SFFSoftware()) for _ in _xrange(_no_items)]
        self.assertEqual(len(S), _no_items)
        self.assertEqual(list(S.get_ids()), list(_xrange(_no_items)))
        self.assertRegex(
            _str(S),
            r"""SFFSoftwareList\(\[SFFSoftware\(.*\)\]\)"""
        )
        # add without an ID; no change in the result of .get_ids()
        S.append(
            adapter.SFFSoftware.from_gds_type(emdb_sff.software_type())
        )
        self.assertEqual(list(S.get_ids()), list(_xrange(_no_items)))
        # prevent adding an item with an ID present
        with self.assertRaisesRegex(KeyError, r".*already present.*"):
            S.append(adapter.SFFSoftware(id=0))

    def test_create_from_gds_type(self):
        """Create direct from the gds_type"""
        _S = emdb_sff.software_listType()
        _no_items = _random_integer(start=2, stop=10)
        _S.set_software([
            emdb_sff.software_type(
                id=i,
            ) for i in _xrange(_no_items)]
        )
        S = adapter.SFFSoftwareList.from_gds_type(_S)
        self.assertRegex(
            _str(S),
            r"""SFFSoftwareList\(\[SFFSoftware\(.*\)\]\)"""
        )
        self.assertEqual(len(S), _no_items)
        self.assertEqual(list(S.get_ids()), list(_xrange(_no_items)))

    def test_json(self):
        """Interconvert to JSON"""
        sl = adapter.SFFSoftwareList()
        no_sw = _random_integer(start=2, stop=5)
        [sl.append(
            adapter.SFFSoftware(
                name=rw.random_word(),
                version=rw.random_word(),
                processing_details=li.get_sentences(sentences=5),
            )
        ) for _ in _xrange(no_sw)]
        sl_json = sl.as_json()
        self.assertEqual(len(sl), no_sw)
        self.assertEqual(sl_json, [{
            u'id': sw.id,
            u'name': sw.name,
            u'version': sw.version,
            u'processing_details': sw.processing_details
        } for sw in sl])
        sw2 = adapter.SFFSoftwareList.from_json(sl_json)
        self.assertEqual(sl, sw2)

    def test_hff(self):
        """Interconvert to HDF5"""
        # empty
        S = adapter.SFFSoftwareList()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = S.as_hff(group)
            self.assertIn(u'software_list', group)
            self.assertEqual(len(group[u'software_list']), 0)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            S2 = adapter.SFFSoftwareList.from_hff(h[u'container'])
            self.assertEqual(S, S2)
        # non-empty
        S = adapter.SFFSoftwareList()
        [S.append(
            adapter.SFFSoftware(
                name=rw.random_word(),
                version='v{}.{}.{}'.format(*_random_integers(count=3, start=1, stop=10)),
                processing_details=li.get_sentences(sentences=3),
            )
        ) for _ in _xrange(_random_integer(start=2, stop=8))]
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = S.as_hff(group)
            self.assertIn(u'software_list', group)
            self.assertEqual(len(group[u'software_list']), len(S))
            for i, sw in enumerate(S):
                self.assertEqual(sw, adapter.SFFSoftware.from_hff(group[u'software_list/{}'.format(i)]))
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            S2 = adapter.SFFSoftwareList.from_hff(h[u'container'])
            self.assertEqual(S, S2)


class TestSFFTransformationMatrix(Py23FixTestCase):
    def setUp(self):
        self.rows, self.cols = _random_integer(start=2, stop=5), _random_integer(start=6, stop=10)
        self.data = numpy.random.rand(self.rows, self.cols)
        self.data_string = " ".join(list(map(repr, self.data.flatten().tolist())))

    def tearDown(self):
        adapter.SFFTransformationMatrix.reset_id()

    def test_stringify(self):
        """Test that we can convert a numpy array to a string"""
        self.data_string = adapter.SFFTransformationMatrix.stringify(self.data)
        self.assertEqual(len(self.data_string.split(' ')), self.rows * self.cols)  # correct number of items
        new_array = numpy.fromstring(self.data_string, sep=' ').reshape(self.rows, self.cols)
        self.assertTrue(numpy.array_equal(self.data, numpy.array(new_array)))

    def test_from_array(self):
        """Test default configs for a SFFTransformationMatrix object"""
        # create from array
        T = adapter.SFFTransformationMatrix.from_array(self.data)  # implicitly infer matrix dims
        self.assertEqual(T.id, 0)
        self.assertEqual(T.rows, self.rows)
        self.assertEqual(T.cols, self.cols)
        self.assertEqual(T.data, self.data_string)
        self.assertTrue(numpy.array_equal(T.data_array, self.data))

    def test_create_array(self):
        # create from constructor using numpy
        T = adapter.SFFTransformationMatrix(
            rows=self.rows,
            cols=self.cols,
            data=self.data
        )
        self.assertEqual(T.id, 0)
        self.assertEqual(T.rows, self.rows)
        self.assertEqual(T.cols, self.cols)
        print(T.data)
        print(self.data_string)
        self.assertEqual(T.data, self.data_string)
        self.assertTrue(numpy.array_equal(T.data_array, self.data))

    def test_create_array_implicit(self):
        # create from constructor using numpy without specifying rows and cols
        T = adapter.SFFTransformationMatrix(
            data=self.data
        )
        self.assertEqual(T.id, 0)
        self.assertEqual(T.rows, self.rows)
        self.assertEqual(T.cols, self.cols)
        self.assertEqual(T.data, self.data_string)
        self.assertTrue(numpy.array_equal(T.data_array, self.data))

    def test_create_string(self):
        # create from constructor using string
        T = adapter.SFFTransformationMatrix(
            rows=self.rows,
            cols=self.cols,
            data=self.data_string
        )
        self.assertEqual(T.id, 0)
        self.assertEqual(T.rows, self.rows)
        self.assertEqual(T.cols, self.cols)
        self.assertEqual(T.data, self.data_string)
        self.assertTrue(numpy.array_equal(T.data_array, self.data))

    def test_create_post_hoc(self):
        # create empty then populate data
        T = adapter.SFFTransformationMatrix()
        T.data_array = self.data
        self.assertEqual(T.id, 0)
        self.assertEqual(T.rows, self.rows)
        self.assertEqual(T.cols, self.cols)
        self.assertEqual(T.data, self.data_string)
        self.assertTrue(numpy.array_equal(T.data_array, self.data))
        # exception
        with self.assertRaisesRegex(ValueError, r"not a numpy array"):
            T.data_array = list(range(20))

    def test_exceptions(self):
        # exceptions
        # wrong dimensions
        print(self.rows, self.rows)
        print(self.data.shape)
        with self.assertRaisesRegex(ValueError, r".*incompatible rows/cols and array.*"):
            T = adapter.SFFTransformationMatrix(
                rows=self.rows,
                cols=self.rows,
                data=self.data_string
            )
            print(T)

    def test_create_from_gds_type(self):
        # with id
        _id = _random_integer()
        _T = emdb_sff.transformation_matrix_type(
            id=_id,
            rows=self.rows,
            cols=self.cols,
            data=self.data_string,
        )
        T = adapter.SFFTransformationMatrix.from_gds_type(_T)
        self.assertEqual(T.id, _id)
        self.assertEqual(T.rows, self.rows)
        self.assertEqual(T.cols, self.cols)
        self.assertEqual(T.data, self.data_string)
        print(T.data_array.flatten().tolist())
        print(self.data.flatten().tolist())
        self.assertTrue(numpy.array_equal(T.data_array, self.data))

        # without id
        _T = emdb_sff.transformation_matrix_type(
            rows=self.rows,
            cols=self.cols,
            data=self.data_string,
        )
        T = adapter.SFFTransformationMatrix.from_gds_type(_T)
        self.assertIsNone(T.id)
        self.assertEqual(T.rows, self.rows)
        self.assertEqual(T.cols, self.cols)
        self.assertEqual(T.data, self.data_string)
        self.assertTrue(numpy.array_equal(T.data_array, self.data))

    def test_json(self):
        """Interconvert to JSON"""
        rows, cols = _random_integers(count=2, start=3, stop=6)
        tx = adapter.SFFTransformationMatrix.from_array(numpy.random.rand(rows, cols))
        tx_json = tx.as_json()
        self.assertEqual(tx.id, tx_json[u'id'])
        self.assertEqual(tx.rows, tx_json[u'rows'])
        self.assertEqual(tx.cols, tx_json[u'cols'])
        self.assertEqual(tx.data, tx_json[u'data'])
        tx2 = adapter.SFFTransformationMatrix.from_json(tx_json)
        self.assertEqual(tx, tx2)

    def test_hff(self):
        """Interconvert HDF5"""
        # empty
        tx = adapter.SFFTransformationMatrix()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = tx.as_hff(group)
            group_name = u'{}'.format(tx.id)
            self.assertIn(group_name, group)
            self.assertIn(group_name + u'/id', group)
            self.assertNotIn(group_name + u'/rows', group)
            self.assertNotIn(group_name + u'/cols', group)
            self.assertNotIn(group_name + u'/data', group)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                tx2 = adapter.SFFTransformationMatrix.from_hff(group)
                self.assertEqual(tx, tx2)
        # non-empty
        tx = adapter.SFFTransformationMatrix.from_array(numpy.random.rand(3, 4))
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = tx.as_hff(group)
            group_name = u'{}'.format(tx.id)
            self.assertIn(group_name, group)
            self.assertIn(group_name + u'/id', group)
            self.assertIn(group_name + u'/rows', group)
            self.assertIn(group_name + u'/cols', group)
            self.assertIn(group_name + u'/data', group)
            self.assertEqual(group[group_name + u'/id'][()], tx.id)
            self.assertEqual(group[group_name + u'/rows'][()], tx.rows)
            self.assertEqual(group[group_name + u'/cols'][()], tx.cols)
            self.assertEqual(group[group_name + u'/data'][()], tx.data)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            for group in h[u'container'].values():
                tx2 = adapter.SFFTransformationMatrix.from_hff(group)
                self.assertEqual(tx, tx2)


class TestSFFTransformList(Py23FixTestCase):
    def setUp(self):
        self.tx_count = _random_integer(start=2, stop=10)
        self.rows, self.cols = _random_integer(start=2, stop=10), _random_integer(start=2, stop=10)
        self.txs = self.get_transforms(self.tx_count, rows=self.rows, cols=self.cols)
        self.gds_txs = self.get_gds_transforms(self.tx_count, rows=self.rows, cols=self.cols)
        self.gds_txs_with_ids = self.get_gds_transforms(self.tx_count, rows=self.rows, cols=self.cols, with_ids=True)

    @staticmethod
    def get_transforms(tx_count, rows=3, cols=4):
        transforms = [
            adapter.SFFTransformationMatrix(
                rows=rows, cols=cols, data=numpy.random.rand(rows, cols)
            ) for _ in _xrange(tx_count)]
        return transforms

    @staticmethod
    def get_gds_transforms(tx_count, rows=3, cols=4, with_ids=False):
        if with_ids:
            _ids = list(_xrange(tx_count))
        else:
            _ids = [None] * tx_count
        transforms = [
            emdb_sff.transformation_matrix_type(
                id=_ids[i],
                rows=rows, cols=cols,
                data=" ".join(list(map(_str, numpy.random.rand(rows, cols).flatten().tolist())))
            ) for i in _xrange(tx_count)
        ]
        return transforms

    def tearDown(self):
        adapter.SFFTransformationMatrix.reset_id()

    def test_default(self):
        TT = adapter.SFFTransformList()
        [TT.append(tx) for tx in self.txs]
        self.assertEqual(self.tx_count, len(TT))
        self.assertEqual(list(TT.get_ids()), list(_xrange(self.tx_count)))

    def test_min_length(self):
        """Test validation of minimum length"""
        TT = adapter.SFFTransformList()
        with self.assertRaisesRegex(base.SFFValueError, r".*export failed due to validation error.*"):
            TT.export(sys.stderr)

    def test_create_from_gds_type(self):
        """Test that we can create from gds_types"""
        # without ids
        _TT = emdb_sff.transform_listType(self.gds_txs)
        TT = adapter.SFFTransformList.from_gds_type(_TT)
        self.assertEqual(self.tx_count, len(TT))
        self.assertEqual(len(TT.get_ids()), 0)
        # with ids
        _TT = emdb_sff.transform_listType(self.gds_txs_with_ids)
        TT = adapter.SFFTransformList.from_gds_type(_TT)
        self.assertEqual(self.tx_count, len(TT))
        self.assertEqual(list(TT.get_ids()), list(_xrange(len(TT))))

    def test_json(self):
        """Interconvert to JSON"""
        tl = adapter.SFFTransformList()
        no_txs = _random_integer(start=2, stop=5)
        [tl.append(adapter.SFFTransformationMatrix.from_array(numpy.random.rand(3, 4))) for _ in _xrange(no_txs)]
        tl_json = tl.as_json()
        self.assertEqual(len(tl), no_txs)
        self.assertEqual(tl_json, [{
            u'id': tx.id,
            u'rows': tx.rows,
            u'cols': tx.cols,
            u'data': tx.data
        } for tx in tl])
        tl2 = adapter.SFFTransformList.from_json(tl_json)
        self.assertEqual(tl, tl2)

    def test_hff(self):
        """Interconvert to HDF5"""
        # empty
        T = adapter.SFFTransformList()
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = T.as_hff(group)
            self.assertIn(u'transform_list', group)
            self.assertEqual(len(group[u'transform_list']), 0)
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            T2 = adapter.SFFTransformList.from_hff(h[u'container'])
            self.assertEqual(T, T2)
        # non-empty
        T = adapter.SFFTransformList()
        [T.append(
            adapter.SFFTransformationMatrix.from_array(numpy.random.rand(3, 4))
        ) for _ in _xrange(_random_integer(start=2, stop=8))]
        with h5py.File(self.test_hdf5_fn, u'w') as h:
            group = h.create_group(u'container')
            group = T.as_hff(group)
            self.assertIn(u'transform_list', group)
            self.assertEqual(len(group[u'transform_list']), len(T))
            for i, tx in enumerate(T):
                self.assertEqual(tx, adapter.SFFTransformationMatrix.from_hff(group[u'transform_list/{}'.format(i)]))
        with h5py.File(self.test_hdf5_fn, u'r') as h:
            T2 = adapter.SFFTransformList.from_hff(h[u'container'])
            self.assertEqual(T, T2)


class TestSFFSegmentation(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        # empty segmentation object
        segmentation = adapter.SFFSegmentation()  # 3D volume
        segmentation.name = rw.random_word()
        segmentation.primary_descriptor = u"three_d_volume"
        # transforms
        transforms = adapter.SFFTransformList()
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=numpy.random.rand(3, 4),
            )
        )
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=numpy.random.rand(3, 4)
            )
        )
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=numpy.random.rand(3, 4)
            )
        )
        # bounding_box
        xmax = _random_integer(start=500)
        ymax = _random_integer(start=500)
        zmax = _random_integer(start=500)
        segmentation.bounding_box = adapter.SFFBoundingBox(
            xmax=xmax,
            ymax=ymax,
            zmax=zmax
        )
        # lattice container
        lattices = adapter.SFFLatticeList()
        # lattice 1
        binlist = numpy.array([random.randint(0, 5) for i in _xrange(20 * 20 * 20)]).reshape(20, 20, 20)
        lattice = adapter.SFFLattice(
            mode=u'uint32',
            endianness=u'little',
            size=adapter.SFFVolumeStructure(cols=20, rows=20, sections=20),
            start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
            data=binlist,
        )
        lattices.append(lattice)
        # lattice 2
        binlist2 = numpy.array([random.random() * 100 for i in _xrange(30 * 40 * 50)]).reshape(30, 40, 50)
        lattice2 = adapter.SFFLattice(
            mode=u'float32',
            endianness=u'big',
            size=adapter.SFFVolumeStructure(cols=30, rows=40, sections=50),
            start=adapter.SFFVolumeIndex(cols=-50, rows=-40, sections=100),
            data=binlist2,
        )
        lattices.append(lattice2)
        # segments
        segments = adapter.SFFSegmentList()
        # segment one
        segment = adapter.SFFSegment()
        vol1_value = 1
        segment.three_d_volume = adapter.SFFThreeDVolume(
            lattice_id=0,
            value=vol1_value,
        )
        segment.colour = adapter.SFFRGBA(random_colour=True)
        segments.append(segment)
        # segment two
        segment = adapter.SFFSegment()
        vol2_value = 37.1
        segment.three_d_volume = adapter.SFFThreeDVolume(
            lattice_id=1,
            value=vol2_value
        )
        segment.colour = adapter.SFFRGBA(random_colour=True)
        # add segment to segments
        segments.append(segment)
        segmentation.transforms = transforms
        segmentation.segments = segments
        segmentation.lattices = lattices
        cls.segmentation = segmentation
        cls.shape_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'test_shape_segmentation.sff')
        cls.three_d_volume_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'test_3d_segmentation.sff')
        cls.mesh_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'test_mesh_segmentation.sff')

    @classmethod
    def tearDownClass(cls):
        """Remove files from disk"""
        if os.path.exists(cls.shape_file):
            os.remove(cls.shape_file)
        if os.path.exists(cls.three_d_volume_file):
            os.remove(cls.three_d_volume_file)
        if os.path.exists(cls.mesh_file):
            os.remove(cls.mesh_file)

    @staticmethod
    def get_mesh_components(count=20):
        vertices = numpy.random.rand(count, 3)
        normals = numpy.random.rand(count, 3)
        triangles = numpy.random.randint(0, count, size=(count, 3))
        return vertices, normals, triangles

    def test_create_3D(self):
        """Create an SFFSegmentation object with 3D volume segmentation from scratch"""
        segmentation = adapter.SFFSegmentation()
        segmentation.name = rw.random_word()
        segmentation.primary_descriptor = u"three_d_volume"
        # transforms
        transforms = adapter.SFFTransformList()
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(_str, range(12)))
            )
        )
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(_str, range(12)))
            )
        )
        transforms.append(
            adapter.SFFTransformationMatrix(
                rows=3,
                cols=4,
                data=" ".join(map(_str, range(12)))
            )
        )
        # bounding_box
        xmax = _random_integer(start=500)
        ymax = _random_integer(start=500)
        zmax = _random_integer(start=500)
        segmentation.bounding_box = adapter.SFFBoundingBox(
            xmax=xmax,
            ymax=ymax,
            zmax=zmax
        )
        # lattice container
        lattices = adapter.SFFLatticeList()
        # lattice 1
        # binlist = numpy.array([random.randint(0, 5) for i in _xrange(20 * 20 * 20)]).reshape(20, 20, 20)
        binlist = numpy.random.randint(0, 5, size=(20, 20, 20))
        lattice = adapter.SFFLattice(
            mode=u'uint32',
            endianness=u'little',
            size=adapter.SFFVolumeStructure(cols=20, rows=20, sections=20),
            start=adapter.SFFVolumeIndex(cols=0, rows=0, sections=0),
            data=binlist,
        )
        lattices.append(lattice)
        # lattice 2
        # binlist2 = numpy.array([random.random() * 100 for i in _xrange(30 * 40 * 50)]).reshape(30, 40, 50)
        binlist2 = numpy.random.rand(30, 40, 50) * 100
        lattice2 = adapter.SFFLattice(
            mode=u'float32',
            endianness=u'big',
            size=adapter.SFFVolumeStructure(cols=30, rows=40, sections=50),
            start=adapter.SFFVolumeIndex(cols=-50, rows=-40, sections=100),
            data=binlist2,
        )
        lattices.append(lattice2)
        # segments
        segments = adapter.SFFSegmentList()
        # segment one
        segment = adapter.SFFSegment(colour=adapter.SFFRGBA(random_colour=True))
        vol1_value = 1
        segment.three_d_volume = adapter.SFFThreeDVolume(
            lattice_id=0,
            value=vol1_value,
        )
        segments.append(segment)
        # segment two
        segment = adapter.SFFSegment(colour=adapter.SFFRGBA(random_colour=True))
        vol2_value = 37.1
        segment.three_d_volume = adapter.SFFThreeDVolume(
            lattice_id=1,
            value=vol2_value
        )
        # add segment to segments
        segments.append(segment)
        segmentation.transforms = transforms
        segmentation.segments = segments
        segmentation.lattices = lattices
        # export
        # self.stderr(segmentation)
        # self.stderrj(segmentation.as_json())
        segmentation.export(self.three_d_volume_file)
        # assertions
        self.assertRegex(
            _str(segmentation),
            r"""SFFSegmentation\(name="\w+", version="{}"\)""".format(
                EMDB_SFF_VERSION
            )
        )
        self.assertEqual(segmentation.primary_descriptor, u"three_d_volume")
        self.assertEqual(segmentation.bounding_box.xmin, 0)
        self.assertEqual(segmentation.bounding_box.xmax, xmax)
        self.assertEqual(segmentation.bounding_box.ymin, 0)
        self.assertEqual(segmentation.bounding_box.ymax, ymax)
        self.assertEqual(segmentation.bounding_box.zmin, 0)
        self.assertEqual(segmentation.bounding_box.zmax, zmax)
        # test the number of transforms
        self.assertTrue(len(segmentation.transforms) > 0)
        # test the transform IDs
        t_ids = map(lambda t: t.id, segmentation.transforms)
        self.assertCountEqual(t_ids, range(3))
        # segments
        self.assertEqual(len(segmentation.segments), 2)
        # segment one
        segment = segmentation.segments[0]
        # volume
        self.assertEqual(segment.three_d_volume.lattice_id, 0)
        self.assertEqual(segment.three_d_volume.value, vol1_value)
        # segment two
        segment = segmentation.segments.get_by_id(2)
        # volume
        self.assertEqual(segment.three_d_volume.lattice_id, 1)
        self.assertEqual(segment.three_d_volume.value, vol2_value)
        # lattices
        lattices = segmentation.lattices
        self.assertEqual(len(lattices), 2)
        # lattice one
        lattice1 = lattices.get_by_id(0)
        self.assertEqual(lattice1.mode, u'uint32')
        self.assertEqual(lattice1.endianness, u'little')
        self.assertCountEqual(lattice1.size.value, (20, 20, 20))
        self.assertCountEqual(lattice1.start.value, (0, 0, 0))
        # lattice two
        self.assertEqual(lattice2.mode, u'float32')
        self.assertEqual(lattice2.endianness, u'big')
        self.assertCountEqual(lattice2.size.value, (30, 40, 50))
        self.assertCountEqual(lattice2.start.value, (-50, -40, 100))

    def test_create_shapes(self):
        """Test that we can create a segmentation of shapes programmatically"""
        segmentation = adapter.SFFSegmentation()
        segmentation.name = rw.random_word()
        segmentation.software_list = adapter.SFFSoftwareList()
        segmentation.software_list.append(
            adapter.SFFSoftware(
                name=rw.random_word(),
                version=rw.random_word(),
                processingDetails=li.get_sentence(),
            )
        )
        segmentation.primary_descriptor = u"shape_primitive_list"
        transforms = adapter.SFFTransformList()
        segments = adapter.SFFSegmentList()
        segment = adapter.SFFSegment()
        # shapes
        shapes = adapter.SFFShapePrimitiveList()
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCuboid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCuboid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        cylinder = adapter.SFFCylinder(
            height=_random_float() * 100,
            diameter=_random_float() * 100,
            transformId=transform.id,
        )
        shapes.append(cylinder)
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        ellipsoid = adapter.SFFEllipsoid(
            x=_random_float() * 100,
            y=_random_float() * 100,
            z=_random_float() * 100,
            transformId=transform.id,
        )
        shapes.append(ellipsoid)
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        ellipsoid2 = adapter.SFFEllipsoid(x=_random_float() * 100, y=_random_float() * 100, z=_random_float() * 100,
                                          transformId=transform.id, )
        shapes.append(ellipsoid2)
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottom_radius=_random_float() * 100,
                transform_id=transform.id,
            )
        )
        segment.shape_primitive_list = shapes
        segments.append(segment)
        # more shapes
        segment = adapter.SFFSegment()
        # shapes
        shapes = adapter.SFFShapePrimitiveList()
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottom_radius=_random_float() * 100,
                transform_id=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottom_radius=_random_float() * 100,
                transform_id=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottom_radius=_random_float() * 100,
                transformId=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCuboid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transform_id=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCuboid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transform_id=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCylinder(
                height=_random_float() * 100,
                diameter=_random_float() * 100,
                transform_id=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFEllipsoid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transform_id=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFEllipsoid(
                x=_random_float() * 100,
                y=_random_float() * 100,
                z=_random_float() * 100,
                transform_id=transform.id,
            )
        )
        transform = adapter.SFFTransformationMatrix(
            rows=3,
            cols=4,
            data=" ".join(map(_str, range(12))),
        )
        transforms.append(transform)
        shapes.append(
            adapter.SFFCone(
                height=_random_float() * 100,
                bottomRadius=_random_float() * 100,
                transform_id=transform.id,
            )
        )
        segment.shape_primitive_list = shapes
        segments.append(segment)
        segmentation.segments = segments
        segmentation.transforms = transforms
        # export
        segmentation.export(self.shape_file)
        # assertions
        self.assertEqual(len(segment.shape_primitive_list), 9)
        self.assertEqual(segment.shape_primitive_list.num_cones, 4)
        self.assertEqual(segment.shape_primitive_list.num_cylinders, 1)
        self.assertEqual(segment.shape_primitive_list.num_cuboids, 2)
        self.assertEqual(segment.shape_primitive_list.num_ellipsoids, 2)

    def test_create_meshes(self):
        """Test that we can create a segmentation of meshes programmatically"""
        segmentation = adapter.SFFSegmentation()
        segmentation.name = rw.random_word()
        segmentation.primary_descriptor = u"mesh_list"
        segments = adapter.SFFSegmentList()
        segment = adapter.SFFSegment()
        # meshes
        mesh_list = adapter.SFFMeshList()
        # mesh 1
        count1 = _random_integer(start=3, stop=10)
        vertices1, normals1, triangles1 = self.get_mesh_components(count=count1)
        mesh = adapter.SFFMesh(
            vertices=adapter.SFFVertices.from_array(vertices1),
            normals=adapter.SFFNormals.from_array(normals1),
            triangles=adapter.SFFTriangles.from_array(triangles1)
        )
        # mesh 2
        count2 = _random_integer(start=3, stop=10)
        vertices2, normals2, triangles2 = self.get_mesh_components(count=count2)
        mesh2 = adapter.SFFMesh(
            vertices=adapter.SFFVertices.from_array(vertices2),
            normals=adapter.SFFNormals.from_array(normals2),
            triangles=adapter.SFFTriangles.from_array(triangles2)
        )
        mesh_list.append(mesh)
        mesh_list.append(mesh2)
        segment.mesh_list = mesh_list
        segments.append(segment)
        # segment two
        segment = adapter.SFFSegment()
        # mesh
        mesh_list = adapter.SFFMeshList()
        count3 = _random_integer(start=3, stop=10)
        vertices3, normals3, triangles3 = self.get_mesh_components(count=count3)
        mesh = adapter.SFFMesh(
            vertices=adapter.SFFVertices.from_array(vertices3),
            normals=adapter.SFFNormals.from_array(normals3),
            triangles=adapter.SFFTriangles.from_array(triangles3)
        )
        mesh_list.append(mesh)
        segment.mesh_list = mesh_list
        segments.append(segment)
        segmentation.segments = segments
        # export
        segmentation.export(self.mesh_file)
        # assertions
        # segment one
        segment1 = segmentation.segments.get_by_id(1)
        self.assertEqual(len(segment1.mesh_list), 2)
        mesh1, mesh2 = segment1.mesh_list
        self.assertEqual(len(mesh1.vertices), vertices1.shape[0])
        self.assertEqual(len(mesh1.normals), normals1.shape[0])
        self.assertEqual(len(mesh1.triangles), triangles1.shape[0])
        self.assertEqual(len(mesh2.vertices), vertices2.shape[0])
        self.assertEqual(len(mesh2.normals), normals2.shape[0])
        self.assertEqual(len(mesh2.triangles), triangles2.shape[0])
        # segment two
        segment2 = segmentation.segments.get_by_id(2)
        mesh = segment2.mesh_list[0]
        self.assertEqual(len(segment2.mesh_list), 1)
        self.assertEqual(len(mesh.vertices), vertices3.shape[0])
        self.assertEqual(len(mesh.normals), normals3.shape[0])
        self.assertEqual(len(mesh.triangles), triangles3.shape[0])

    def test_create_annotations(self):
        """Test that we can add annotations programmatically"""
        segmentation = adapter.SFFSegmentation()  # annotation
        segmentation.name = u"name"
        segmentation.software_list = adapter.SFFSoftwareList()
        segmentation.software_list.append(
            adapter.SFFSoftware(
                name=u"Software",
                version=u"1.0.9",
                processing_details=u"Processing details"
            )
        )
        segmentation.details = u"Details"
        # global external references
        segmentation.global_external_references = adapter.SFFGlobalExternalReferenceList()
        segmentation.global_external_references.append(
            adapter.SFFExternalReference(
                resource=u'one',
                url=u'two',
                accession=u'three'
            )
        )
        segmentation.global_external_references.append(
            adapter.SFFExternalReference(
                resource=u'four',
                url=u'five',
                accession=u'six'
            )
        )
        segmentation.segments = adapter.SFFSegmentList()
        segment = adapter.SFFSegment()
        biol_ann = adapter.SFFBiologicalAnnotation()
        biol_ann.name = u"Segment1"
        biol_ann.description = u"Some description"
        # external refs
        biol_ann.external_references = adapter.SFFExternalReferenceList()
        biol_ann.external_references.append(
            adapter.SFFExternalReference(
                resource=u"sldjflj",
                accession=u"doieaik"
            )
        )
        biol_ann.external_references.append(
            adapter.SFFExternalReference(
                resource=u"sljd;f",
                accession=u"20ijalf"
            )
        )
        biol_ann.external_references.append(
            adapter.SFFExternalReference(
                resource=u"lsdjlsd",
                url=u"lsjfd;sd",
                accession=u"23ijlsdjf"
            )
        )
        biol_ann.number_of_instances = 30
        segment.biological_annotation = biol_ann
        # colour
        segment.colour = adapter.SFFRGBA(
            red=1,
            green=0,
            blue=1,
            alpha=0
        )
        segmentation.segments.append(segment)
        # export
        # segmentation.export(os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'test_annotated_segmentation.sff'))
        # assertions
        self.assertEqual(segmentation.name, u'name')
        self.assertEqual(segmentation.version, segmentation._local.schema_version)  # automatically set
        software = segmentation.software_list[0]
        self.assertEqual(software.name, u"Software")
        self.assertEqual(software.version, u"1.0.9")
        self.assertEqual(software.processing_details, u"Processing details")
        self.assertEqual(segmentation.details, u"Details")
        # global external references
        self.assertEqual(segmentation.global_external_references[0].resource, u'one')
        self.assertEqual(segmentation.global_external_references[0].url, u'two')
        self.assertEqual(segmentation.global_external_references[0].accession, u'three')
        self.assertEqual(segmentation.global_external_references[1].resource, u'four')
        self.assertEqual(segmentation.global_external_references[1].url, u'five')
        self.assertEqual(segmentation.global_external_references[1].accession, u'six')
        # segment: biological_annotation
        self.assertEqual(segment.biological_annotation.name, u"Segment1")
        self.assertEqual(segment.biological_annotation.description, u"Some description")
        self.assertEqual(len(segment.biological_annotation.external_references), 3)
        self.assertEqual(segment.biological_annotation.external_references[0].resource, u"sldjflj")
        self.assertEqual(segment.biological_annotation.external_references[0].accession, u"doieaik")
        self.assertEqual(segment.biological_annotation.external_references[1].resource, u"sljd;f")
        self.assertEqual(segment.biological_annotation.external_references[1].accession, u"20ijalf")
        self.assertEqual(segment.biological_annotation.external_references[2].resource, u"lsdjlsd")
        self.assertEqual(segment.biological_annotation.external_references[2].url, u"lsjfd;sd")
        self.assertEqual(segment.biological_annotation.external_references[2].accession, u"23ijlsdjf")
        self.assertEqual(segment.biological_annotation.number_of_instances, 30)
        # colour
        self.assertEqual(segment.colour.value, (1, 0, 1, 0))

    def test_segment_ids(self):
        """to ensure IDs are correctly reset"""
        # segmentation one
        segmentation = adapter.SFFSegmentation()
        segmentation.segments = adapter.SFFSegmentList()
        segment = adapter.SFFSegment()
        segmentation.segments.append(segment)
        # segmentation two
        segmentation2 = adapter.SFFSegmentation()
        segmentation2.segments = adapter.SFFSegmentList()
        segmentation2.segments.append(adapter.SFFSegment())
        # assertions
        self.assertEqual(segmentation.segments[0].id, segmentation2.segments[0].id)

    def test_transform_ids(self):
        """Test that transform ids work correctly"""
        transforms = adapter.SFFTransformList()
        matrix = adapter.SFFTransformationMatrix(rows=3, cols=3, data=' '.join(map(_str, range(9))))
        transforms.append(matrix)

        transforms2 = adapter.SFFTransformList()
        matrix2 = adapter.SFFTransformationMatrix(rows=3, cols=3, data=' '.join(map(_str, range(9))))
        transforms2.append(matrix2)

        self.assertIsNotNone(transforms[0].id)
        self.assertEqual(transforms[0].id, transforms2[0].id)

    def test_read_sff(self):
        """Read from XML (.sff) file"""
        sff_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'emd_1547.sff')
        segmentation = adapter.SFFSegmentation.from_file(sff_file)
        transform = segmentation.transform_list[1]
        # assertions
        self.assertEqual(segmentation.name,
                         u"EMD-1547: Structure of GroEL in complex with non-native capsid protein gp23, Bacteriophage "
                         u"T4 co-chaperone gp31 and ADPAlF3")
        self.assertTrue(len(segmentation.version) > 0)
        software = segmentation.software_list[0]
        self.assertEqual(software.name, u"Segger (UCSF Chimera)")
        self.assertEqual(software.version, u"1.9.7")
        self.assertEqual(
            software.processing_details,
            u"Images were recorded on a 200 kV FEG microscope on photographic film and processed at 2.8 Å/pixel, with "
            u"final data sets of 30,000 and 35,000 side views of the binary and ternary complexes respectively. A "
            u"starting model for the binary complex was obtained by angular reconstitution in IMAGIC32, and our "
            u"previously determined GroEL-ADP-gp31 structure20 was used as a starting model for the ternary complexes. "
            u"The data sets were sorted into classes showing different substrate features by a combination of MSA and "
            u"competitive projection matching10, and the atomic structures of the GroEL subunit domains, gp31 and gp24 "
            u"subunits were docked into the final, asymmetric maps as separate rigid bodies using URO33.")
        self.assertEqual(transform.rows, 3)
        self.assertEqual(transform.cols, 4)
        self.assertEqual(transform.data,
                         u"2.8 0.0 0.0 -226.8 0.0 2.8 0.0 -226.8 0.0 0.0 2.8 -226.8")

    def test_read_hff(self):
        """Read from HDF5 (.hff) file"""
        hff_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'emd_1547.hff')
        segmentation = adapter.SFFSegmentation.from_file(hff_file)
        # assertions
        self.assertEqual(segmentation.name,
                         u"EMD-1547: Structure of GroEL in complex with non-native capsid protein gp23, Bacteriophage "
                         u"T4 co-chaperone gp31 and ADPAlF3")
        self.assertTrue(len(segmentation.version) > 0)
        self.assertEqual(segmentation.version, u"0.8.0.dev1")
        software = segmentation.software_list[0]
        self.assertEqual(software.name, u"Segger (UCSF Chimera)")
        self.assertEqual(software.version, u"1.9.7")
        self.assertEqual(
            software.processing_details,
            u"Images were recorded on a 200 kV FEG microscope on photographic film and processed at 2.8 Å/pixel, with "
            u"final data sets of 30,000 and 35,000 side views of the binary and ternary complexes respectively. A "
            u"starting model for the binary complex was obtained by angular reconstitution in IMAGIC32, and our "
            u"previously determined GroEL-ADP-gp31 structure20 was used as a starting model for the ternary complexes. "
            u"The data sets were sorted into classes showing different substrate features by a combination of MSA and "
            u"competitive projection matching10, and the atomic structures of the GroEL subunit domains, gp31 and gp24 "
            u"subunits were docked into the final, asymmetric maps as separate rigid bodies using URO33.")
        self.assertEqual(segmentation.primary_descriptor, u"three_d_volume")

    def test_read_json(self):
        """Read from JSON (.json) file"""
        json_file = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'emd_1547.json')
        segmentation = adapter.SFFSegmentation.from_file(json_file)
        # assertions
        self.assertEqual(segmentation.name,
                         u"EMD-1547: Structure of GroEL in complex with non-native capsid protein gp23, Bacteriophage "
                         u"T4 co-chaperone gp31 and ADPAlF3")
        self.assertTrue(len(segmentation.version) > 0)
        software = segmentation.software_list[0]
        self.assertEqual(software.name, u"Segger (UCSF Chimera)")
        self.assertEqual(software.version, u"1.9.7")
        self.assertEqual(
            software.processing_details,
            u"Images were recorded on a 200 kV FEG microscope on photographic film and processed at 2.8 Å/pixel, with "
            u"final data sets of 30,000 and 35,000 side views of the binary and ternary complexes respectively. A "
            u"starting model for the binary complex was obtained by angular reconstitution in IMAGIC32, and our "
            u"previously determined GroEL-ADP-gp31 structure20 was used as a starting model for the ternary complexes. "
            u"The data sets were sorted into classes showing different substrate features by a combination of MSA and "
            u"competitive projection matching10, and the atomic structures of the GroEL subunit domains, gp31 and gp24 "
            u"subunits were docked into the final, asymmetric maps as separate rigid bodies using URO33.")

    def test_export_sff(self):
        """Export to an XML (.sff) file"""
        temp_file = tempfile.NamedTemporaryFile()
        self.segmentation.export(temp_file.name + u'.sff')
        # assertions
        with open(temp_file.name + u'.sff') as f:
            self.assertEqual(f.readline(), u'<?xml version="1.0" encoding="UTF-8"?>\n')

    def test_export_hff(self):
        """Export to an HDF5 file"""
        temp_file = tempfile.NamedTemporaryFile()
        self.segmentation.export(temp_file.name + u'.hff')
        # assertions
        with open(temp_file.name + u'.hff', u'rb') as f:
            find = f.readline().find(b'HDF')
            self.assertGreaterEqual(find, 0)

    def test_export_json(self):
        """Export to a JSON file"""
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name += u'.json'
        self.segmentation.to_file(temp_file.name)
        # assertions
        with open(temp_file.name) as f:
            J = json.load(f)
            self.assertEqual(J[u'primary_descriptor'], u"three_d_volume")

    def test_merge_annotation(self):
        """Test that we can merge annotation from one to another"""
        seg1_fn = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'annotated_emd_1014.json')
        seg2_fn = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'emd_1014.json')
        seg1 = adapter.SFFSegmentation.from_file(seg1_fn)
        seg2 = adapter.SFFSegmentation.from_file(seg2_fn)
        # perform the notes merge
        seg1.merge_annotation(seg2)
        self.assertEqual(seg1.global_external_references, seg2.global_external_references)
        for segment in seg1.segment_list:
            other_segment = seg2.segment_list.get_by_id(segment.id)
            self.assertEqual(segment.biological_annotation.external_references, other_segment.biological_annotation.external_references)

    def test_copy_annotation(self):
        """Test that we can copy annotations: global and local"""
        seg_fn = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'emd_1014.json')
        seg = adapter.SFFSegmentation.from_file(seg_fn)
        segment_ids = list(seg.segment_list.get_ids())
        from_segment_id = random.choice(segment_ids)
        from_segment = seg.segment_list.get_by_id(from_segment_id)
        segment_ids.remove(from_segment_id)
        try:
            to_segment_ids = random.choices(segment_ids, k=len(segment_ids)//2)
        except AttributeError:
            to_segment_ids = list(set([random.choice(segment_ids) for _ in _xrange(len(segment_ids)//2)]))
        # clear annotations; check no annotations left
        for segment_id in to_segment_ids:
            segment = seg.segment_list.get_by_id(segment_id)
            segment.biological_annotation.external_references.clear()
            self.assertEqual(len(segment.biological_annotation.external_references), 0)
        # copy annotations
        # noinspection PyStatementEffect
        (seg.copy_annotation(from_segment_id, to_id) for to_id in to_segment_ids)
        # now ensure they are similar to the one copied from
        for segment_id in to_segment_ids:
            segment = seg.segment_list.get_by_id(segment_id)
            self.assertEqual(segment.biological_annotation.external_references, from_segment.biological_annotation.external_references)
        # for global
        seg.global_external_references.clear()
        self.assertEqual(len(seg.global_external_references), 0)
        seg.copy_annotation(from_segment_id, -1) # -1 for global
        self.assertEqual(len(from_segment.biological_annotation.external_references), len(seg.global_external_references))
        for i, er in enumerate(from_segment.biological_annotation.external_references):
            self.assertEqual(er, seg.global_external_references[i])

    def test_clear_annotation(self):
        """Test that we can clear annotations"""
        seg_fn = os.path.join(TEST_DATA_PATH, u'sff', u'v0.8', u'emd_1014.json')
        seg = adapter.SFFSegmentation.from_file(seg_fn)
        # global
        self.assertTrue(len(seg.global_external_references) > 0)
        seg.clear_annotation(-1)
        self.assertEqual(len(seg.global_external_references), 0)
        # local
        segment_ids = list(seg.segment_list.get_ids())
        from_segment_id = random.choice(segment_ids)
        from_segment = seg.segment_list.get_by_id(from_segment_id)
        self.assertTrue(len(from_segment.biological_annotation.external_references) > 0)
        seg.clear_annotation(from_segment_id)
        self.assertEqual(len(from_segment.biological_annotation.external_references), 0)


