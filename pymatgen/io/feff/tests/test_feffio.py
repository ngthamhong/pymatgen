# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

from __future__ import unicode_literals

import unittest
import os

from pymatgen.io.feff import Header, FeffTags, FeffLdos, FeffPot, Xmu, \
    FeffAtoms

test_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..",
                        'test_files')

class  HeaderTest(unittest.TestCase):

    header_string = """* This FEFF.inp file generated by pymatgen
TITLE comment: From cif file
TITLE Source:  CoO19128.cif
TITLE Structure Summary:  Co2 O2
TITLE Reduced formula:  CoO
TITLE space group: (Cmc2_1), space number:  (36)
TITLE abc:  3.297078   3.297078   5.254213
TITLE angles: 90.000000  90.000000 120.000000
TITLE sites: 4
* 1 Co     0.666666     0.333332     0.496324
* 2 Co     0.333333     0.666667     0.996324
* 3 O     0.666666     0.333332     0.878676
* 4 O     0.333333     0.666667     0.378675"""

    def test_init(self):
        filepath = os.path.join(test_dir, 'HEADER')
        header = Header.header_string_from_file(filepath)
        h = header.splitlines()
        hs = HeaderTest.header_string.splitlines()
        for i, line in enumerate(h):
            self.assertEqual(line, hs[i])
        self.assertEqual(HeaderTest.header_string.splitlines(),
                         header.splitlines(), "Failed to read HEADER file")

    def test_from_string(self):
        header = Header.from_string(HeaderTest.header_string)
        self.assertEqual(header.struct.composition.reduced_formula, "CoO",
                         "Failed to generate structure from HEADER string")

    def test_get_string(self):
        cif_file = os.path.join(test_dir, 'CoO19128.cif')
        h = Header.from_cif_file(cif_file)
        head = str(h)
        self.assertEqual(head.splitlines()[3].split()[-1],
                         HeaderTest.header_string.splitlines()[3].split()[-1],
                         "Failed to generate HEADER from structure")

    def test_as_dict_and_from_dict(self):
        file_name = os.path.join(test_dir, 'HEADER')
        header = Header.from_file(file_name)
        d = header.as_dict()
        header2 = Header.from_dict(d)
        self.assertEqual(str(header), str(header2),
                         "Header failed to and from dict test")

class FeffAtomsTest(unittest.TestCase):

    def test_init(self):
        filepath = os.path.join(test_dir, 'ATOMS')
        atoms = FeffAtoms.atoms_string_from_file(filepath)
        self.assertEqual(atoms.splitlines()[3].split()[4], 'O',
                         "failed to read ATOMS file")

    def test_get_string(self):
        header = Header.from_string(HeaderTest.header_string)
        struc = header.struct
        central_atom = 'O'
        a = FeffAtoms(struc, central_atom)
        atoms = a.get_string()
        self.assertEqual(atoms.splitlines()[3].split()[4], central_atom,
                         "failed to create ATOMS string")

    def test_as_dict_and_from_dict(self):
        file_name = os.path.join(test_dir, 'HEADER')
        header = Header.from_file(file_name)
        struct = header.struct
        atoms = FeffAtoms(struct, 'O')
        d = atoms.as_dict()
        atoms2 = FeffAtoms.from_dict(d)
        self.assertEqual(str(atoms), str(atoms2),
                         "FeffAtoms failed to and from dict test")

