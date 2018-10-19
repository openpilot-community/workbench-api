#!/usr/bin/bash
function launch {

  export PYTHONPATH="/data/openpilot"

  # start manager
  cd /data/workbench
  python ./workbenchd.py

  # if broken, keep on screen error
  while true; do sleep 1; done
}

launch
