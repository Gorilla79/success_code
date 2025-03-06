import serial
import time

# Uno1 보드의 시리얼 포트 설정
uno1_port = "/dev/ttyACM2"
baud_rate = 9600
timeout = 1

try:
    uno_serial_1 = serial.Serial(uno1_port, baud_rate, timeout=timeout)
    time.sleep(2)  # 아두이노와의 안정적인 연결을 위해 대기

    print("Uno1 보드와 연결되었습니다.")

    # 기존 데이터 클리어 (💡 중요)
    uno_serial_1.reset_input_buffer()  # 혹은 uno_serial_1.flushInput()

    # Uno1 보드로 '1' 전송
    uno_serial_1.write("3\n".encode())  # '\n' 추가하여 줄바꿈 문자 전달
    print("Uno1 보드에 '1'을 보냈습니다.")

    time.sleep(0.5)  # 💡 아두이노가 데이터를 처리할 시간을 확보

    # Uno1 보드의 응답 확인
    while True:
        if uno_serial_1.in_waiting > 0:
            received_data = uno_serial_1.readline().strip()
            print(f"Uno1 보드 응답: {received_data.decode('utf-8')}")
            break  # 응답이 오면 종료

except Exception as e:
    print(f"에러 발생: {e}")

finally:
    uno_serial_1.close()
    print("Uno1 보드와의 연결을 종료합니다.")
