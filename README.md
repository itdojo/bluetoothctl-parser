# bluetoothctl-parser

Two python scripts:
1. `bluetoothctl-parser.py` - Gathers device info using **bluetoothctl**, cleans it up and outputs it STDOUT in JSON format.
2. `bluetoothctl-prettytable.py` - Gathers device info from **bluetoothctl**, cleans it and and outputs it to a table. This script gets device data every 5 seconds and refreshes the table.  It runs in a forever loop.

# bluetoothctl-parser.py Usage
1. Start bluetooth scanning using bluetoothctl.  Leave the scan running while using the script.
```bash
bluetoothctl scan on
```
2. Open a second terminal and mark the script executable.
```bash
chmod +x bluetoothctl-parser.py
```
3. Run the script.  No privilege is required.
```bash
./bluetoothctl-parser.py
```

***

# bluetoothctl-prettytable.py Usage
1. Start bluetooth scanning using bluetoothctl.  Leave the scan running while using the script.
```bash
bluetoothctl scan on
```
2. Open a second terminal and mark the script executable.
```bash
chmod +x bluetoothctl-prettytable.py
```
3. Run the script.  No privilege is required.
```bash
./bluetoothctl-prettytable.py
```

# bluetoothctl-parser.py Sample Output

<img src=https://dojolabs.s3.amazonaws.com/bluetooth/bluetoothctl-parser-script-output2.jpg>

<img src=https://dojolabs.s3.amazonaws.com/bluetooth/bluetoothctl-parser-script-output1.jpg>

***

# bluetoothctl-prettytable.py Sample Output

<img src=https://dojolabs.s3.amazonaws.com/bluetooth/bluetoothctl-prettytable.jpg>


***

# Troubleshooting
* `bluetoothctl.py` returns only **[]** or `bluetoothctl-prettytable.py` returns a header row with no devices:
  * Check that `bluetoothctl scan on` is actually running.

***

# To Do:
* There are a few fields that sometimes still have a leading or trailing blank space; I need to remove those.
* Add writing results to a database to include first_seen, last_seen, GPS, etc..
* Integrate GPS recording.
* `bluetoothctl-prettytable.py` sometimes add a wonkily-formatted row when devices are in the process of being added. It goes away as soon as the device is fully seen.  I need to chase it down in the tables to figure out how to clean that up.
