#!/usr/bin/env python3

import pandas as pd
import pyautogui
import time
import subprocess
import sys

# Safety Feature: Moving your mouse cursor to the extreme top-left corner of 
# your screen will instantly abort the script if things go out of sync.
pyautogui.FAILSAFE = True

def run_keyboard_sync(tsv_path):
    try:
        df = pd.read_csv(tsv_path, sep="\t")
    except FileNotFoundError:
        print(f"Error: Could not find file {tsv_path}")
        sys.exit(1)

    print("=" * 60)
    print("🚀 UBUNTU CHROME KEYBOARD EMULATOR STARTING")
    print("=" * 60)
    print("1. Ensure Google Chrome is logged into your LibraryThing account.")
    print("2. Keep Chrome visible on your primary monitor layout.")
    print("3. Emergency Abort: Slam your mouse into the top-left corner of the screen.")
    print("\nStarting in 5 seconds... Switch to Chrome now!")
    time.sleep(5)

    for index, row in df.iterrows():
        work_id = row['Work id']
        book_id = row['Book Id']
        barcode = row['Barcode']
        title = row.get('Title', 'Unknown Title')

        print(f"[{index + 1}/{len(df)}] Automating '{title[:25]}...' -> {barcode}")

        # Open the specific edit page directly in Google Chrome via Ubuntu's system terminal
        url = f"https://www.librarything.com/work/{work_id}/edit/{book_id}"
        subprocess.Popen(['google-chrome', url])
        
        # Wait for Chrome to spin up and load the page layout
        # (Increase this value to 4.0 if your school internet connection lags)
        time.sleep(3.0)

        # --- KEYBOARD NAVIGATION SEQUENCE ---
        
        # 1. Clear any accidental cursor focus by clicking a safe white space
        # We click near the middle-left area where no buttons reside
        pyautogui.click(x=200, y=400)
        time.sleep(0.2)

        # 2. Focus the page form by pressing Tab once
        pyautogui.press('tab')
        time.sleep(0.1)

        # 3. Use Chrome's native Search tool to jump directly to the field label
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.2)
        pyautogui.write('Barcode')
        time.sleep(0.2)
        pyautogui.press('escape') # Close the tiny search overlay pop-up
        time.sleep(0.2)

        # 4. Press Tab once to jump from the highlighted text into the actual input box
        pyautogui.press('tab')
        time.sleep(0.2)

        # 5. Clear out any old characters that might be sitting in the field
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        time.sleep(0.1)

        # 6. Type the new custom structured barcode string
        pyautogui.write(str(barcode))
        time.sleep(0.2)

        # 7. Use LibraryThing's form submit shortcut (Alt + S) to save changes
        pyautogui.hotkey('alt', 's')
        
        # Wait for the database submission request to clear
        time.sleep(1.5)

        # 8. Close the active Chrome tab so your screen doesn't clutter up
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(0.5)

    print("\n🎉 Synchronization batch run complete!")

if __name__ == "__main__":
    # Point this to whatever staging file output your generation script made
    run_keyboard_sync("marked_catalog.tsv")
