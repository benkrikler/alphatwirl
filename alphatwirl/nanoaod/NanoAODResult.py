##__________________________________________________________________||
import os
import re
import numpy as np

from Component import Component

##__________________________________________________________________||
class NanoAODResult(object):
    """A NanoAOD result

    Args:
        component_df (pd.DataFrame): the dataframe of components on each row
    """

    def __init__(self, component_df):
        # Name for the progress bar
        component_df["name"] = component_df[["dataset","era"]].apply("_".join,
                                                                     axis=1)
        self.components_df = component_df

    def components(self):
        comps = []
        for row in self.components_df.itertuples():
            comp_dict = dict(
                name      = row.name,
                eventtype = row.eventtype,
                dataset   = row.dataset,
                era       = row.era,
                nevents   = row.nevents,
                nfiles    = row.nfiles,
                files     = row.files,
            )

            # MC related information. Just XS for now
            try:
                comp_dict["cross_section"] = row.cross_section
            except AttributeError:
                comp_dict["cross_section"] = np.nan

            # Add the component information as a named tuple to a list
            comps.append(Component(**comp_dict))
        return comps

##__________________________________________________________________||
