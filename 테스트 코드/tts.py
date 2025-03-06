from gtts import gTTS
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

# User input
number = input("Enter a 3-digit number (e.g., 456): ")

# Convert number to Korean text
units = ["", "십", "백"]
digits = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]

result = []
for i, digit in enumerate(reversed(number)):
    if digit != "0":
        result.append(f"{digits[int(digit)]}{units[i]}")
result_text = " ".join(reversed(result)) + "번 탈락"

# Output path
output_path = "/home/hwaya/voice_dataset/output.mp3"  # Update this path if needed

# Generate TTS audio using gTTS
tts = gTTS(text=result_text, lang="ko")
tts.save(output_path)

print(f"TTS audio has been saved to {output_path}")

# Play the audio using pygame
pygame.mixer.music.load(output_path)
pygame.mixer.music.play()

print("Playing audio... Press 'Ctrl+C' to stop.")
try:
    while pygame.mixer.music.get_busy():
        pass  # Keep the script running while the audio is playing
except KeyboardInterrupt:
    print("\nPlayback interrupted. Exiting.")
    pygame.mixer.music.stop()
