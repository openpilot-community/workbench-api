#!/usr/bin/bash
# TODO: I'm sure this file could be better, do not write shell scripts regularly for sure.

# This is a self-executing script.
# It is downloaded and excuted with one command via SSH.
echo 'Installing Workbench API'
cd /data;

# Uninstall existing Workbench
# TODO: This may change soon if we begin maintaining isolated releases for existing client installs...
# echo 'Uninstalling any existing Workbench related directories...'
# rm -rf ./workbench/;
# echo 'Uninstall complete.'

echo 'Cloning the Workbench API...'
git clone https://github.com/openpilot-community/workbench-api.git  ./workbench/ 2> /dev/null
echo 'Cloning complete.'

cd workbench;
UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"
    git reset --hard;
    git clean -xdf;
    git pull;
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
else
    echo "Diverged"
    git reset --hard;
    git clean -xdf;
    git pull;
fi



echo 'Setting permissions for files.'
chmod +x /data/workbench/scripts/launch.sh
chmod +x /data/workbench/workbenchd.py
echo 'Setting permissions complete.'

echo 'Killing any existing TMUX Session for Workbench API'
tmux kill-session -t "workbench" || echo "ATTENTION: Existing TMUX Session did not already exist. But this is normal..."

echo 'Launching Workbench API in a new TMUX Session'
tmux new-session -d -s "workbench" /data/workbench/scripts/launch.sh

echo 'Workbench API install complete.'