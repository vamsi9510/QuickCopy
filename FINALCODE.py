import keyboard
import pyperclip
from pystray import Icon, MenuItem, Menu
from PIL import Image
import threading
import time

program_running = False
string = ""

def load_image():
    image_path = 'LOGO.png'
    image = Image.open(image_path)
    return image

def copy_to_clipboard():
    global string
    time.sleep(0.1)  # Slight delay to allow clipboard content to stabilize
    new_clipboard_content = pyperclip.paste()

    if new_clipboard_content and (not string or string[-len(new_clipboard_content):] != new_clipboard_content):
        string += new_clipboard_content+" "

def paste_from_clipboard():
    global string
    string = string.replace("  " , " ")
    pyperclip.copy(string)
    string = ""

def main_program():
    global program_running
    paste_from_clipboard()
    keyboard.add_hotkey('ctrl+c', copy_to_clipboard)
    keyboard.add_hotkey('alt+v', paste_from_clipboard)

    while program_running:
        keyboard.wait()

def toggle_program(icon, item):
    global program_running
    program_running = not item.checked
    if program_running:
        threading.Thread(target=main_program, daemon=True).start()
    else:
        keyboard.unhook_all_hotkeys()

def quit_program(icon, item):
    global program_running
    program_running = False
    keyboard.unhook_all_hotkeys()
    icon.stop()

menu = Menu(
    MenuItem('Enable', toggle_program, checked=lambda item: program_running),
    MenuItem('Exit', quit_program)
)

icon_image = load_image()
icon = Icon("Clipboard App", icon_image, "Clipboard App", menu)

icon.run()