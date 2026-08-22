import uproot
import numpy as np
import struct
import os
import sys
import glob

# search for files 'run???ch?' in the current folder
matching_files = glob.glob("run???ch?")

# filter to strictly ensure the wildcard placeholders are digits
valid_files = []
for f in matching_files:
    base = os.path.basename(f)
    if (
        len(base) == 9
        and base.startswith("run")
        and base[3:6].isdigit()
        and base[6:8] == "ch"
        and base[8].isdigit()
    ):
        valid_files.append(f)

# determine the latest file if any exist
latest_file = max(valid_files, key=os.path.getmtime) if valid_files else None

# determine the target run file based on arguments or search results
input_file = None

if len(sys.argv) > 1:
    specified_file = sys.argv[1]
    if not os.path.isfile(specified_file):
        print(
            f"Warning: '{specified_file}' does not exist.",
            file=sys.stderr,
        )
        sys.exit(1)
    input_file = specified_file
elif latest_file:
    input_file = latest_file
else:
    print(
        "Warning: No matching run files found in the current folder.",
        file=sys.stderr,
    )
    sys.exit(1)

print(f"Processing {input_file}")

# Pico ADC sampling frequency is approx 500kSPS (using clock divider 0)
# We use 2us per sample interval as a default starting point
SAMPLE_INTERVAL_US = 2 

# Read the first 2 bytes to get n (samples per waveform)
with open(input_file, "rb") as f:
    header_n = f.read(2)
    n = struct.unpack('<H', header_n)[0]
    print(f"Reading file with n={n} samples per waveform")
    
    timestamps = []
    waveforms = []
    max_heights = []
    
    while True:
        ts_data = f.read(8)
        if not ts_data:
            break
        
        wf_data = f.read(n)
        if len(wf_data) < n:
            print("Warning: Partial waveform found at end of file. Stopping.")
            break
        
        ms = struct.unpack('<Q', ts_data)[0]
        wf = np.frombuffer(wf_data, dtype=np.uint8)
        
        timestamps.append(ms)
        waveforms.append(wf)
        max_heights.append(np.max(wf))

if not timestamps:
    print("Error: No valid events found in the file.")
    sys.exit(1)

# Convert to numpy arrays
ts = np.array(timestamps, dtype=np.uint64)
samples = np.array(waveforms, dtype=np.uint8)
max_heights = np.array(max_heights, dtype=np.uint8)

# Create time array for each sample
# Shape: (num_events, n)
sample_times = np.arange(n, dtype=np.float32) * SAMPLE_INTERVAL_US

# Create ROOT file
output_file = os.path.splitext(input_file)[0] + ".root"
with uproot.recreate(output_file) as f:
    f.mktree("t", {
        "n": np.full(len(ts), n, dtype=np.int32),
        "ms": ts,
        "us": np.tile(sample_times, (len(ts), 1)),
        "s": samples,
        "h": max_heights
    })
    
print(f"Successfully converted {len(ts)} events to {output_file}")