class  FeffTagsTest(unittest.TestCase):

    def test_init(self):
        filepath = os.path.join(test_dir, 'PARAMETERS')
        parameters = FeffTags.from_file(filepath)
        parameters["RPATH"] = 10
        self.assertEqual(parameters["COREHOLE"], "Fsr",
                         "Failed to read PARAMETERS file")
        self.assertEqual(parameters["LDOS"], [-30., 15., .1],
                         "Failed to read PARAMETERS file")

    def test_diff(self):
        filepath1 = os.path.join(test_dir, 'PARAMETERS')
        parameters1 = FeffTags.from_file(filepath1)
        filepath2 = os.path.join(test_dir, 'PARAMETERS.2')
        parameters2 = FeffTags.from_file(filepath2)
        self.assertEqual(FeffTags(parameters1).diff(parameters2),
                         {'Different': {},
                          'Same': {'CONTROL': [1, 1, 1, 1, 1, 1],
                                   'MPSE': [2],
                                   'OPCONS': '',
                                   'SCF': [6.0, 0, 30, .2, 1],
                                   'EXCHANGE': [0, 0.0, 0.0, 2],
                                   'S02': [0.0],
                                   'COREHOLE': 'Fsr',
                                   'FMS': [8.5, 0],
                                   'XANES': [3.7, 0.04, 0.1],
                                   'EDGE': 'K',
                                   'PRINT': [1, 0, 0, 0, 0, 0],
                                   'LDOS': [-30., 15., .1]}})

    def test_as_dict_and_from_dict(self):
        file_name = os.path.join(test_dir, 'PARAMETERS')
        tags = FeffTags.from_file(file_name)
        d=tags.as_dict()
        tags2 = FeffTags.from_dict(d)
        self.assertEqual(tags, tags2,
                         "Parameters do not match to and from dict")

class  FeffPotTest(unittest.TestCase):

    def test_init(self):
        filepath = os.path.join(test_dir, 'POTENTIALS')
        feffpot = FeffPot.pot_string_from_file(filepath)
        d, dr = FeffPot.pot_dict_from_string(feffpot)
        self.assertEqual(d['Co'], 1, "Wrong symbols read in for FeffPot")

    def test_as_dict_and_from_dict(self):
        file_name = os.path.join(test_dir, 'HEADER')
        header = Header.from_file(file_name)
        struct = header.struct
        pot = FeffPot(struct, 'O')
        d=pot.as_dict()
        pot2 = FeffPot.from_dict(d)
        self.assertEqual(str(pot), str(pot2),
                         "FeffPot to and from dict does not match")

class FeffLdosTest(unittest.TestCase):

    filepath1 = os.path.join(test_dir, 'feff.inp')
    filepath2 = os.path.join(test_dir, 'ldos')
    l = FeffLdos.from_file(filepath1, filepath2)

    def test_init(self):
        efermi = FeffLdosTest.l.complete_dos.efermi
        self.assertEqual(efermi, -11.430,
                         "Did not read correct Fermi energy from ldos file")

    def test_complete_dos(self):
        complete_dos = FeffLdosTest.l.complete_dos
        self.assertEqual(complete_dos.as_dict()['spd_dos']['S']['efermi'],
                         - 11.430,
                         "Failed to construct complete_dos dict properly")

    def test_as_dict_and_from_dict(self):
        l2 = FeffLdosTest.l.charge_transfer_to_string()
        d = FeffLdosTest.l.as_dict()
        l3 = FeffLdos.from_dict(d).charge_transfer_to_string()
        self.assertEqual(l2, l3,
                         "Feffldos to and from dict does not match")

class XmuTest(unittest.TestCase):

    def test_init(self):
        filepath1 = os.path.join(test_dir, 'xmu.dat')
        filepath2 = os.path.join(test_dir, 'feff.inp')
        x = Xmu.from_file(filepath1, filepath2)
        self.assertEqual(x.absorbing_atom, 'O',
                         "failed to read xmu.dat file properly")

    def test_as_dict_and_from_dict(self):
        filepath1 = os.path.join(test_dir, 'xmu.dat')
        filepath2 = os.path.join(test_dir, 'feff.inp')
        x = Xmu.from_file(filepath1, filepath2)
        data=x.data.tolist()
        d=x.as_dict()
        x2 = Xmu.from_dict(d)
        data2= x2.data.tolist()
        self.assertEqual(data, data2,
                         "Xmu to and from dict does not match")

if __name__ == '__main__':
    unittest.main()
