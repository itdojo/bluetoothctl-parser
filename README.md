# bluetoothctl-parser
Script that gatherss device info from bluetoothctl, cleans it up and outputs it to JSON format.

# Usage
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
# Sample Output
<img src=https://dojolabs.s3.amazonaws.com/bluetooth/bluetoothctl-parser-script-output2.jpg>
<img src=https://dojolabs.s3.amazonaws.com/bluetooth/bluetoothctl-parser-script-output1.jpg>

# Troubleshooting
* Script returns only `[]`.
Check that `bluetoothctl scan on` is actually running.

# To Do:
* There are a few fields that soemtimes still have a leading or trailing blank space; I need to remove those.
* Add writing results to a database to include first_seen, last_seen, GPS, etc..
* Integrate GPS recording.

