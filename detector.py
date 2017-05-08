# encoding: utf-8
import relations
import numpy as np
import helper
import os


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
    return matrixs


def get_candidates(matrixs, min_window_size):
    """
    Getting candidates from relation matrix.
    """
    candidates = []
    for _, matrix in matrixs.iteritems():
        for _, stream in matrix.iteritems():
            candidates.extend(partition(stream, min_window_size))
    return candidates


def combine(candidates, radius, bounds, min_window_size, alpha=0.9):
    """
    combine
    """
    clusters = helper.DBSCAN_1d(candidates, radius, 1)
    clusters.sort(key=lambda x: -len(x))

    partitioned = [bounds[0], bounds[-1]]
    for cluster in clusters:
        center = sum(cluster) / len(cluster)

        for i, value in enumerate(partitioned):
            if value == center:
                break
            if value > center:
                if partitioned[i] - partitioned[i - 1] >= 2 * min_window_size:
                    left = center - partitioned[i - 1]
                    right = partitioned[i] - center
                    if min_window_size * alpha <= left <= min_window_size:
                        partitioned.insert(i, partitioned[i - 1] + min_window_size)
                    elif min_window_size * alpha <= right <= min_window_size:
                        partitioned.insert(i, partitioned[i] - min_window_size)
                    elif left >= min_window_size and right >= min_window_size:
                        partitioned.insert(i, center)
    return partitioned


def detect(traces, min_window_size, radius, relation_types):
    """
    detect
    """
    matrixs = transform(traces, relation_types)
    candidates = get_candidates(matrixs, min_window_size)
    change_points = combine(candidates, radius, [0, len(traces)], min_window_size)
    return change_points


def partition(stream, min_window_size):
    """
    Detecting candiate points from stream.
    """
    candidates = set()
    begin = -1
    count = 0

    for index, value in enumerate(stream):
        if begin == -1 or stream[begin] != value:
            if count >= min_window_size:
                candidates.add(begin)
                candidates.add(index)
            begin, count = index, 0
        count += 1
    if count >= min_window_size:
        candidates.add(begin)

    return candidates


def test():
    log_dir = './logs'
    for filename in os.listdir(log_dir):
        path = os.path.join(log_dir, filename)
        if os.path.isfile(path):
            print "log: ", filename
            traces = helper.parse_mxml(path)
            change_points = detect(traces, 100, 10, [relations.DIRECT_SUCCESION])
            print "Change points detected: ", change_points
            print "----------------------------------------------------------------------------------"


def main():
    usage = """\
usage:
    python detector.py [-w value] [-r value] log_file_path
options:
    -w minimum window size, integer, default value is 100
    -r DBSCAN radius, integer, default value is 10
example:
    python detector.py -w 100 -r 10 /tmp/loan.mxml
    python detector.py /tmp/loan.mxml
    """
    import getopt, sys

    try:
        opts, args = getopt.getopt(sys.argv[1:], "w:r:")
        if len(args) == 0:
            print usage
            return

        minimum_window_size = 100
        radius = 10
        for opt, value in opts:
            if opt == '-w':
                minimum_window_size = int(value)
            elif opt == '-r':
                radius = int(value)
        print "------------------------------------------------------------------------------"
        print "Log: ", args[0]
        print "Minimum window size: ", minimum_window_size
        print "DBSCAN radius: ", radius
        print "------------------------------------------------------------------------------"

        traces = helper.parse_mxml(args[0])
        change_points = detect(traces, minimum_window_size, radius, [relations.DIRECT_SUCCESION])
        print "Change points detected: ", change_points
    except getopt.GetoptError:
        print usage
    except SyntaxError as error:
        print error
        print usage


if __name__ == '__main__':
    main()
