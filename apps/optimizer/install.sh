#!/bin/bash
echo "Installing Building Rules Optimizer App!"
echo "First of all, removing old installation..."
./uninstall.sh
echo "Now installing it..."
mkdir venv
virtualenv venv
source venv/bin/activate
pip install flask==0.9
mkdir logs
/sbin/ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}' > config/_ip.inf
