# process-drift-detection
Detecting process drift from event log.
## Python packages required
- lxml (http://lxml.de/)
- numpy (http://www.numpy.org/)
## How to use
Command line usage:
```
python detector.py [-w value] [-r value] log_file_path
options:
    -w minimum window size, integer, default value is 100
    -r DBSCAN radius, integer, default value is 10
```
Examples:
```
 python detector.py -w 100 -r 10 /tmp/loan.mxml
 python detector.py /tmp/loan.mxml
```