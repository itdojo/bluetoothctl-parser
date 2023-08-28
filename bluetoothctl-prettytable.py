#!/usr/bin/env python3

# This script parses the output of bluetoothctl to get a list of discovered devices
# and their info. It then prints the info in a table using PrettyTable.
# It refreshes the table every 5 seconds.
# Usage: python3 bluetoothctl-prettytable.py
# Note: 'bluetoothctl scan on' must be running first to get a list of devices
# Author: Colin Weaver, ITdojo, Inc.

import subprocess
import json
from time import sleep
import os
from prettytable import ALL, PrettyTable as pt
from prettytable import PLAIN_COLUMNS, MARKDOWN, ORGMODE, DEFAULT, SINGLE_BORDER, DOUBLE_BORDER, NONE
import signal
import sys

# Function to handle Ctrl+C
def signal_handler(sig, frame):
    print(' [*] Exiting...')
    print()
    sys.exit(0)


# Function to run shell commands
def run_shell_cmd(cmd):
    return subprocess.Popen(
        cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
)


# Function to create PrettyTable
def make_table(device_info, header_row, border, header, padding, style):
    table = pt(header_row)
    table.set_style(style)
    table.border = border
    table.header = header
    table.align = 'l'  # left align data
    table.hrules = ALL  # ALL, FRAME, HEADER, NONE
    table.padding_width = padding  # padding between border and column data
    for each in device_info:
        if "Device" in each.keys():
            device = each["Device"].lstrip(" ").rstrip(" ")
        else:
            device = ""
        if "Name" in each.keys():
            name = each["Name"].lstrip(" ").rstrip(" ")
        else:
            name = ""
        if "Alias" in each.keys():
            alias = each["Alias"].lstrip(" ").rstrip(" ")
        else:
            alias = ""
        if "RSSI" in each.keys():
            rssi = each["RSSI"].lstrip(" ").rstrip(" ")
        else:
            rssi = ""
        if "Icon" in each.keys():
            icon = each["Icon"].lstrip(" ").rstrip(" ")
        else:
            icon = ""
        if "Services" in each.keys():
            gen_object = [x.values() for x in each["Services"]]
            services = [list(x)[0] for x in gen_object]
            services = ",\n ".join(services)
        else:
            services = ""
        table.add_row([device, name, alias, rssi, icon, services])
        table.sortby = "Device"
        table.align["RSSI"] = "c"
    return table


# Get list of devices from bluetoothctl
def get_bluetoothctl_devices():
        # Get list of devices from bluetoothctl
    devices = run_shell_cmd(get_devices_cmd).communicate()[0].decode("utf-8").split("\n")
    devices = [x.replace("Device ","") for x in devices]
    devices = [x.split(" ") for x in devices]
    devices = [{"name":x[1],"mac":x[0]} for x in devices if len(x) > 1]
    return devices


# Get info for each device from bluetoothctl 
def get_bluetoothctl_info(devices):
    # Get info for each device from bluetoothctl
    dev_info = [x['mac'] for x in devices]
    dev_info = [run_shell_cmd(f"{get_info_cmd} " + x).communicate()[0].decode("utf-8") for x in dev_info]
    # Split info for each device into a list
    info = [x.split("\n") for x in dev_info]

    # Split each line of info into a list
    info2 = []
    for e in info:
        info2.append([x.split("\n") for x in e if len(x) > 1])

    # Split each line of info into a list & clean up the data
    clean_dev_info = []
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
        clean_dev_info.append(temp)  # Append temp list to clean_dev_info list
    return clean_dev_info


# Create a list of dictionaries for each device
def create_dev_info_dict(info3):
    device_info = []
    for dev in info3: # Iterate through the outer list
        t = [x for x in dev if len(x) >= 2]
        d = {}  # Initialize a new dictionary for each device
        for each in t:
            if type(each[0]) == str:
                d[each[0]] = each[1]
            else:
                d["Services"] = [{uuid[0]: uuid[1]} for uuid in each]
        device_info.append(d)
    return device_info


# Create PrettyTable
def create_prettytable(device_info):
    return make_table(device_info, header_row, border, header, padding, style)  # header row, border, header, padding


# Main function
def main():
    # Get list of devices from bluetoothctl
    devices = get_bluetoothctl_devices()
    clean_dev_info = get_bluetoothctl_info(devices)
    device_info = create_dev_info_dict(clean_dev_info)
    table = create_prettytable(device_info)
    os.system('clear')
    print(table)
    sleep(5)


# PrettyTable settings
header_row = ["Device", "Name", "Alias", "RSSI", "Icon", "Services"]
border = True 
header = True  
padding = 1 # padding between border and column data
style = DOUBLE_BORDER  # MSWORD_FRIENDLY, PLAIN_COLUMNS, MARKDOWN, ORGMODE, DEFAULT, SINGLE_BORDER, DOUBLE_BORDER, NONE

# bluetoothctl commands
get_devices_cmd = "bluetoothctl devices"
get_info_cmd = "bluetoothctl info"

# Handle Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

os.system('clear')

# Run main function
if __name__ == "__main__":
    while True:
        main()
