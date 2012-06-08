
class QueueJobAnalyzer(object):
    def __init__():
        self.output_format = "{r:>8} {q:>8} {o:>8}"
        self.user_job_command = None
        self.user_job_postprocess = None

    def get_user_job_counts(self,user):
        status_output = self.user_job_command(user)
        return self.user_job_postprocess(status_output)

    def print_user_job_count(self, user):
        running, queued, other = self.get_user_job_counts(user)
        print "="*26
        print self.output_format(r=running, q=queued, o=other)
        print "="*26


class SGEJobAnalyzer(QueueJobAnalyzer):
    def __init__():
        super(SGEJobAnalyser,self).__init__()
        self.user_job_command = "qstat -u {user}"
        self.user_job_postprocess = self.combine

    def combine(output):
        return 0, 0, 0

class CondorJobAnalyzer(QueueJobAnalyzer):
    def __init__():
        super(CondorJobAnalyser,self).__init__()
        self.user_job_command = "condor_status -submitter | grep ' {user}'"
        self.user_job_postprocess = self.separate

    def separate(output):
        return output.split()[1:]
