# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class ComponentReaderBundle(object):

    def __init__(self):
        self.readers = [ ]

    def addReader(self, reader):
        self.readers.append(reader)

    def begin(self):
        for reader in self.readers:
            reader.begin()

    def read(self, component):
        for reader in self.readers:
            reader.read(component)

    def end(self):
        return [reader.end() for reader in self.readers]

##__________________________________________________________________||
