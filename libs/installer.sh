#!/bin/bash
sudo cp ev3.py /usr/lib/python2.7
sudo cp wiiMote.py /usr/lib/python2.7
echo libs imported
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python-cwiid
echo Finished!!