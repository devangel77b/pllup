#!/usr/bin/env python3

"""
To start ydotoold do this
# 1. Clear any broken socket files left behind
rm -f ~/.ydotool_socket

# 2. Restart the daemon with your exact user privileges 
sudo ydotoold --socket-path="$HOME/.ydotool_socket" --socket-own="$(id -u):$(id -g)"
"""

import os
import pandas as pd
import time
import subprocess
import sys
import argparse

# Helper function to fire ydotool commands sequentially
def ydo(args):
    env = os.environ.copy()
    env["YDOTOOL_SOCKET"] = os.path.expanduser("~/.ydotool_socket")
                                        
    subprocess.run(["ydotool"] + args, env=env)
    time.sleep(0.1) # Small safety delay between inputs

def run_keyboard_sync(tsv_path):
    try:
        df = pd.read_csv(tsv_path, sep="\t")
    except FileNotFoundError:
        print(f"Error: Could not find file {tsv_path}")
        sys.exit(1)

    print("=" * 60)
    print("🚀 UBUNTU CHROME KEYBOARD EMULATOR STARTING (WAYLAND/YDOTOOL)")
    print("=" * 60)
    print("Starting in 5 seconds... Maximize Google Chrome now!")
    time.sleep(5)

    for index, row in df.iterrows():
        work_id = row['Work id']
        book_id = row['Book Id']
        barcode = row['Barcode']
        other_call = row['LC Classification'] 
        title = row.get('Title', 'Unknown Title')

        print(f"[{index + 1}/{len(df)}] Automating '{title[:20]}...{barcode} {other_call}'")

        # Open the specific copy editor page directly in Google Chrome
        url = f"https://librarything.com/work/{work_id}/edit/{book_id}"
        subprocess.Popen(['google-chrome', url])
        time.sleep(4.0) # Wait for page to render fully

        # Safe area click to bring Chrome window to the active focus layer
        # ydotool mousemove uses --absolute flag
        ydo(["mousemove", "--absolute", "500", "85"])
        ydo(["click", "0xC0"]) # 0xC0 = Left click (press and release)
        time.sleep(0.2)

        # --- FIELD 1: BARCODE ---
        # Ctrl+F -> Key 29 (Ctrl) and Key 33 (F)
        ydo(["key", "29:1", "33:1", "33:0", "29:0"])
        time.sleep(0.3)
        ydo(["type", "Barcode"])
        time.sleep(0.3)
        # Escape -> Key 1
        ydo(["key", "1:1", "1:0"])
        time.sleep(0.2)
        # Tab -> Key 15
        ydo(["key", "15:1", "15:0"])
        time.sleep(0.1)
        
        # Write barcode
        ydo(["type", str(barcode)])
        time.sleep(0.2)

        # --- FIELD 2: LC CALL NUMBER ---
        # Ctrl+F
        ydo(["key", "29:1", "33:1", "33:0", "29:0"])
        time.sleep(0.3)
        ydo(["type", "LC Classification"])
        time.sleep(0.3)
        # Escape
        ydo(["key", "1:1", "1:0"])
        time.sleep(0.2)
        # Tab
        ydo(["key", "15:1", "15:0"])
        time.sleep(0.1)
        
        # Write call number
        ydo(["type", str(other_call)])
        time.sleep(0.2)

        # --- SAVE AND CLOSE ---
        # Ctrl+F
        ydo(["key", "29:1", "33:1", "33:0", "29:0"])
        time.sleep(0.3)
        ydo(["type", "Save"])
        time.sleep(0.3)
        # Escape
        ydo(["key", "1:1", "1:0"])
        time.sleep(0.2)
        # Enter -> Key 28
        ydo(["key", "28:1", "28:0"])
        time.sleep(0.5)
        
        # Close Active Chrome Tab (Ctrl+W) -> Key 29 (Ctrl) and Key 17 (W)
        ydo(["key", "29:1", "17:1", "17:0", "29:0"])
        time.sleep(0.5)

    print("\n🎉 Synchronization complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Push cleaned tsv data back to Librarything")
    parser.add_argument("input_file", help="Path to tsv file; should have title, LCC, and barcode numbers")
    args = parser.parse_args()

    run_keyboard_sync(args.input_file)
