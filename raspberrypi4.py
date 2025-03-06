# -*- coding: utf-8 -*-
import serial
import time
import sys

# Ensure UTF-8 encoding for proper text output
sys.stdout.reconfigure(encoding='utf-8')

# Serial port configuration
mega_port = "/dev/mega"   # Mega board
uno_port_1 = "/dev/uno1"  # First Uno board
uno_port_2 = "/dev/uno2"  # Second Uno board (New)

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
                uno_serial_1.write(b"1\n")  # ✅ '\n' 추가하여 문자열 전송
                uno_serial_1.flush()  # 💡 즉시 전송 보장
                print("Successfully sent '1' to Uno Board 1")

                # Wait for PUSH from Mega
                while mega_serial.in_waiting == 0:
                    pass  # 기다리는 동안 다른 작업 방해 없이 대기
                
                received_data = mega_serial.readline().strip()
                if received_data == b"PUSH":
                    uno_serial_1.write(b"2\n")  # ✅ 변경
                    uno_serial_1.flush()  # 💡 즉시 전송 보장
                    print("Successfully sent '2' to Uno Board 1")

                # Wait for "3" from Uno Board 1
                while True:
                    if uno_serial_1.in_waiting > 0:
                        received_data_uno1 = uno_serial_1.readline().strip()
                        print(f"Received from Uno1: {received_data_uno1}")
                        if received_data_uno1 == b"3":
                            uno_serial_2.write(b"3\n")  # ✅ 변경
                            uno_serial_2.flush()
                            print("Sent '3' to Uno Board 2")
                            break  # Exit loop when 3 is received
                
                # Wait for "4" from Uno Board 2
                while True:
                    if uno_serial_2.in_waiting > 0:
                        received_data_uno2 = uno_serial_2.readline().strip()
                        print(f"Received from Uno2: {received_data_uno2}")
                        if received_data_uno2 == b"4":
                            uno_serial_1.write(b"4\n")  # ✅ 변경
                            uno_serial_1.flush()
                            print("Successfully sent '4' to Uno Board 1")
                            break  # Exit loop when 4 is received

                # Wait for "5" from Uno Board 1
                while True:
                    if uno_serial_1.in_waiting > 0:
                        received_data_uno1 = uno_serial_1.readline().strip()
                        print(f"Received from Uno1: {received_data_uno1}")
                        if received_data_uno1 == b"5":
                            uno_serial_2.write(b"5\n")  # ✅ 변경
                            uno_serial_2.flush()
                            print("Sent '5' to Uno Board 2")
                            break  # Exit loop when 5 is sent

                # Wait for "6" from Uno Board 2
                while True:
                    if uno_serial_2.in_waiting > 0:
                        received_data_uno2 = uno_serial_2.readline().strip()
                        print(f"Received from Uno2: {received_data_uno2}")
                        if received_data_uno2 == b"6":
                            uno_serial_1.write(b"6\n")  # ✅ 변경
                            uno_serial_1.flush()
                            print("Sent '6' to Uno Board 1")
                            break  # Exit loop when 6 is received

        time.sleep(0.05)  # Reduce CPU usage

except KeyboardInterrupt:
    print("Program terminated by user.")

finally:
    # Close serial ports before exiting
    mega_serial.close()
    uno_serial_1.close()
    uno_serial_2.close()
    print("Serial ports closed.")

