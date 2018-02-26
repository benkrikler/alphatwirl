from .Component import Component
from .ComponentLoop import ComponentLoop
from .ComponentReaderComposite import ComponentReaderComposite
from .NanoAODResult import NanoAODResult

hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from .EventBuilder import EventBuilder
    from .EventBuilderConfig import EventBuilderConfig
    from .EventBuilderConfigMaker import EventBuilderConfigMaker
