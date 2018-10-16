#!/usr/bin/env python
from multiprocessing import Process
import sys
import workbench.monitor as monitor

def start_monitor():
  print '[started] Workbench Monitor'
  monitor.main()
  print '[stopped] Workbench Monitor'

if __name__ == '__main__':
    p1 = Process(target = start_monitor)
    p1.start()