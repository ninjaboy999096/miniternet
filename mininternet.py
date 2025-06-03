import os
import time
import requests
import threading
import keyboard  # pip install keyboard

# URLs
MAIN_URL = 'https://raw.githubusercontent.com/ninjaboy999096/miniternet/main/mininternet.txt'
DEBUG_URL = 'https://raw.githubusercontent.com/ninjaboy999096/miniternet/main/debug_info.txt'

current_url = MAIN_URL
last_content = None

# For detecting sequence a->b->c
sequence = ['a', 'b', 'c']
seq_index = 0

def clear_console():
    os.system('cls')

def fetch_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch file: Status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching file: {e}")
    return None

def check_sequence(key):
    global seq_index, current_url
    if key.name == sequence[seq_index]:
        seq_index += 1
        if seq_index == len(sequence):
            # Sequence complete - switch URL
            if current_url == MAIN_URL:
                current_url = DEBUG_URL
            else:
                current_url = MAIN_URL
            seq_index = 0
    else:
        # Reset if wrong key
        if key.name == sequence[0]:
            seq_index = 1
        else:
            seq_index = 0

def key_listener():
    keyboard.on_press(check_sequence)
    # Wait until ESC pressed to exit
    keyboard.wait('esc')

def main():
    global last_content
    clear_console()
    print("Press 'a', then 'b', then 'c' to switch files. Press ESC to quit.\n")
    
    # Start key listener in a separate thread
    listener_thread = threading.Thread(target=key_listener, daemon=True)
    listener_thread.start()

    while True:
        content = fetch_content(current_url)
        if content and content != last_content:
            clear_console()
            print("Press 'a', then 'b', then 'c' to switch files. Press ESC to quit.\n")
            print(content)
            last_content = content
        time.sleep(3)

if __name__ == "__main__":
    main()
