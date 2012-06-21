#! /usr/bin/env python
import sys

from modules.hosts import get_host_analyzer
from modules.summary import full_summary

if __name__=="__main__":
    HostQAnalyzer = get_host_analyzer()
    QAnalyzer = HostQAnalyzer()
    full_summary(QAnalyzer)
