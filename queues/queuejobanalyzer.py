from commands import getoutput

class QueueJobAnalyzer(object):
    def __init__(self):
        pass

    def _get_user_job_string(self, user):
        return getoutput(self.user_job_command.format(u=user))

    def _user_job_postprocess(self, user):
        return None, None, None

    def _get_queue_status_string(self):
        return getoutput(self.queue_status_command)

    def _queue_status_postprocess(self):
        return None

    # interfaces
    def get_user_job_counts(self,user):
        status_output = self._get_user_job_string(user)
        return self._user_job_postprocess(status_output)

    def get_queue_status(self, queues=None):
        status_output = self._get_queue_status_string()
        return self._queue_status_postprocess(status_output)
