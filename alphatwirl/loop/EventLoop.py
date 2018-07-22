# Tai Sakuma <tai.sakuma@gmail.com>
import uuid

import alphatwirl
from alphatwirl.misc.deprecation import _renamed_class_method_option

##__________________________________________________________________||
class EventLoop(object):
    """An event loop

    Args:
        build_events: A picklable function to create events.
        reader: An event reader. This must be picklable before
            `begin()` is called and after `end` is called.
        progressbar_label (optional): a label shown by the progress
            bar

    """
    def __init__(self, build_events, reader, name=None):
        self.build_events = build_events
        self.reader = reader

        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name

        # assign a random unique id to be used by progress bar
        self.taskid = uuid.uuid4()

    def __repr__(self):
        name_value_pairs = (
            ('build_events', self.build_events),
            ('reader',       self.reader),
            ('name',         self.name),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self):
        events = self.build_events()
        self.nevents = len(events)
        self._report_progress(0)
        self.reader.begin(events)
        for i, event in enumerate(events):
            self._report_progress(i+1)
            self.reader.event(event)
        self.reader.end()
        return self.reader

    def _report_progress(self, i):
        try:
            report = alphatwirl.progressbar.ProgressReport(
                name=self.progressbar_label, done=(i),
                total=self.nevents, taskid=self.taskid
            )
            alphatwirl.progressbar.report_progress(report)
        except:
            pass

##__________________________________________________________________||
