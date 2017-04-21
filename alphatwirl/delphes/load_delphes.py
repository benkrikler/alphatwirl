# Tai Sakuma <tai.sakuma@cern.ch>
import ROOT

_loaded = False

##__________________________________________________________________||
def load_delphes():

    global _loaded
    if _loaded:
        return

    # https://root.cern.ch/phpBB3/viewtopic.php?t=21603
    ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
    # https://cp3.irmp.ucl.ac.be/projects/delphes/ticket/1039
    ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

    ROOT.gSystem.Load("libDelphes.so")

    _loaded = True

##__________________________________________________________________||
