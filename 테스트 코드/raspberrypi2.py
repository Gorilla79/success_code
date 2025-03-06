# -*- coding: utf-8 -*-
import serial
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 직렬 포트 설정
mega_port = "/dev/ttyACM0"   # Mega 보드
uno_port_1 = "/dev/ttyACM1"  # Uno 보드 1
uno_port_2 = "/dev/ttyACM2"  # Uno 보드 2

baud_rate = 9600
timeout = 1

# 직렬 통신 설정
try:
    mega_serial = serial.Serial(mega_port, baud_rate, timeout=timeout)
    uno_serial_1 = serial.Serial(uno_port_1, baud_rate, timeout=timeout)
    uno_serial_2 = serial.Serial(uno_port_2, baud_rate, timeout=timeout)

    # 직렬 버퍼 정리
    mega_serial.flushInput()
    uno_serial_1.flushInput()
    uno_serial_2.flushInput()

    print("Serial connections established successfully.")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit(1)


def wait_for_serial(serial_conn, expected_value, timeout=3):
    """
    특정 값을 직렬 포트에서 받을 때까지 대기.
    만약 timeout이 지나도 응답이 없으면 None 반환.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if serial_conn.in_waiting > 0:
            received_data = serial_conn.readline().strip()
            print(f"DEBUG: Received -> {received_data}")  # 디버깅 로그
            if received_data == expected_value:
                return received_data
        time.sleep(0.05)  # CPU 사용률 낮추기
    return None  # 타임아웃 발생


# 메인 로직
try:
    while True:
        # Mega 보드에서 데이터 수신 대기
        received_data = wait_for_serial(mega_serial, b"START")
        if received_data:
            uno_serial_1.write(b'1')  
            print("Sent integer 1 to Uno Board 1")

            # Mega 보드에서 PUSH 신호 대기
            if wait_for_serial(mega_serial, b"PUSH"):
                uno_serial_1.write(b'2')  
                print("Sent integer 2 to Uno Board 1")

                # Uno1에서 "3" 수신 대기
                if wait_for_serial(uno_serial_1, b"3"):
                    print("Received '3' from Uno Board 1")
                    uno_serial_2.write(b'3')  
                    print("Sent '3' to Uno Board 2")

                    # Uno2에서 "4" 수신 대기
                    if wait_for_serial(uno_serial_2, b"4"):
                        print("Received '4' from Uno Board 2")
                        uno_serial_1.write(b'4')  
                        print("Sent '4' to Uno Board 1")

                        # Uno1에서 "5" 수신 대기
                        if wait_for_serial(uno_serial_1, b"5"):
                            print("Received '5' from Uno Board 1")
                            uno_serial_2.write(b'5')  
                            print("Sent '5' to Uno Board 2")

                            # Uno2에서 "6" 수신 대기
                            if wait_for_serial(uno_serial_2, b"6"):
                                print("Received '6' from Uno Board 2")
                                uno_serial_1.write(b'6')  
                                print("Sent '6' to Uno Board 1")

        time.sleep(0.1)  # CPU 사용률 조절

except KeyboardInterrupt:
    print("Program terminated by user.")

finally:
    mega_serial.close()
    uno_serial_1.close()
    uno_serial_2.close()
    print("Serial ports closed.")
