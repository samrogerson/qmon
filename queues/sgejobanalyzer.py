import re
from collections import defaultdict

from queuejobanalyzer import QueueJobAnalyzer

class SGEJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(SGEJobAnalyzer,self).__init__()
        self.queues = ["hepshort.q", "hepmedium.q", "heplong.q"]
        self.user_job_command = "qstat -u {u}"
        self.queue_status_command = "qstat -f"

        self.pos = {
            "status_start": 40,
            "status_end": 42,
            "id_start": 103,
            "q_status_start": 37,
            "q_status_end": 44,
        }

    def _queue_status_postprocess(self, output):
        lines = filter(lambda s: not s.startswith('-'), output.split('\n')[2:])

        statuses = defaultdict(dict)
        for line in lines:
            queue = line.split('@')[0]
            if queue not in statuses :
                statuses[queue] = defaultdict(int)
            q_status_str = line[self.pos['q_status_start']:self.pos['q_status_end']].strip()
            resv, used, tot = map(int,q_status_str.split('/'))
            statuses[queue]['t'] += tot
            statuses[queue]['r'] += used
            statuses[queue]['a'] += tot - resv - used
        return statuses

    def _user_job_postprocess(self, output):
        statuses = defaultdict(int)
        for line in output.split('\n')[2:]:
            weight = 1
            key = line[self.pos['status_start']:self.pos['status_end']+1].strip()
            if key not in ['r', 'qw']:
                key = 'o'
            if key != 'r':
                id = line[self.pos['id_start']:]
                # check if we are in a parametric job
                if "-" in id and ":" in id:
                    s,e,st = re.split('-|:', id)
                    weight = (int(e)-int(s))/int(st)
            statuses[key] += weight
        return statuses['r'], statuses['qw'], statuses['o']
