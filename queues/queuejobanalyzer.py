from commands import getoutput

class QueueJobAnalyzer(object):
    def __init__(self):
        pass

    def _get_queue_job_string(self, queue):
        return getoutput(self.queue_job_command.format(q=queue))

    def _queue_job_postprocess(self, output):
        return None, None, None

    def _get_queue_status_string(self):
        return getoutput(self.queue_status_command)

    def _queue_status_postprocess(self, output):
        return None

    # interfaces
    def get_queue_job_counts(self, queues = None):
        if queues == None:
            queues = self.queues
        q_dict = {}
        status_output = ""
        for q in queues :
            status_output = self._get_queue_job_string(q)
            q_dict[q] = self._queue_job_postprocess(status_output)
        return q_dict

    def get_queue_status(self):
        status_output = self._get_queue_status_string()
        return self._queue_status_postprocess(status_output)
