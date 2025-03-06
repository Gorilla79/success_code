# -*- coding: utf-8 -*-
import serial
import time
import sys

# Ensure UTF-8 encoding for proper text output
sys.stdout.reconfigure(encoding='utf-8')

# Serial port configuration
mega_port = "/dev/ttyACM0"   # Mega board
uno_port_1 = "/dev/ttyACM1"  # First Uno board
uno_port_2 = "/dev/ttyACM2"  # Second Uno board (New)

# Serial port properties
baud_rate = 9600  # Default baud rate for Arduino
timeout = 1       # Response timeout (seconds)

# Establish serial communication with Mega and Uno boards
try:
    mega_serial = serial.Serial(mega_port, baud_rate, timeout=timeout)
    uno_serial_1 = serial.Serial(uno_port_1, baud_rate, timeout=timeout)
    uno_serial_2 = serial.Serial(uno_port_2, baud_rate, timeout=timeout)
    print("Serial connections established successfully.")

    # 💡 시리얼 버퍼 초기화
    mega_serial.reset_input_buffer()
    uno_serial_1.reset_input_buffer()
    uno_serial_2.reset_input_buffer()
    time.sleep(2)  # 💡 아두이노와 안정적인 연결을 위해 대기

except Exception as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Main loop: Read from Mega and forward data to Uno if needed
try:
    while True:
        if mega_serial.in_waiting > 0:  # Check if data is available
            received_data = mega_serial.readline().strip()  # Read raw bytes
            
            print(f"Received from Mega: {received_data}")

            if b"START" in received_data:  # Ensure it's a byte, not a string
                uno_serial_1.write("1\n".encode())  # ✅ '\n' 추가하여 문자열 전송
                print("Successfully sent '1' to Uno Board 1")
                time.sleep(0.5)  # 💡 전송 후 대기

                # Wait for PUSH from Mega
                while True:
                    if mega_serial.in_waiting > 0:
                        received_data = mega_serial.readline().strip()
                        if received_data == b"PUSH":
                            uno_serial_1.write("2\n".encode())  # ✅ 변경
                            print("Successfully sent '2' to Uno Board 1")
                            time.sleep(0.5)
                            break  # Exit loop when PUSH is received
                
                # Wait for "3" from Uno Board 1
                while True:
                    if uno_serial_1.in_waiting > 0:
                        received_data_uno1 = uno_serial_1.readline().strip()
                        if received_data_uno1 == b"3":
                            print(f"Received from Uno1: {received_data_uno1}")

                            # Send "3" to Uno Board 2
                            uno_serial_2.write("3\n".encode())  # ✅ 변경
                            print("Sent '3' to Uno Board 2")
                            time.sleep(0.5)

                            # Wait for "4" from Uno Board 2
                            while True:
                                if uno_serial_2.in_waiting > 0:
                                    received_data_uno2 = uno_serial_2.readline().strip()
                                    if received_data_uno2 == b"4":
                                        print(f"Received from Uno2: {received_data_uno2}")
                                        uno_serial_1.write("4\n".encode())  # ✅ 변경
                                        print("Successfully sent '4' to Uno Board 1")
                                        time.sleep(0.5)
                                        break  # Exit loop when 4 is received
                            break  # Exit loop when 3 is processed

                # Wait for "5" from Uno Board 1
                while True:
                    if uno_serial_1.in_waiting > 0:
                        received_data_uno1 = uno_serial_1.readline().strip()
                        if received_data_uno1 == b"5":
                            print(f"Received from Uno1: {received_data_uno1}")

                            # Send "5" to Uno Board 2
                            uno_serial_2.write("5\n".encode())  # ✅ 변경
                            print("Sent '5' to Uno Board 2")
                            time.sleep(0.5)
                            break  # Exit loop when 5 is sent

                # Wait for "6" from Uno Board 2
                while True:
                    if uno_serial_2.in_waiting > 0:
                        received_data_uno2 = uno_serial_2.readline().strip()
                        if received_data_uno2 == b"6":
                            print(f"Received from Uno2: {received_data_uno2}")

                            # Send "6" to Uno Board 1
                            uno_serial_1.write("6\n".encode())  # ✅ 변경
                            print("Sent '6' to Uno Board 1")
                            time.sleep(0.5)
                            break  # Exit loop when 6 is received

        time.sleep(0.1)  # Reduce CPU usage

except KeyboardInterrupt:
    print("Program terminated by user.")

finally:
    # Close serial ports before exiting
    mega_serial.close()
    uno_serial_1.close()
    uno_serial_2.close()
    print("Serial ports closed.")
