#!/usr/bin/bash
function launch {
  # no cpu rationing for now
  # echo 0-3 > /dev/cpuset/background/cpus
  # echo 0-3 > /dev/cpuset/system-background/cpus
  # echo 0-3 > /dev/cpuset/foreground/boost/cpus
  # echo 0-3 > /dev/cpuset/foreground/cpus
  # echo 0-3 > /dev/cpuset/android/cpus
  export PYTHONPATH="/data/openpilot"

  # start manager
  cd /data/workbench
  python ./workbenchd.py

  # if broken, keep on screen error
  while true; do sleep 1; done
}

launch
