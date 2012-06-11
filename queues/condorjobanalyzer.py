import re
from queuejobanalyzer import QueueJobAnalyzer
from collections import defaultdict
from getpass import getuser
from commands import getoutput

class CondorJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(CondorJobAnalyzer,self).__init__()
        self.queues = ['Condor']
        self.queue_job_command = 'condor_status -submitter'.format(u=getuser())
        self.queue_status_command = 'condor_status'


    def _queue_status_postprocess(self, output):
        # title, total, idle, held
        summary_line = output.split('\n')[-1]
        statuses = defaultdict(dict)
        cores = [int(c) for c in summary_line.split()[1:]]

        # need to use condor_status -format "%s" something
        statuses[self.queues[0]]['t'] = cores[0]
        statuses[self.queues[0]]['r'] = cores[2]
        statuses[self.queues[0]]['a'] = cores[3]
        return statuses


    def _queue_job_postprocess(self, output):
        user = getuser()
        statuses = {}
        for line in output.split('\n')[3:-2]:
            fields = re.split('@|[ ]+', line.strip())
            if len(fields) != 5 or fields[0] != user:
                continue
            # we're not in a title line
            s = [int(f) for f in fields[2:]]
            status = {'r': s[0], 'qw': s[1], 'o': s[2]}
            statuses[user] = status
        return statuses
