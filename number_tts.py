from gtts import gTTS
import pygame
import os

# 숫자를 한글로 변환하는 함수
def number_to_korean(number):
    units = ["", "십", "백"]
    digits = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]

    result = []
    length = len(number)

    for i, digit in enumerate(reversed(number)):
        if digit != "0":
            result.append(f"{digits[int(digit)]}{units[i]}")

    result_text = "".join(reversed(result))

    # 특수 규칙 적용
    result_text = result_text.replace("일십", "십")  # 십일, 십이.. 자연스럽게 변환
    result_text += "번"  # "번" 추가 (예: 234 → "이백삼십사번")
    
    return result_text

# 사용자 입력 받기
number = input("숫자를 입력하세요 (예: 1, 15, 234): ").strip()

# 변환된 한글 텍스트 출력
korean_text = number_to_korean(number)
print("음성 출력:", korean_text)

# TTS 음성 생성
tts = gTTS(text=korean_text, lang="ko", slow=False)  # 기본적으로 여성 목소리
output_path = "output.mp3"
tts.save(output_path)

# pygame으로 오디오 재생
pygame.mixer.init()
pygame.mixer.music.load(output_path)
pygame.mixer.music.play()

print("재생 중...")

# 재생이 끝날 때까지 대기
while pygame.mixer.music.get_busy():
    pass

