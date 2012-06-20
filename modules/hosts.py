from socket import gethostname

from queues.condorjobanalyzer import CondorJobAnalyzer
from queues.sgejobanalyzer import SGEJobAnalyzer

HOST_DICT = {
    'fnal.gov': CondorJobAnalyzer,
    'hep.ph.ic.ac.uk': SGEJobAnalyzer,
# used for local testing
    #'kinitos' : CondorJobAnalyzer,
}

def get_host_analyzer():
    hostname = gethostname()
    lst = filter(lambda host: hostname.endswith(host), HOST_DICT.keys())
    assert len(lst) == 1, "Cannot determine unique host"
    return HOST_DICT[lst[0]]
