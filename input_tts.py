from gtts import gTTS
import pygame
import os


# 사용자 입력 받기
korean_text = input("문자를 입력하세요 : ").strip()
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

