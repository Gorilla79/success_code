# -*- coding: utf-8 -*-
import serial
import time
import sys
import subprocess
import os

# UTF-8 Encoding for proper text output
sys.stdout.reconfigure(encoding='utf-8')

# Serial Port Configuration
mega_port = "/dev/ttyACM0"    # Mega Board
uno_port_1 = "/dev/ttyUSB0"   # First Uno Board (DEVICE THAT NEEDS 4, 1, 2 SIGNALS)
uno_port_2 = "/dev/ttyUSB1"   # Second Uno Board
esp32_port = "/dev/ttyUSB2"   # ESP32 Board

# Serial Port Properties
baud_rate = 9600  # Default Baud Rate
timeout = 1       # Timeout (Seconds)

# Establish Serial Communication
try:
    mega_serial = serial.Serial(mega_port, baud_rate, timeout=timeout)
    uno_serial_1 = serial.Serial(uno_port_1, baud_rate, timeout=timeout)  # DEVICE THAT NEEDS SIGNALS
    uno_serial_2 = serial.Serial(uno_port_2, baud_rate, timeout=timeout)
    esp_serial = serial.Serial(esp32_port, 115200, timeout=timeout)
    print("✅ Serial connections established successfully.")
except Exception as e:
    print(f"⚠️ Serial connection error: {e}")
    exit(1)

# Function to open a new terminal and run a script
def open_terminal(command):
    return subprocess.Popen(["gnome-terminal", "--", "bash", "-c", command])

# Open `music.py` and `led_control.py` in new terminals
print("🎵 Starting music.py...")
music_terminal = open_terminal("python3 /home/uoeee/music.py")

print("💡 Starting led_control.py...")
led_terminal = open_terminal("python3 /home/uoeee/led_control.py")

time.sleep(2)  # Allow some time for terminals to initialize

# Send "START" signal to `music.py`
os.system("echo 'START' > /tmp/music_signal")
print("📤 Sent: START to Music Process")

try:
    while True:
        if mega_serial.in_waiting > 0:  # Check if data is available
            received_data = mega_serial.readline().strip()
            print(f"📥 Received from Mega: {received_data}")

            if received_data == b"1START":
                uno_serial_1.write(b'1')  # Send 1 to Uno Board 1
                print("📤 Sent: 1 to Uno Board 1 (USB0)")

                # Send "BUTTON" signal to `music.py`
                os.system("echo 'BUTTON' > /tmp/music_signal")
                print("📤 Sent: BUTTON to Music Process")

                # Send "GAMESTART" signal to `led_control.py`
                os.system("echo 'GAMESTART' > /tmp/led_signal")
                print("📤 Sent: GAMESTART to LED Process")

                # Wait for "PUSH" from Mega
                while True:
                    if mega_serial.in_waiting > 0:
                        received_data = mega_serial.readline().strip()
                        if received_data == b"PUSH":
                            uno_serial_1.write(b'2')  # Send 2 to Uno Board 1
                            print("📤 Sent: 2 to Uno Board 1 (USB0)")
                            break  # Exit loop when PUSH is received

                # Wait for "3" from Uno Board 1
                while True:
                    if uno_serial_1.in_waiting > 0:
                        received_data_uno1 = uno_serial_1.readline().strip()
                        if received_data_uno1 == b"3":
                            uno_serial_2.write(b'3')
                            print("📤 Sent: 3 to Uno Board 2")
                            break

                # Wait for "4" from Uno Board 2
                while True:
                    if uno_serial_2.in_waiting > 0:
                        received_data_uno2 = uno_serial_2.readline().strip()
                        if received_data_uno2 == b"4":
                            uno_serial_1.write(b'4')  # Send 4 to Uno1
                            print("📤 Sent: 4 to Uno Board 1 (USB0)")
                            break

                # Wait for "5" from Uno Board 1
                while True:
                    if uno_serial_1.in_waiting > 0:
                        received_data_uno1 = uno_serial_1.readline().strip()
                        if received_data_uno1 == b"5":
                            uno_serial_2.write(b'5')
                            print("📤 Sent: 5 to Uno Board 2")
                            break

                # Wait for "6" from Uno Board 2
                while True:
                    if uno_serial_2.in_waiting > 0:
                        received_data_uno2 = uno_serial_2.readline().strip()
                        if received_data_uno2 == b"6":
                            uno_serial_1.write(b'6')
                            print("📤 Sent: 6 to Uno Board 1")

                            # Send "FAIL" signal to `music.py`
                            os.system("echo 'FAIL' > /tmp/music_signal")
                            print("📤 Sent: FAIL to Music Process")

                            # Send "2" and "4" to ESP32
                            esp_serial.write(b"2\n")
                            print("📤 Sent: 2 to ESP32")

                            time.sleep(3)
                            esp_serial.write(b"4\n")
                            print("📤 Sent: 4 to ESP32")

                            # Send "4" again to Uno Board 1 (USB0)
                            uno_serial_1.write(b'4')
                            print("📤 Sent: 4 to Uno Board 1 (USB0) after 3 seconds")

                            break  # Exit loop when 6 is received

        time.sleep(0.1)  # Reduce CPU Usage

except KeyboardInterrupt:
    print("🔴 Program terminated by user.")

finally:
    mega_serial.close()
    uno_serial_1.close()
    uno_serial_2.close()
    esp_serial.close()
    print("✅ Serial ports closed.")
