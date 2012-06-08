from queuejobanalyzer import QueueJobAnalyzer

class CondorJobAnalyzer(QueueJobAnalyzer):
    def __init__(self):
        super(CondorJobAnalyzer,self).__init__()
        self.cmd_string = "condor_status -submitter | grep ' {u}'"

    def user_job_postprocess(self, output):
        return output.split()[1:]
