#!/bin/bash
#
# When working with vagrant, sometimes Fusion's vmnet gets a bit hosed up,
# and you just want to reset it. Run this script.
#
sudo /Applications/VMware\ Fusion.app/Contents/Library/vmnet-cli --configure
sudo /Applications/VMware\ Fusion.app/Contents/Library/vmnet-cli --stop
sudo /Applications/VMware\ Fusion.app/Contents/Library/vmnet-cli --start
