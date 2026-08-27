#!/bin/bash

# Usage: ./flash_avr_mcu.sh <mcu_name> [hex_file_path]

DEFAULT_BIN_PATH="/home/estanislao-crivos/binaries/"

# Check arguments
if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    echo "Usage: $0 <mcu_name> [hex_file_path]"
    echo "Example: $0 atmega2560 /path/to/file.hex"
    exit 1
fi

MCU="$1"

# Use provided HEX path or fallback to default
if [ -n "$2" ]; then
    HEX_FILE="$2"
else
    HEX_FILE="$DEFAULT_BIN_PATH/avr-c-template.hex"
fi

# Check HEX file exists
if [ ! -f "$HEX_FILE" ]; then
    echo "Error: HEX file not found at: $HEX_FILE"
    exit 1
fi

# Automatically find the latest /dev/ttyACM* port
PORT=$(ls -1t /dev/ttyACM* 2>/dev/null | head -n 1)

if [ -z "$PORT" ]; then
    echo "Error: No /dev/ttyACM* device found."
    exit 1
fi

echo "Flashing MCU $MCU @ port: $PORT with HEX file: $HEX_FILE"

# Run avrdude
avrdude -C /etc/avrdude.conf -v -V -p "$MCU" -c stk500v1 -P "$PORT" -b 19200 -U flash:w:"$HEX_FILE":i

# Report result
if [ $? -eq 0 ]; then
    echo "Flash completed successfully."
else
    echo "Flash failed."
    exit 1
fi
