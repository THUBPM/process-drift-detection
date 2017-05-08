# encoding: utf-8
import numpy as np

def _direct_succesion(trace):
    """
    Extacting direct succesion relations from trace.
    """
    res = {}
    for i in xrange(len(trace) - 1):
        name = '%s->%s' % (trace[i], trace[i + 1])
        res[name] = 1
    return res

def _weak_order(trace):
    """
    Extacting weak order relations from trace.
    """
    res = {}
    for i in xrange(len(trace) - 1):
        for j in xrange(i + 1, len(trace)):
            name = '%s-->%s' % (trace[i], trace[j])
            res[name] = 1
    return res


def transform(traces, types):
    """
    transform traces into relation matrix
    """
    n_traces = len(traces)
    matrixs = {}
    for relation_type in types:
        matrix = {}
        for i, trace in enumerate(traces):
            for key, value in relation_type['extract'](trace).iteritems():
                array = matrix.setdefault(key, np.full(n_traces, relation_type['default'], np.int8))
                array[i] = value
        matrixs[relation_type['name']] = matrix
    return matrix


DIRECT_SUCCESION = {
    'name': 'direct_succesion',
    'extract': _direct_succesion,
    'default': 0,
}

WEAK_ORDER = {
    'name': 'weak order',
    'extract': _weak_order,
    'default': 0,
}


