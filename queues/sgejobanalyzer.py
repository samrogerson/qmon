import re
from collections import defaultdict
from collections import OrderedDict

from queuejobanalyzer import QueueJobAnalyzer

class SGEJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(SGEJobAnalyzer,self).__init__()
        self.queues = ['hepshort.q', 'hepmedium.q', 'heplong.q']
        self.queue_job_command = 'qstat -q {q} -u "*"'
        self.queue_status_command = 'qstat -g c'

        self.pos = {
            'user_start': 27,
            'user_end': 39,
            'status_start': 40,
            'status_end': 42,
            'id_start': 103,
        }


    def _queue_status_postprocess(self, output):
        lines = output.split('\n')[2:]

        statuses = OrderedDict()
        for q in self.queues:
            statuses[q] = defaultdict(int)

        for line in lines:
            fields = line.split()
            queue = fields[0]
            used = int(fields[2])
            available = int(fields[4])
            total  = int(fields[5])
            statuses[queue]['t'] += total
            statuses[queue]['r'] += used
            statuses[queue]['a'] += available
        return statuses


    def _queue_job_postprocess(self, output):
        statuses = defaultdict(dict)
        for line in output.split('\n')[2:]:
            user = line[self.pos['user_start']: self.pos['user_end']].strip()
            if user not in statuses:
                statuses[user] = defaultdict(int)
            status = line[self.pos['status_start']:self.pos['status_end']+1].strip()
            weight = 1
            if status not in ['r', 'qw']:
                status = 'o'
            if status != 'r':
                id = line[self.pos['id_start']:]
                # check if we are in a parametric job
                if "-" in id and ":" in id:
                    s,e,st = re.split('-|:', id)
                    weight = (int(e)-int(s))/int(st)
            statuses[user][status] += weight
        return statuses
