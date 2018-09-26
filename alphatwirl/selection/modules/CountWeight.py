import copy

##__________________________________________________________________||
N_KEYS = 3
IDX_DEPTH = 0
IDX_PASS = 3
IDX_TOTAL = 4

##__________________________________________________________________||
class Count(object):
    """ Similar to Count.py, but increments by the value in event.w 
    instead of 1.
    """

    def __init__(self, weight_attr="weight"):
        self._results = [ ]
        self._weight = weight_attr
        self._count_const = isinstance(self._weight, (int, float))

    def count(self, pass_, event):
        if self._count_const:
            return self._count_const(pass_, event)

        return self._count_attr(pass_, event)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self._results)

    def copy(self):
        return copy.deepcopy(self)

    def add(self, selection):
        class_name = selection.__class__.__name__
        selection_name = selection.name if hasattr(selection, 'name') and selection.name is not None else ''
        depth = 1
        pass_ = 0
        total = 0
        self._results.append([depth, class_name, selection_name, pass_, total])

    def _count_attr(self, pass_, event):
        for r, p in zip(self._results, pass_):
            r[IDX_TOTAL] += getattr(event, self._weight)[0] # total
            if p: r[IDX_PASS] += getattr(event, self._weight)[0] # pass

    def _count_const(self, pass_, event):
        for r, p in zip(self._results, pass_):
            r[IDX_TOTAL] += self._weight # total
            if p: r[IDX_PASS] += self._weight # pass

    def increment_depth(self, by = 1):
        for r in self._results:
            r[IDX_DEPTH] += by

    def insert(self, i, other):
        self._results[(i + 1):(i + 1)] = other._results

    def results(self):
        return self._results

    def __add__(self, other):
        ret = self.copy()

        if other == 0: # other is 0 when e.g. sum([obj1, obj2])
            return ret

        self._add_results_inplace(ret._results, other._results)
        return ret

    def __iadd__(self, other):
        self._add_results_inplace(self._results, other._results)
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def _add_results_inplace(self, res1, res2):
        if not len(res1) == len(res2):
            import logging
            logging.warning('cannot add because res1 and res2 don\'t have the same length: res1 = {}, res2 = {}'.format(res1, res2))
            return

        if not all([(r1[:N_KEYS] == r2[:N_KEYS]) for r1, r2 in zip(res1, res2)]):
            import logging
            logging.warning('cannot add because res1 and res2 don\'t have the same key columns: res1 = {}, res2 = {}'.format(res1, res2))
            return

        for r1, r2 in zip(res1, res2):
            r1[IDX_PASS] += r2[IDX_PASS]
            r1[IDX_TOTAL] += r2[IDX_TOTAL]

    def to_tuple_list(self):
        return [tuple(e) for e in self._results]

##__________________________________________________________________||
