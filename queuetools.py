from commands import getoutput

def separate(output):
    return output.split()[1:]

def combine(output):
    return 0, 0, 0

class QueueJobAnalyzer(object):
    def __init__(self):
        self.pl = 35
        self.output_format = "{u:<8} {r:>8} {q:>8} {o:>8}"
        self.user_job_command = None
        self.user_job_postprocess = None

    def get_user_job_counts(self,user):
        status_output = getoutput(self.user_job_command.format(user=user))
        return self.user_job_postprocess(status_output)

    def print_user_job_count(self, user):
        running, queued, other = self.get_user_job_counts(user)
        print "="*self.pl
        print self.output_format.format(u=user, r=running, q=queued, o=other)
        print "="*self.pl

class SGEJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(SGEJobAnalyzer,self).__init__()
        self.user_job_command = "qstat -u {user}"
        self.user_job_postprocess = combine

class CondorJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(CondorJobAnalyzer,self).__init__()
        self.user_job_command = "condor_status -submitter | grep ' {user}'"
        self.user_job_postprocess = separate

if __name__=="__main__":
    test_analyzer = SGEJobAnalyzer()
    test_analyzer.print_user_job_count("sr505")
