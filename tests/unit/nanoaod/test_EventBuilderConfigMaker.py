import sys
import unittest

from alphatwirl.roottree import EventBuilderConfig as BaseEventBuilderConfig
from alphatwirl.nanoaod import EventBuilderConfig

##__________________________________________________________________||
hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from alphatwirl.nanoaod import EventBuilderConfigMaker

##__________________________________________________________________||
class MockComponent(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

##__________________________________________________________________||
class MockTObject(object):
    def __init__(self, name):
        self.name = name

    def GetEntries(self):
        return 2500

##__________________________________________________________________||
class MockTFile(object):
    def Open(self, path):
        self.path = path
        return self

    def Get(self, name):
        return MockTObject(name)

##__________________________________________________________________||
class MockROOT(object):
    def __init__(self):
        self.TFile = MockTFile()


##__________________________________________________________________||
@unittest.skipUnless(hasROOT, "has no ROOT")
class TestEventBuilderConfigMaker(unittest.TestCase):

    def setUp(self):
        self.moduleEventBuilderConfigMaker = sys.modules['alphatwirl.nanoaod.EventBuilderConfigMaker']
        self.orgROOT = self.moduleEventBuilderConfigMaker.ROOT
        self.moduleEventBuilderConfigMaker.ROOT = MockROOT()

    def tearDown(self):
        self.moduleEventBuilderConfigMaker.ROOT = self.orgROOT

    def test_create_config_for(self):
        obj = EventBuilderConfigMaker(
            treeName = 'Events'
        )

        component = MockComponent(
            name = "TTJets_2018",
            eventtype = "MC",
            dataset = "TTJets",
            era = "2018",
            nevents = 30,
            nfiles = 2,
            files = ["/nanoaod/dir/TTJets/nano_1.root"],
            cross_section = 1234,
        )

        expected = EventBuilderConfig(
            base = BaseEventBuilderConfig(
                inputPaths = component.files,
                treeName = 'Events',
                maxEvents = component.nevents,
                start = 20,
                name = component.name
                ),
            component = component,
        )

        actual = obj.create_config_for(
            component,
            files = component.files,
            start = 20,
            length = component.nevents,
        )

        self.assertEqual(expected, actual)

    def test_file_list_in(self):
        obj = EventBuilderConfigMaker(
            treeName = 'Events'
        )

        component = MockComponent(
            name = "TTJets_2018",
            eventtype = "MC",
            dataset = "TTJets",
            era = "2018",
            nevents = 30,
            nfiles = 2,
            files = ["/nanoaod/dir/TTJets/nano_1.root"],
            cross_section = 1234,
        )

        expected = ["/nanoaod/dir/TTJets/nano_1.root"]

        actual = obj.file_list_in(component)

        self.assertEqual(expected, actual)

    def test_file_list_in_maxFiles(self):
        obj = EventBuilderConfigMaker(
            treeName = 'Events'
        )

        component = MockComponent(
            name = "TTJets_2018",
            eventtype = "MC",
            dataset = "TTJets",
            era = "2018",
            nevents = 30,
            nfiles = 2,
            files = ["/nanoaod/dir/TTJets/nano_1.root",
                     "/nanoaod/dir/TTJets/nano_2.root"],
            cross_section = 1234,
        )

        expected = [ ]

        actual = obj.file_list_in(component, maxFiles = 0)

        self.assertEqual(expected, actual)

##__________________________________________________________________||
