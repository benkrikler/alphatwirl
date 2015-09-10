# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class ReaderWithEventSelection(object):

    """An event reader with event selection"

    Call the event reader only with the selected events
    """

    def __init__(self, reader, selection):
        self.reader = reader
        self.selection = selection

    def begin(self, event):
        if hasattr(self.selection, 'begin'): self.selection.begin(event)
        self.reader.begin(event)

    def event(self, event):
        if not self.selection(event): return
        self.reader.event(event)

    def end(self):
        if hasattr(self.selection, 'end'): self.selection.end()
        self.reader.end()

    def copyFrom(self, src):
        self.reader.copyFrom(src.reader)

##__________________________________________________________________||
