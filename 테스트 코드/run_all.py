import subprocess
import time

# Path to the virtual environment activation script
VENV_PATH = "source ~/project/bin/activate"

# Function to open a new terminal with virtual environment activated
def open_terminal(script_name):
    command = f"bash -c '{VENV_PATH} && python3 /home/uoeee/{script_name}; exec bash'"

    # Try xfce4-terminal first, fallback to xterm if it fails
    try:
        return subprocess.Popen(["xfce4-terminal", "--hold", "--command", command])
    except FileNotFoundError:
        return subprocess.Popen(["xterm", "-hold", "-e", command])

print("🚀 Starting RaspberryPi Server in Virtual Environment...")
server_terminal = open_terminal("project.py")

time.sleep(2)  # Allow some time for the server to start

print("🎵 Starting Music Client in Virtual Environment...")
music_terminal = open_terminal("music.py")

print("💡 Starting LED Client in Virtual Environment...")
led_terminal = open_terminal("led_control.py")

print("✅ All terminals launched successfully with the virtual environment activated!")
