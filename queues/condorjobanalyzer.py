from queuejobanalyzer import QueueJobAnalyzer

class CondorJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(CondorJobAnalyzer,self).__init__()
        self.user_job_command = "condor_status -submitter | grep ' {u}'"

    def _user_job_postprocess(self, output):
        return output.split()[1:]
