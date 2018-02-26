import os
import unittest

import numpy as np
import pandas as pd

from alphatwirl.nanoaod import Component
from alphatwirl.nanoaod import NanoAODResult

##__________________________________________________________________||
class TestNanoAODResult(unittest.TestCase):

    def setUp(self):
        components = pd.DataFrame([dict(
            eventtype = "MC",
            dataset = "TTJets",
            era = "2018",
            nevents = 30,
            nfiles = 2,
            files = ["/nanoaod/dir/TTJets/nano_1.root",
                     "/nanoaod/dir/TTJets/nano_2.root"],
        )])
        self.nanoaod = NanoAODResult(components)

    def test_init(self):
        components = pd.DataFrame([dict(
            name = "TTJets_2018",
            eventtype = "MC",
            dataset = "TTJets",
            era = "2018",
            nevents = 30,
            nfiles = 2,
            files = ["/nanoaod/dir/TTJets/nano_1.root",
                     "/nanoaod/dir/TTJets/nano_2.root"],
        )])
        self.assertEqual(components.name[0], self.nanoaod.components_df.name[0])
        self.assertEqual(components.eventtype[0], self.nanoaod.components_df.eventtype[0])
        self.assertEqual(components.dataset[0], self.nanoaod.components_df.dataset[0])
        self.assertEqual(components.era[0], self.nanoaod.components_df.era[0])
        self.assertEqual(components.nevents[0], self.nanoaod.components_df.nevents[0])
        self.assertEqual(components.nfiles[0], self.nanoaod.components_df.nfiles[0])
        self.assertEqual(components.files[0], self.nanoaod.components_df.files[0])

    def test_components(self):
        expected = [Component(**dict(
            name = "TTJets_2018",
            eventtype = "MC",
            dataset = "TTJets",
            era = "2018",
            nevents = 30,
            nfiles = 2,
            files = ["/nanoaod/dir/TTJets/nano_1.root",
                     "/nanoaod/dir/TTJets/nano_2.root"],
            cross_section = np.nan,
        ))]
        self.assertEqual(expected, self.nanoaod.components())

##__________________________________________________________________||
