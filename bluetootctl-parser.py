#!/usr/bin/env python3

# This script parses the output of bluetoothctl to get a list of paired devices
# and their info. It then prints the info in JSON format.
# Usage: python3 bluetoothctl-parser.py
# Note: 'bluetoothctl scan on' must be running first to get a list of devices
# Author: Colin Weaver, ITdojo, Inc.

import subprocess
import json

# Function to run shell commands
def run_shell_cmd(cmd):
    return subprocess.Popen(
        cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
)


# Get list of devices from bluetoothctl
devices = run_shell_cmd("bluetoothctl devices").communicate()[0].decode("utf-8").split("\n")
devices = [x.replace("Device ","") for x in devices]
devices = [x.split(" ") for x in devices]
devices = [{"name":x[1],"mac":x[0]} for x in devices if len(x) > 1]

# Get info for each device from bluetoothctl
dev_info = [x['mac'] for x in devices]
dev_info = [run_shell_cmd("bluetoothctl info " + x).communicate()[0].decode("utf-8") for x in dev_info]

# Split info for each device into a list
info = [x.split("\n") for x in dev_info]

# Split each line of info into a list
info2 = []
for e in info:
    info2.append([x.split("\n") for x in e if len(x) > 1])

# Split each line of info into a list
info3 = []
for e in info2:
    temp = []
    uuid_list = []
    counter = 1
    for x in e:
        if "Device" in x[0]:
            temp.append(f"Device, {x[0][7:24]}".split(","))  # Split other data into separate entries
            #d = {"Device":x[0][7:24]}
            #temp.append(d)
        elif len(x) < 1:  # Skip empty list entries
            pass
        elif "UUID" in x[0]:  # Split UUIDs into separate entries
                uuid_data = x[0].replace("\tUUID: ",'').replace(')','').split('(')
                uuid_data = [x.strip() for x in uuid_data]
                uuid_data.reverse()
                uuid_list.append(uuid_data)
                uuid_data = x[0][7:].strip(')')  # Get UUID data
                #entry = f"UUID{counter}, {uuid_data}" # Create new entry
                #temp.append(entry.split(",")) # Append new entry to temp list
                #counter += 1
        else:
            temp.append(x[0].replace("\t","").split(":"))  # Split other data into separate entries
    temp.append(uuid_list)  # Append UUID list to temp list
    info3.append(temp)  # Append temp list to info3 list

# Create a list of dictionaries for each device
device_info = []
for dev in info3: # Iterate through the outer list
    t = [x for x in dev if len(x) >= 2]
    d = {}  # Initialize a new dictionary for each device
    for each in t:
        if type(each[0]) == str:  # Check if it's a key-value pair
            d[each[0]] = each[1]  # Populate the dictionary with key-value pairs
        else:  # This must be the list of service UUIDs
            d["Services"] = [{uuid[0]: uuid[1]} for uuid in each]
    device_info.append(d)

# Print device info in JSON format
print(json.dumps(device_info, indent=4, sort_keys=True))
