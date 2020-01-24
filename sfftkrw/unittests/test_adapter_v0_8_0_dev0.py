# -*- coding: utf-8 -*-
from __future__ import print_function

import importlib
import os
import random
import sys

import numpy
from random_words import RandomWords, LoremIpsum

from . import TEST_DATA_PATH, Py23FixTestCase, _random_integer, _random_float
from .. import EMDB_SFF_VERSION
from ..core import _str, _xrange, _decode, _print, _bytes
from ..schema import base

rw = RandomWords()
li = LoremIpsum()

adapter_name = 'sfftkrw.schema.adapter_{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_')
)
adapter = importlib.import_module(adapter_name)

# dynamically import the latest schema generateDS API
emdb_sff_name = 'sfftkrw.schema.{schema_version}'.format(
    schema_version=EMDB_SFF_VERSION.replace('.', '_')
)
emdb_sff = importlib.import_module(emdb_sff_name)


class TestSFFRGBA(Py23FixTestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_hdf5_fn = os.path.join(TEST_DATA_PATH, u'sff', u'v0.7', u'test.hdf5')

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.test_hdf5_fn)
        except FileNotFoundError:
            pass

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

    # def test_as_hff(self):
    #     """Test convert to HDF5 group"""
    #     colour = adapter.SFFRGBA(
    #         red=self.red,
    #         green=self.green,
    #         blue=self.blue,
    #         alpha=self.alpha
    #     )
    #     with h5py.File(self.test_hdf5_fn, u'w') as h:
    #         group = h.create_group(u"container")
    #         group = colour.as_hff(group)
    #         self.assertIn(u"colour", group)
    #         self.assertCountEqual(group[u'colour'][()], colour.value)

    # def test_from_hff(self):
    #     """Test create from HDF5 group"""
    #     colour = adapter.SFFRGBA(
    #         red=self.red,
    #         green=self.green,
    #         blue=self.blue,
    #         alpha=self.alpha
    #     )
    #     with h5py.File(self.test_hdf5_fn, u'w') as h:
    #         group = h.create_group(u"container")
    #         group = colour.as_hff(group)
    #         self.assertIn(u"colour", group)
    #         self.assertCountEqual(group[u'colour'][()], colour.value)
    #         colour2 = adapter.SFFRGBA.from_hff(h[u'container'])
    #         self.assertCountEqual(colour.value, colour2.value)

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

    # def test_as_json(self):
    #     """Test export to JSON"""
    #     # empty
    #     c = adapter.SFFRGBA()
    #     with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
    #         c.as_json()
    #     # populated
    #     c = adapter.SFFRGBA(random_colour=True)
    #     c_json = c.as_json()
    #     # _print(c_json)
    #     self.assertEqual(c_json[u'colour'], c.value)

    # def test_from_json(self):
    #     """Test import from JSON"""
    #     c_json = {'colour': (0.8000087483646712, 0.017170600210644427, 0.5992636068532492, 1.0)}
    #     c = adapter.SFFRGBA.from_json(c_json)
    #     # _print(c)
    #     self.assertEqual(c.value, c_json[u'colour'])


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

    # def test_as_json(self):
    #     """Test that we can output as JSON"""
    #     e = adapter.SFFExternalReference(
    #         resource=self.r,
    #         url=self.u,
    #         accession=self.a,
    #         label=self.l,
    #         description=self.d,
    #     )
    #     e_json = e.as_json()
    #     self.assertEqual(e_json[u'id'], e.id)
    #     self.assertEqual(e_json[u'type'], e.resource)
    #     self.assertEqual(e_json[u'otherType'], e.other_type)
    #     self.assertEqual(e_json[u'value'], e.accession)
    #     self.assertEqual(e_json[u'label'], e.label)
    #     self.assertEqual(e_json[u'description'], e.description)
    #     # missing mandatory
    #     e = adapter.SFFExternalReference(
    #         # resource=self.r,
    #         # url=self.u,
    #         # accession=self.a,
    #         label=self.l,
    #         description=self.d,
    #     )
    #     with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
    #         e.as_json()
    #     # missing non-mandatory
    #     e = adapter.SFFExternalReference(
    #         resource=self.r,
    #         url=self.u,
    #         accession=self.a,
    #         # label=self.l,
    #         # description=self.d,
    #     )
    #     self.assertEqual(e_json[u'type'], e.resource)
    #     self.assertEqual(e_json[u'otherType'], e.other_type)
    #     self.assertEqual(e_json[u'value'], e.accession)

    # def test_from_json(self):
    #     """Test that we can recreate from JSON"""
    #     e_json = {'id': 0, 'type': 'symptom', 'otherType': 'thin', 'value': 'definitions',
    #               'label': 'chairpersons swabs pools',
    #               'description': 'Malesuada facilisinam elitduis mus dis facer, primis est pellentesque integer dapibus '
    #                              'semper semvestibulum curae lacusnulla.'}
    #     e = adapter.SFFExternalReference.from_json(e_json)
    #     self.assertEqual(e_json[u'id'], e.id)
    #     self.assertEqual(e_json[u'type'], e.resource)
    #     self.assertEqual(e_json[u'otherType'], e.other_type)
    #     self.assertEqual(e_json[u'value'], e.accession)
    #     self.assertEqual(e_json[u'label'], e.label)
    #     self.assertEqual(e_json[u'description'], e.description)
    #     # missing mandatory
    #     e_json = {'id': 0, 'otherType': 'thin', 'value': 'definitions',
    #               'label': 'chairpersons swabs pools',
    #               'description': 'Malesuada facilisinam elitduis mus dis facer, primis est pellentesque integer dapibus '
    #                              'semper semvestibulum curae lacusnulla.'}
    #     with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
    #         adapter.SFFExternalReference.from_json(e_json)
    #     # missing non-mandatory
    #     e_json = {'type': 'symptom', 'otherType': 'thin', 'value': 'definitions',
    #               'label': 'chairpersons swabs pools'}
    #     e = adapter.SFFExternalReference.from_json(e_json)
    #     self.assertIsNone(e.id)
    #     self.assertEqual(e_json[u'type'], e.resource)
    #     self.assertEqual(e_json[u'otherType'], e.other_type)
    #     self.assertEqual(e_json[u'value'], e.accession)
    #     self.assertEqual(e_json[u'label'], e.label)
    #     self.assertIsNone(e.description)


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
        _E.export(sys.stderr, 0)
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

    # def test_as_json(self):
    #     """Test that we can export to JSON"""
    #     ee = [adapter.SFFExternalReference(
    #         resource=self.rr[i],
    #         url=self.uu[i],
    #         accession=self.aa[i],
    #         label=self.ll[i],
    #         description=self.dd[i]
    #     ) for i in _xrange(self._no_items)]
    #     E = adapter.SFFExternalReferenceList()
    #     [E.append(e) for e in ee]
    #     E_json = E.as_json()
    #     # _print(E_json)
    #     for i in _xrange(self._no_items):
    #         self.assertEqual(E[i].id, E_json[i][u'id'])
    #         self.assertEqual(E[i].type, E_json[i][u'type'])
    #         self.assertEqual(E[i].other_type, E_json[i][u'otherType'])
    #         self.assertEqual(E[i].value, E_json[i][u'value'])
    #         self.assertEqual(E[i].label, E_json[i][u'label'])
    #         self.assertEqual(E[i].description, E_json[i][u'description'])
    #     # empty
    #     E = adapter.SFFExternalReferenceList()
    #     E_json = E.as_json()
    #     self.assertEqual(len(E), len(E_json))
    #
    # def test_from_json(self):
    #     """Test that we can import from JSON"""
    #     E_json = [{'id': 0, 'type': 'projectiles', 'otherType': 'blast', 'value': 'injector',
    #                'label': 'bricks breaches crawl',
    #                'description': 'Est facilisicurabitur morbi dapibus volutpat, vestibulumnulla consecteturpraesent velit sempermorbi diaminteger taciti risusdonec accusam.'},
    #               {'id': 1, 'type': 'signals', 'otherType': 'wines', 'value': 'experience',
    #                'label': 'alibi defaults showers',
    #                'description': 'Auctor habitasse amet temporsuspendisse, integer hendrerit nullasuspendisse.'},
    #               {'id': 2, 'type': 'openings', 'otherType': 'pack', 'value': 'augmentations',
    #                'label': 'outing rings tilling',
    #                'description': 'Liberoduis esse nobis semvestibulum bibendumin non, sagittis eget eum massapellentesque eratproin nonummy massaphasellus.'},
    #               {'id': 3, 'type': 'blaze', 'otherType': 'contract', 'value': 'diagrams',
    #                'label': 'sewers weddings telecommunications',
    #                'description': 'Ipsum no luctus ultricies enimsed antesuspendisse.'},
    #               {'id': 4, 'type': 'terms', 'otherType': 'blackboard', 'value': 'nothing',
    #                'label': 'depot trades strikers', 'description': 'Elitr hendrerit tortorvestibulum exerci.'},
    #               {'id': 5, 'type': 'carriage', 'otherType': 'screens', 'value': 'apprehension',
    #                'label': 'signalers hunk wagon', 'description': 'Consequatduis muspellentesque.'},
    #               {'id': 6, 'type': 'lot', 'otherType': 'gums', 'value': 'rim', 'label': 'chatter north clearances',
    #                'description': 'Nostra felis.'},
    #               {'id': 7, 'type': 'outlet', 'otherType': 'actions', 'value': 'twists',
    #                'label': 'compromises additives mirrors',
    #                'description': 'Diaminteger phasellus mi sollicitudin laoreetphasellus possim, himenaeos semvestibulum egestasmauris clita elitnunc suscipit pulvinar.'},
    #               {'id': 8, 'type': 'shears', 'otherType': 'user', 'value': 'view', 'label': 'cable diagram churns',
    #                'description': 'Dolor laoreet adipiscing takimata neque dignissim velit enimaliquam, lobortisetiam mazim nunccurabitur aliquip praesent blandit.'},
    #               {'id': 9, 'type': 'jurisdiction', 'otherType': 'plug', 'value': 'calibrations',
    #                'label': 'oscillation baby males', 'description': 'Iusto aliquam quod orci, aaenean justo luctus.'}]
    #     E = adapter.SFFExternalReferenceList.from_json(E_json)
    #     # _print(E)
    #     for i, extref in enumerate(E_json):
    #         self.assertEqual(E[i].id, extref[u'id'])
    #         self.assertEqual(E[i].type, extref[u'type'])
    #         self.assertEqual(E[i].other_type, extref[u'otherType'])
    #         self.assertEqual(E[i].value, extref[u'value'])
    #         self.assertEqual(E[i].label, extref[u'label'])
    #         self.assertEqual(E[i].description, extref[u'description'])
    #     # invalid
    #     E_json = "sldjfl"  # iterable but invalid
    #     with self.assertRaisesRegex(base.SFFValueError, r".*validation.*"):
    #         adapter.SFFExternalReferenceList.from_json(E_json)


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

    # def test_hff(self):
    #     """Test conversion to and from HDF5"""
    #     # empty case
    #     b_empty = adapter.SFFBiologicalAnnotation()
    #     # _print(b_empty)
    #     hff_f = tempfile.NamedTemporaryFile()
    #     hff_f.name += '.hff'
    #     with h5py.File(hff_f.name, 'w') as h:
    #         group = h.create_group(u'test')
    #         group = b_empty.as_hff(group)
    #
    #         b2_empty = adapter.SFFBiologicalAnnotation.from_hff(group[u'biologicalAnnotation'])
    #         # _print(b2_empty)
    #
    #         self.assertEqual(b_empty.name, b2_empty.name)
    #         self.assertEqual(b_empty.name, b2_empty.name)
    #         self.assertEqual(b_empty.description, b2_empty.description)
    #         self.assertEqual(b_empty.number_of_instances, b2_empty.number_of_instances)
    #         self.assertEqual(b_empty.external_references, b2_empty.external_references)
    #     # get rid of the file
    #     os.remove(hff_f.name)
    #
    #     # non-empty case
    #     b_full = adapter.SFFBiologicalAnnotation()
    #     b_full.name = ' '.join(rw.random_words(count=2))
    #     b_full.description = li.get_sentence()
    #     es = adapter.SFFExternalReferenceList()
    #     no_es = _random_integer(2, 10)
    #     for _ in _xrange(no_es):
    #         e = adapter.SFFExternalReference()
    #         e.type = rw.random_word()
    #         e.other_type = rw.random_word()
    #         e.value = rw.random_word()
    #         e.label = ' '.join(rw.random_words(count=3))
    #         e.description = li.get_sentence()
    #         es.append(e)
    #     b_full.external_references = es
    #     hff_f = tempfile.NamedTemporaryFile()
    #     hff_f.name += '.hff'
    #     # _print(b_full)
    #     with h5py.File(hff_f.name, 'w') as h:
    #         group = h.create_group(u'test')
    #         group = b_full.as_hff(group)
    #
    #         b2_full = adapter.SFFBiologicalAnnotation.from_hff(group[u'biologicalAnnotation'])
    #         # _print(b2_full)
    #
    #         self.assertEqual(b_full.name, b2_full.name)
    #         self.assertEqual(b_full.name, b2_full.name)
    #         self.assertEqual(b_full.description, b2_full.description)
    #         self.assertEqual(b_full.number_of_instances, b2_full.number_of_instances)
    #         self.assertEqual(b_full.external_references, b2_full.external_references)
    #     # get rid of the file
    #     os.remove(hff_f.name)
    #
    # def test_json(self):
    #     """Test conversion to and from JSON"""
    #     # empty case
    #     b_empty = adapter.SFFBiologicalAnnotation()
    #     # # _print(b_empty)
    #     b_json = b_empty.as_json()
    #     # _print(b_json)
    #     b2_empty = adapter.SFFBiologicalAnnotation.from_json(b_json)
    #     # _print(b2_empty)
    #     self.assertEqual(b_empty, b2_empty)
    #     # non-empty case
    #     b_full = adapter.SFFBiologicalAnnotation()
    #     b_full.name = ' '.join(rw.random_words(count=2))
    #     b_full.description = li.get_sentence()
    #     es = adapter.SFFExternalReferenceList()
    #     no_es = _random_integer(2, 10)
    #     for _ in _xrange(no_es):
    #         e = adapter.SFFExternalReference()
    #         e.type = rw.random_word()
    #         e.other_type = rw.random_word()
    #         e.value = rw.random_word()
    #         e.label = ' '.join(rw.random_words(count=3))
    #         e.description = li.get_sentence()
    #         es.append(e)
    #     b_full.external_references = es
    #     b_json = b_full.as_json()
    #     # _print(b_json)
    #     b2_full = adapter.SFFBiologicalAnnotation.from_json(b_json)
    #     # _print(b2_full)
    #     self.assertEqual(b_full, b2_full)
    #
    # def test_from_json(self):
    #     """Test that we can import from JSON"""
    #     b_json = {'name': 'returns agent', 'description': 'Lacus leopraesent risusdonec tempus congue.',
    #               'externalReferences': [{'id': 0, 'type': 'listing', 'otherType': 'antennas', 'value': 'weddings',
    #                                       'label': 'times selection deployment',
    #                                       'description': 'Facilisicurabitur mi sanctus fames dignissim autem.'},
    #                                      {'id': 1, 'type': 'basis', 'otherType': 'leaks', 'value': 'cups',
    #                                       'label': 'yaw workloads house', 'description': 'Nequeetiam habitasse.'},
    #                                      {'id': 2, 'type': 'chance', 'otherType': 'theory', 'value': 'allegation',
    #                                       'label': 'maps chairwomen flashes',
    #                                       'description': 'Suscipit eos pulvinar zzril doming dolores.'}]}
    #     b_full = adapter.SFFBiologicalAnnotation.from_json(b_json)
    #     # _print(b_full)
    #     self.assertEqual(b_full.name, b_json[u'name'])
    #     self.assertEqual(b_full.description, b_json[u'description'])
    #     try:
    #         self.assertEqual(b_full.number_of_instances, b_json[u'numberOfInstances'])
    #     except KeyError:
    #         self.assertEqual(b_full.number_of_instances, 1)
    #     for i, extref in enumerate(b_json[u'externalReferences']):
    #         self.assertEqual(b_full.external_references[i].id, extref[u'id'])
    #         self.assertEqual(b_full.external_references[i].type, extref[u'type'])
    #         self.assertEqual(b_full.external_references[i].other_type, extref[u'otherType'])
    #         self.assertEqual(b_full.external_references[i].value, extref[u'value'])
    #         self.assertEqual(b_full.external_references[i].label, extref[u'label'])
    #         self.assertEqual(b_full.external_references[i].description, extref[u'description'])


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


