#!/usr/bin/bash
# TODO: I'm sure this file could be better, do not write shell scripts regularly for sure.

# This is a self-executing script.
# It is downloaded and excuted with one command via SSH.
echo 'Installing Workbench API'
cd /data;

# Uninstall existing Workbench
# TODO: This may change soon if we begin maintaining isolated releases for existing client installs...
echo 'Uninstalling any existing Workbench related directories...'
rm -rf ./workbench/;
echo 'Uninstall complete.'

echo 'Cloning the Workbench API...'
# TODO: Probably should be versioned with a tag and pull the tag for its own build.
git clone https://github.com/openpilot-community/workbench-api.git ./workbench
pip install python-socketio eventlet --target=./vendor
echo 'Cloning complete.'

echo 'Setting permissions for files.'
chmod +x /data/workbench/launch.sh
chmod +x /data/workbench/workbenchd.py
echo 'Setting permissions complete.'

echo 'Killing any existing TMUX Session for Workbench API'
tmux kill-session -t "workbench" || echo "ATTENTION: Existing TMUX Session did not already exist. But this is normal..."

echo 'Launching Workbench API in a new TMUX Session'
tmux new-session -d -s "workbench" /data/workbench/launch.sh

echo 'Workbench API install complete.'