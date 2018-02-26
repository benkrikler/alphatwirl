##__________________________________________________________________||
class ComponentLoop(object):

    def __init__(self, nanoaod_results, reader):
        self.reader = reader
        self.nanoaod_results = nanoaod_results

    def __call__(self):
        self.reader.begin()
        for component in self.nanoaod_results.components():
            self.reader.read(component)
        return self.reader.end()

##__________________________________________________________________||
