#! /usr/bin/env python
import sys

from queues.sgejobanalyzer import SGEJobAnalyzer
from queues.condorjobanalyzer import CondorJobAnalyzer

import modules.summary as summary
from modules.hosts import get_host_analyzer


def full_summary():
    HostQAnalyzer = get_host_analyzer()
    QAnalyzer = HostQAnalyzer()
    summary.per_queue(QAnalyzer)
    summary.per_user(QAnalyzer, title=True)

if __name__=="__main__":
    full_summary()
