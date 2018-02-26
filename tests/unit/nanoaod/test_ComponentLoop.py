import unittest
import numpy as np

from alphatwirl.nanoaod import ComponentLoop
from alphatwirl.nanoaod import Component

##__________________________________________________________________||
class MockReader:
    def __init__(self):
        self.beginCalled = False
        self.readComponents = [ ]
        self.endCalled = False

    def begin(self):
        self.beginCalled = True

    def read(self, component):
        self.readComponents.append(component)

    def end(self):
        self.endCalled = True
        return 2232

##__________________________________________________________________||
class MockNanoAODResult:
    def __init__(self, components):
        self._components = components

    def components(self):
        return self._components

##__________________________________________________________________||
class TestComponentLoop(unittest.TestCase):

    def test_read(self):
        reader = MockReader()

        self.assertFalse(reader.beginCalled)
        self.assertEqual([ ], reader.readComponents)
        self.assertFalse(reader.endCalled)

        component1 = Component(**dict(
            name = "Comp1_Data_2018",
            eventtype = "Data",
            dataset = "Comp1_Data",
            era = "2018",
            nevents = 1234,
            nfiles = 2,
            files = ["comp1_mock_file1.root", "comp1_mock_file2.root"],
            cross_section = np.nan,
        ))
        component2 = Component(**dict(
            name = "Comp2_MC_2017",
            eventtype = "MC",
            dataset = "Comp2_MC",
            era = "2017",
            nevents = 4321,
            nfiles = 1,
            files = ["comp2_mock_file1.root"],
            cross_section = 1.4e-2,
        ))
        components = [component1, component2]
        nanoaod_result = MockNanoAODResult(components)

        componentLoop = ComponentLoop(nanoaod_result, reader)

        self.assertEqual(2232, componentLoop())

        self.assertTrue(reader.beginCalled)
        self.assertEqual(components, reader.readComponents)
        self.assertTrue(reader.endCalled)

##__________________________________________________________________||
