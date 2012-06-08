import re
from collections import defaultdict

from queuejobanalyzer import QueueJobAnalyzer

class SGEJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(SGEJobAnalyzer,self).__init__()
        self.cmd_string = "qstat -u {u}"
        self.status_start = 40
        self.status_end = 42
        self.id_start = 103

    def user_job_postprocess(self, output):
        statuses = defaultdict(int)
        for line in output.split('\n')[2:] :
            weight = 1
            key = line[self.status_start:self.status_end+1].strip()
            if key not in ['r', 'qw'] :
                key = 'o'
            if key != 'r':
                id = line[self.id_start:]
                # check if we are in a parametric job
                if "-" in id and ":" in id :
                    s,e,st = re.split('-|:', id)
                    weight = (int(e)-int(s))/int(st)
            statuses[key] += weight
        return statuses['r'], statuses['qw'], statuses['o']
