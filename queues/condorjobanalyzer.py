from queuejobanalyzer import QueueJobAnalyzer
from collections import defaultdict
from getpass import getuser
from commands import getoutput

class CondorJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(CondorJobAnalyzer,self).__init__()
        self.queues = ['Condor']
        self.user_job_command = 'condor_status -submitter | grep " {u}"'.format(u=getuser())
        self.queue_status_command = 'condor_status -submitter'

    def _get_avail(self):
        output = getoutput('condor_status -avail')
        summary_line = output.split('\n')[-1]
        avail = int(summary_line.split()[1])
        return avail

    def _user_job_postprocess(self, output):
        print output
        return output.split()[1:]

    def _queue_status_postprocess(self, output):
        # title, running, idle, held
        summary_line = output.split('\n')[-1]
        statuses = defaultdict(dict)
        avail = self._get_avail()
        cores = [int(c) for c in summary_line.split()[1:]]

        # need to use condor_status -format "%s" something
        statuses[self.queues[0]]['r'] = cores[0]
        statuses[self.queues[0]]['a'] = avail
        statuses[self.queues[0]]['t'] = avail + cores[0]
        return statuses
