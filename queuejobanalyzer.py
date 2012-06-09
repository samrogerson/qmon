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

    def print_user_job_count(self, user, title=False):
        sub_banner= "-"*self.pl
        banner = "="*self.pl
        if title :
            print banner
        running, queued, other = self.get_user_job_counts(user)
        print self.output_format.format(u="", r="Running", q="Queued", o="Other")
        print sub_banner
        print self.output_format.format(u=user, r=running, q=queued, o=other)
        if title :
            print banner
