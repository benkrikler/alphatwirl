import os


import ROOT
import logging 


from ..roottree import EventBuilderConfig as BaseEventBuilderConfig
from .EventBuilderConfig import EventBuilderConfig as NanoAODEventBuilderConfig


logger = logging.getLogger(__name__)


class EventBuilderConfigMaker(object):
    def __init__(self, treeName):
        self.treeName = treeName

    def create_config_for(self, dataset, files, start, length):
        base_config = BaseEventBuilderConfig(
            inputPaths = files,
            treeName = self.treeName,
            maxEvents = length,
            start = start,
            name = dataset.name, # for the progress report writer
        )
        config = NanoAODEventBuilderConfig(
            base = base_config,
            component = dataset # for scribblers
        )
        return config

    def file_list_in(self, dataset, maxFiles = -1):
        if maxFiles < 0:
            return dataset.files
        return dataset.files[:min(maxFiles, len(dataset.files))]

    def nevents_in_file(self, path):
        file = ROOT.TFile.Open(path)
	if not file or file.IsZombie():
		logger.error("Cannot open file, {}".format(path))
		raise AttributeError
        tree = file.Get(self.treeName)
        return tree.GetEntries() # GetEntries() is slow. call only as
                                 # many times as necessary
