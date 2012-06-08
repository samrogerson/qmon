from commands import getoutput

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

    def print_user_job_count(self, user):
        running, queued, other = self.get_user_job_counts(user)
        print self.output_format.format(u=user, r=running, q=queued, o=other)


class SGEJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(SGEJobAnalyzer,self).__init__()
        self.cmd_string = "qstat -u {u}"

    def user_job_postprocess(self, output):
        print output
        return 0, 0, 0


class CondorJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(CondorJobAnalyzer,self).__init__()
        self.cmd_string = "condor_status -submitter | grep ' {u}'"

    def user_job_postprocess(self, output):
        return output.split()[1:]


if __name__=="__main__":
    test_analyzer = SGEJobAnalyzer()
    test_analyzer.print_user_job_count("sr505")
