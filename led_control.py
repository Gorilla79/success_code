import serial

# ESP32가 연결된 포트와 전송 속도 설정
ser = serial.Serial('/dev/ttyUSB0', 115200)  # 적절한 포트 이름으로 변경 필요

while True:
    # 사용자 입력을 받아 ESP32로 전송
    text = input("전송할 텍스트를 입력하세요: ")
    ser.write((text + '\n').encode('utf-8'))  # 데이터를 ESP32로 전송
