class SliceStore(object):
    def __init__(self, slc=None, mode='loc'):
        self.slc = slc or slice(None) 
        self.mode = mode
    def __getitem__(self, slc):
        self.slc = slc
        return self
    def __setitem__(self, _, __):
        raise Exception("SliceStore cannot be assigned values")
    def __str__(self):
        return "{{.{}[{}]}}".format(self.mode, repr(self.slc))

def _index_slicer_factory(defaultmode):
    class IndexSlicer(SliceStore):
        def __init__(self, slc=None, mode=defaultmode):
            self.slc = slc or slice(None) 
            self.mode = mode
    return IndexSlicer

# ix = _index_slicer_factory('ix')()
iloc = _index_slicer_factory('iloc')()
loc = _index_slicer_factory('loc')()

if __name__ == '__main__':
    print(iloc)
    print(loc)
    iloc[1:10:2]
    print(iloc)
