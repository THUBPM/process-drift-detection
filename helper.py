from lxml import etree


def DBSCAN_1d(array, radius, min_pts):
    """
    Apply DBSCAN to an array.
    """
    sorted_array = sorted(array)
    len_array = len(sorted_array)

    left_bounds = range(len_array)
    right_bounds = range(len_array)

    for i in xrange(len_array):
        j = right_bounds[i] + 1
        while j < len_array and abs(sorted_array[i] - sorted_array[j]) <= radius:
            if i < left_bounds[j]:
                left_bounds[j] = i
            j += 1
        right_bounds[i] = j - 1

    clusters = []
    begin, end = None, None
    for i in xrange(len_array):
        if end is not None and i > end:
            clusters.append(sorted_array[begin:end + 1])
            begin, end = None, None

        count = right_bounds[i] - left_bounds[i] + 1
        if count >= min_pts:
            if begin is None:
                begin = left_bounds[i]
            end = right_bounds[i]
    if end is not None:
        clusters.append(sorted_array[begin:end + 1])
    return clusters


def _parse_AuditTrailEntry(element):
    """
    - AuditTrailEntry
        - WorkflowModelElement
        - EventType (e.g. assign, complete)
        - Timestamp (e.g. 2005-02-07T15:30:00.000+00:00)
    """
    entry = dict()
    for item in element:
        if item.tag == 'WorkflowModelElement':
            entry['name'] = item.text.strip()
        elif item.tag == 'EventType':
            entry['type'] = item.text.strip()
        elif item.tag == 'Timestamp':
            entry['timestamp'] = item.text.strip()
    return entry


def parse_mxml(filepath):
    """
    - process
        - ProcessInstance(*)
            - AuditTrailEntry(*)
    """
    tree = etree.parse(filepath)
    root = tree.getroot()

    process = root.xpath('./Process')[0]
    traces = []
    instance_id_list = []
    events = set()
    for instance in process:
        trace = []
        for item in instance:
            if item.tag == 'AuditTrailEntry':
                entry = _parse_AuditTrailEntry(item)
                if entry['type'] == 'assign':
                    trace.append(entry['name'])
                    events.add(entry['name'])
                    # print entry['timestamp'],
        # print
        traces.append(trace)
        instance_id_list.append(instance.get('id'))
    return traces


if __name__ == "__main__":
    import numpy as np

    ARRAY = np.random.randint(100, size=20)
    print "dbscan: ", ARRAY
    print "result: ", DBSCAN_1d(ARRAY, 3, 1)
