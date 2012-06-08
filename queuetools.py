from commands import getoutput
from collections import defaultdict

class QueueJobAnalyzer(object):
    def __init__(self):
        self.pl = 35
        self.output_format = "{u:<8} {r:>8} {q:>8} {o:>8}"

    def get_user_job_string(self, user):
        return getoutput(self.cmd_string.format(u=user))

    def user_job_postprocess(self, user):
        return None, None, None

    def get_user_job_counts(self,user):
        status_output = self.get_user_job_string(user)
        return self.user_job_postprocess(status_output)

    def print_user_job_count(self, user, title=False):
        banner = "="*35
        if title :
            print banner
        running, queued, other = self.get_user_job_counts(user)
        print self.output_format.format(u=user, r=running, q=queued, o=other)
        if title :
            print banner


class SGEJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(SGEJobAnalyzer,self).__init__()
        self.cmd_string = "qstat -u {u}"
        self.status_start = 40
        self.status_end = 42

    def user_job_postprocess(self, output):
        statuses = defaultdict(int)
        for line in output.split('\n')[2:] :
            key = line[self.status_start:self.status_end+1].strip()
            if key not in ['r', 'qw'] :
                key = 'o'
            statuses[key] += 1
        return statuses['r'], statuses['qw'], statuses['o']


class CondorJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(CondorJobAnalyzer,self).__init__()
        self.cmd_string = "condor_status -submitter | grep ' {u}'"

    def user_job_postprocess(self, output):
        return output.split()[1:]


if __name__=="__main__":
    test_analyzer = SGEJobAnalyzer()
    test_analyzer.print_user_job_count("sr505", title=True)
