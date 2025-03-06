import pygame
import os

pygame.mixer.init()

music_directory = "/home/uoeee/hwaya_music/"

mp3_files = {
    "1": os.path.join(music_directory, "back.mp3"),
    "2": os.path.join(music_directory, "bingo.mp3"),
    "3": os.path.join(music_directory, "btn.mp3"),
    "4": os.path.join(music_directory, "gameStart.mp3"),
    "5": os.path.join(music_directory, "lose.mp3"),
    "6": os.path.join(music_directory, "play1.mp3"),
    "7": os.path.join(music_directory, "play2.mp3"),
    "8": os.path.join(music_directory, "play3.mp3"),
    "9": os.path.join(music_directory, "play4.mp3"),
    "10": os.path.join(music_directory, "start.mp3"),
    "11": os.path.join(music_directory, "tang.mp3"),
    "12": os.path.join(music_directory, "win.mp3")
}

def play_mp3(file_name):
    
    if os.path.exists(file_name):
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play()
        print(f"{file_name} playing... when you push 'q' button, stop playing music, and when you push 'e' button, exit program.")
        while pygame.mixer.music.get_busy():
            user_input = input("choose (q: stop, e: exit): ").strip()
            if user_input == 'q':
                pygame.mixer.music.stop()
                print("stop playing music.")
                break
            elif user_input == 'e':
                pygame.mixer.music.stop()
                print("exit program.")
                exit(0)
    else:
        print(f"no such '{file_name}'.")

def main():
    while True:
        print("choose one 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 .")
        choice = input("number: ").strip()
        if choice == 'e':
            print("exit program.")
            break
        elif choice in mp3_files:
            play_mp3(mp3_files[choice])
        else:
            print("try again.")

if __name__ == "__main__":
    main()
