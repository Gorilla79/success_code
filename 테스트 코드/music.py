import pygame
import time

pygame.mixer.init()

MUSIC_PATH = "/home/uoeee/hwaya_music/"
game_start = MUSIC_PATH + "gamestart.mp3"
btn = MUSIC_PATH + "btn.mp3"
play_files = [MUSIC_PATH + "play1.mp3", MUSIC_PATH + "play2.mp3", MUSIC_PATH + "play3.mp3"]
tang = MUSIC_PATH + "tang.mp3"

while True:
    with open("/tmp/music_signal", "r") as f:
        signal = f.read().strip()

    if signal == "START":
        pygame.mixer.music.load(game_start)
        pygame.mixer.music.play()
        print("🎵 Playing gamestart.mp3")
    elif signal == "BUTTON":
        pygame.mixer.music.load(btn)
        pygame.mixer.music.play()
        print("🎵 Playing btn.mp3")
    elif signal == "FAIL":
        pygame.mixer.music.load(tang)
        pygame.mixer.music.play()
        print("🎵 Playing tang.mp3")

    time.sleep(1)