class TestSFFVolumeIndex(Py23FixTestCase):
    def setUp(self):
        self.cols = _random_integer()
        self.rows = _random_integer()
        self.sections = _random_integer()

    def test_default(self):
        """Test default settings"""
        vi = adapter.SFFVolumeIndex(cols=self.cols, rows=self.rows, sections=self.sections)
        self.assertRegex(_str(vi), r"SFFVolumeIndex\(cols.*rows.*sections.*\)")
        self.assertEqual(vi.cols, self.cols)
        self.assertEqual(vi.rows, self.rows)
        self.assertEqual(vi.sections, self.sections)

    def test_create_from_gds_type(self):
        """Test that we can create from a gds_type"""
        _vi = emdb_sff.volume_index_type(cols=self.cols, rows=self.rows, sections=self.sections)
        vi = adapter.SFFVolumeIndex.from_gds_type(_vi)
        self.assertRegex(_str(vi), r"SFFVolumeIndex\(cols.*rows.*sections.*\)")
        self.assertEqual(vi.cols, self.cols)
        self.assertEqual(vi.rows, self.rows)
        self.assertEqual(vi.sections, self.sections)


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
        self.l_unicode = self.l_bytes.decode(u'utf-8')

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
        self.assertEqual(
            _str(l),
            u"""SFFLattice(mode="{}", endianness="{}", size={}, start={}, data="{}")""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                _decode(l.data[:100] + b"...", u"utf-8")
            )
        )

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
        self.assertEqual(
            _str(l),
            u"""SFFLattice(mode="{}", endianness="{}", size={}, start={}, data="{}")""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                _decode(l.data[:100] + b"...", u"utf-8"),
            )
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
        self.assertEqual(
            _str(l),
            u"""SFFLattice(mode="{}", endianness="{}", size={}, start={}, data="{}")""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                _decode(l.data[:100] + b"...", u"utf-8")
            )
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
        self.assertEqual(l.data, adapter.SFFLattice._encode(self.l_data, mode=self.l_mode, endianness=self.l_endian))
        self.assertEqual(l.data_array.flatten().tolist(), self.l_data.flatten().tolist())
        self.assertEqual(
            _str(l),
            u"""SFFLattice(mode="{}", endianness="{}", size={}, start={}, data="{}")""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                _decode(l.data[:100] + b"...", u"utf-8"),
            )
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
        self.assertEqual(
            _str(l),
            u"""SFFLattice(mode="{}", endianness="{}", size={}, start={}, data="{}")""".format(
                self.l_mode,
                self.l_endian,
                _str(self.l_size),
                _str(self.l_start),
                _decode(l.data[:100] + b"...", u"utf-8")
            )
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


class TestSFFVertices(Py23FixTestCase):
    """SFFVertices tests"""

    def setUp(self):
        self.num_vertices = _random_integer(start=2, stop=10)
        self.mode = u'float64'
        self.endian = u'little'
        self.data = numpy.random.rand(self.num_vertices, 3)
        self.bytes = adapter.SFFVertices._encode(self.data, mode=self.mode, endianness=self.endian)
        self.unicode = self.bytes.decode(u'utf-8')

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
        self.assertIsInstance(v.data, _bytes)
        self.assertEqual(v.data, adapter.SFFVertices._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        self.assertEqual(
            _str(v),
            u"""SFFVertices(num_vertices={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_vertices,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8")
            )
        )
        _print(v)
        v.export(sys.stderr)
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
        self.assertEqual(
            _str(v),
            u"""SFFVertices(num_vertices={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_vertices,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8")
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
        self.assertEqual(
            _str(v),
            u"""SFFVertices(num_vertices={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_vertices,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8")
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
        self.assertEqual(
            _str(v),
            u"""SFFVertices(num_vertices={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_vertices,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8"),
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
        self.assertEqual(
            _str(v),
            u"""SFFVertices(num_vertices={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_vertices,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8")
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

class TestSFFNormals(Py23FixTestCase):
    """SFFNormals tests"""

    def setUp(self):
        self.num_normals = _random_integer(start=2, stop=10)
        self.mode = u'float64'
        self.endian = u'little'
        self.data = numpy.random.rand(self.num_normals, 3)
        self.bytes = adapter.SFFNormals._encode(self.data, mode=self.mode, endianness=self.endian)
        self.unicode = self.bytes.decode(u'utf-8')

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
        self.assertIsInstance(v.data, _bytes)
        self.assertEqual(v.data, adapter.SFFNormals._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        self.assertEqual(
            _str(v),
            u"""SFFNormals(num_normals={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_normals,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8")
            )
        )
        _print(v)
        v.export(sys.stderr)
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
        self.assertEqual(
            _str(v),
            u"""SFFNormals(num_normals={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_normals,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8")
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
        self.assertEqual(
            _str(v),
            u"""SFFNormals(num_normals={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_normals,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8")
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
        self.assertEqual(
            _str(v),
            u"""SFFNormals(num_normals={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_normals,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8"),
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
        self.assertEqual(
            _str(v),
            u"""SFFNormals(num_normals={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_normals,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8")
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


class TestSFFTriangles(Py23FixTestCase):
    """SFFTriangles tests"""

    def setUp(self):
        self.num_triangles = _random_integer(start=2, stop=10)
        self.mode = u'uint32'
        self.endian = u'little'
        self.data = numpy.random.randint(0, 100, size=(self.num_triangles, 3))
        self.bytes = adapter.SFFTriangles._encode(self.data, mode=self.mode, endianness=self.endian)
        self.unicode = self.bytes.decode(u'utf-8')

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
        self.assertIsInstance(v.data, _bytes)
        self.assertEqual(v.data, adapter.SFFTriangles._encode(self.data, mode=self.mode, endianness=self.endian))
        self.assertEqual(v.data_array.flatten().tolist(), self.data.flatten().tolist())
        self.assertEqual(
            _str(v),
            u"""SFFTriangles(num_triangles={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_triangles,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8")
            )
        )
        _print(v)
        v.export(sys.stderr)
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
        self.assertEqual(
            _str(v),
            u"""SFFTriangles(num_triangles={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_triangles,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8")
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
        self.assertEqual(
            _str(v),
            u"""SFFTriangles(num_triangles={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_triangles,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8")
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
        self.assertEqual(
            _str(v),
            u"""SFFTriangles(num_triangles={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_triangles,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8"),
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
        self.assertEqual(
            _str(v),
            u"""SFFTriangles(num_triangles={}, mode="{}", endianness="{}", data="{}")""".format(
                self.num_triangles,
                self.mode,
                self.endian,
                _decode(v.data[:100] + b"...", u"utf-8")
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
        _print(v[index])
        self.assertTrue(numpy.array_equal(self.data[index], v[index]))


class TestSFFMesh(Py23FixTestCase):
    """Test the SFFMesh class"""

    def test_default(self):
        """Test default operation"""
        m = adapter.SFFMesh(
            vertices=[(0.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.5, 1.0, 0.0)],  # list of float 3-tuples
            triangles=[(0, 1, 2)]  # list of int 3-tuples
        )
        _print(m.vertices)
        _print(m.triangles)
        # m.export(sys.stderr)


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

    # def test_as_json(self):
    #     """Test export to JSON"""
    #     #full
    #     x0, x1, y0, y1, z0, z1 = _random_integers(count=6)
    #     bb = adapter.SFFBoundingBox(
    #         xmin=x0, xmax=x1,
    #         ymin=y0, ymax=y1,
    #         zmin=z0, zmax=z1
    #     )
    #     _print(bb)
    #     bb_json = bb.as_json()
    #     _print(bb_json)
    #     self.assertEqual(bb.xmin, bb_json[u'xmin'])
    #     self.assertEqual(bb.xmax, bb_json[u'xmax'])
    #     self.assertEqual(bb.ymin, bb_json[u'ymin'])
    #     self.assertEqual(bb.ymax, bb_json[u'ymax'])
    #     self.assertEqual(bb.zmin, bb_json[u'zmin'])
    #     self.assertEqual(bb.zmax, bb_json[u'zmax'])
    #     # empty
    #     bb = adapter.SFFBoundingBox()
    #     bb_json = bb.as_json()
    #     self.assertEqual(bb.xmin, bb_json[u'xmin'])
    #     self.assertIsNone(bb.xmax)
    #     self.assertEqual(bb.ymin, bb_json[u'ymin'])
    #     self.assertIsNone(bb.ymax)
    #     self.assertEqual(bb.zmin, bb_json[u'zmin'])
    #     self.assertIsNone(bb.zmax)
    #
    # def test_from_json(self):
    #     """Test import from JSON"""
    #     #full
    #     bb_json = {'xmin': 640.0, 'xmax': 348.0, 'ymin': 401.0, 'ymax': 176.0, 'zmin': 491.0, 'zmax': 349.0}
    #     bb = adapter.SFFBoundingBox.from_json(bb_json)
    #     self.assertEqual(bb.xmin, bb_json[u'xmin'])
    #     self.assertEqual(bb.xmax, bb_json[u'xmax'])
    #     self.assertEqual(bb.ymin, bb_json[u'ymin'])
    #     self.assertEqual(bb.ymax, bb_json[u'ymax'])
    #     self.assertEqual(bb.zmin, bb_json[u'zmin'])
    #     self.assertEqual(bb.zmax, bb_json[u'zmax'])
    #     # empty
    #     bb_json = {}
    #     bb = adapter.SFFBoundingBox.from_json(bb_json)
    #     self.assertEqual(bb.xmin, 0)
    #     self.assertIsNone(bb.xmax)
    #     self.assertEqual(bb.ymin, 0)
    #     self.assertIsNone(bb.ymax)
    #     self.assertEqual(bb.zmin, 0)
    #     self.assertIsNone(bb.zmax)


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
            r"""SFFCone\(id={}, height={}, bottom_radius={}, transform_id={}\)""".format(
                0, None, None, None
            )
        )
        _height, _bottom_radius, _transform_id = _random_float(10), _random_float(10), _random_integer(start=0)
        C = adapter.SFFCone(
            height=_height, bottom_radius=_bottom_radius, transform_id=_transform_id
        )
        self.assertRegex(
            _str(C),
            r"""SFFCone\(id={}, height={}, bottom_radius={}, transform_id={}\)""".format(
                1, _height, _bottom_radius, _transform_id
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
            r"""SFFCone\(id={}, height={}, bottom_radius={}, transform_id={}\)""".format(
                None, None, None, None
            )
        )
        _height, _bottom_radius, _transform_id = _random_float(10), _random_float(10), _random_integer(start=0)
        _C = emdb_sff.cone(
            height=_height, bottom_radius=_bottom_radius, transform_id=_transform_id
        )
        C = adapter.SFFCone.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCone\(id={}, height={}, bottom_radius={}, transform_id={}\)""".format(
                None, _height, _bottom_radius, _transform_id
            )
        )
        self.assertIsNone(C.id)
        self.assertEqual(C.height, _height)
        self.assertEqual(C.bottom_radius, _bottom_radius)


class TestSFFCuboid(Py23FixTestCase):
    """Test the SFFCuboid class"""

    def tearDown(self):
        adapter.SFFShape.reset_id()

    def test_default(self):
        """Test default settings"""
        C = adapter.SFFCuboid()
        self.assertRegex(
            _str(C),
            r"""SFFCuboid\(id={}, x={}, y={}, z={}, transform_id={}\)""".format(
                0, None, None, None, None
            )
        )
        _x, _y, _z, _transform_id = _random_float(10), _random_float(10), _random_float(10), _random_integer()
        C = adapter.SFFCuboid(x=_x, y=_y, z=_z, transform_id=_transform_id)
        self.assertRegex(
            _str(C),
            r"""SFFCuboid\(id={}, x={}, y={}, z={}, transform_id={}\)""".format(
                1, _x, _y, _z, _transform_id
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
            r"""SFFCuboid\(id={}, x={}, y={}, z={}, transform_id={}\)""".format(
                None, None, None, None, None
            )
        )
        _x, _y, _z, _transform_id = _random_float(10), _random_float(10), _random_float(10), _random_integer()
        _C = emdb_sff.cuboid(x=_x, y=_y, z=_z, transform_id=_transform_id)
        C = adapter.SFFCuboid.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCuboid\(id={}, x={}, y={}, z={}, transform_id={}\)""".format(
                None, _x, _y, _z, _transform_id
            )
        )
        self.assertEqual(C.x, _x)
        self.assertEqual(C.y, _y)
        self.assertEqual(C.z, _z)


class TestSFFCylinder(Py23FixTestCase):
    """Test the SFFCylinder class"""

    def tearDown(self):
        adapter.SFFShape.reset_id()

    def test_default(self):
        """Test default settings"""
        C = adapter.SFFCylinder()
        self.assertRegex(
            _str(C),
            r"""SFFCylinder\(id={}, height={}, diameter={}, transform_id={}\)""".format(
                0, None, None, None
            )
        )
        _height, _diameter, _transform_id = _random_float(10), _random_float(10), _random_integer()
        C = adapter.SFFCylinder(
            height=_height, diameter=_diameter, transform_id=_transform_id
        )
        self.assertRegex(
            _str(C),
            r"""SFFCylinder\(id={}, height={}, diameter={}, transform_id={}\)""".format(
                1, _height, _diameter, _transform_id
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
            r"""SFFCylinder\(id={}, height={}, diameter={}, transform_id={}\)""".format(
                None, None, None, None
            )
        )
        _height, _diameter, _transform_id = _random_float(10), _random_float(10), _random_integer(start=0)
        _C = emdb_sff.cylinder(
            height=_height, diameter=_diameter, transform_id=_transform_id
        )
        C = adapter.SFFCylinder.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFCylinder\(id={}, height={}, diameter={}, transform_id={}\)""".format(
                None, _height, _diameter, _transform_id
            )
        )
        self.assertIsNone(C.id)
        self.assertEqual(C.height, _height)
        self.assertEqual(C.diameter, _diameter)


class TestSFFEllipsoid(Py23FixTestCase):
    """Test the SFFEllipsoid class"""

    def tearDown(self):
        adapter.SFFShape.reset_id()

    def test_default(self):
        """Test default settings"""
        E = adapter.SFFEllipsoid()
        self.assertRegex(
            _str(E),
            r"""SFFEllipsoid\(id={}, x={}, y={}, z={}, transform_id={}\)""".format(
                0, None, None, None, None
            )
        )
        _x, _y, _z, _transform_id = _random_float(10), _random_float(10), _random_float(10), _random_integer()
        E = adapter.SFFEllipsoid(x=_x, y=_y, z=_z, transform_id=_transform_id)
        self.assertRegex(
            _str(E),
            r"""SFFEllipsoid\(id={}, x={}, y={}, z={}, transform_id={}\)""".format(
                1, _x, _y, _z, _transform_id
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
            r"""SFFEllipsoid\(id={}, x={}, y={}, z={}, transform_id={}\)""".format(
                None, None, None, None, None
            )
        )
        _x, _y, _z, _transform_id = _random_float(10), _random_float(10), _random_float(10), _random_integer()
        _C = emdb_sff.ellipsoid(x=_x, y=_y, z=_z, transform_id=_transform_id)
        C = adapter.SFFEllipsoid.from_gds_type(_C)
        self.assertRegex(
            _str(C),
            r"""SFFEllipsoid\(id={}, x={}, y={}, z={}, transform_id={}\)""".format(
                None, _x, _y, _z, _transform_id
            )
        )
        self.assertEqual(C.x, _x)
        self.assertEqual(C.y, _y)
        self.assertEqual(C.z, _z)
