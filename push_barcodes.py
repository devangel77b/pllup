#!/usr/bin/env python3

import csv
import argparse
import sys
import time
import requests

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Push staged barcodes from an edited TSV live into LibraryThing/TinyCat.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("staged_file", help="Path to your script-generated TSV file containing updated barcodes")
    parser.add_argument("--cookie", required=True, help="Your active LibraryThing browser raw cookie session string")
    parser.add_argument("--delay", type=float, default=1.2, help="Seconds to pause between web requests to prevent rate limiting")
    args = parser.parse_args()

    # The background endpoint LibraryThing uses to quick-save inventory adjustments
    url = "https://librarything.com"
    
    # Pack your cookie and a browser-like User-Agent into the network headers
    headers = {
        'Cookie': args.cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) SchoolLibraryAutomation/1.0'
    }

    # Let Python naturally raise FileNotFoundError if the path is invalid
    with open(args.staged_file, mode='r', encoding='utf-8') as f:
        records = list(csv.DictReader(f, delimiter='\t'))

    if not records:
        print("Error: The staged file is empty.")
        sys.exit(1)

    # Dictionary validation checking (matches the precise casing of your staging script)
    if 'Book Id' not in records[0] or 'Barcode' not in records[0]:
        print("Error: File is missing required columns. Ensure it has both 'Book Id' and 'Barcode'.")
        sys.exit(1)

    print(f"Beginning live catalog synchronization for {len(records)} items...\n")
    
    success_count = 0
    fail_count = 0

    for index, row in enumerate(records, start=1):
        book_id = row.get('Book Id')
        barcode = row.get('Barcode')
        title = row.get('Title', 'Unknown Item')

        # Clean string checks
        if not book_id or not barcode:
            print(f"⚠️ [{index}/{len(records)}] Skipping row: '{title[:25]}...' due to missing Book Id or Barcode field value.")
            continue

        # Exact structure the LibraryThing backend expects when editing a quick barcode
        payload = {
            'bookid': book_id,
            'barcode': barcode,
            'method': 'save_quick_barcode'
        }

        print(f"🚀 [{index}/{len(records)}] Syncing '{title[:30]}...' -> Barcode: {barcode} (ID: {book_id})")

        try:
            # Send the updates securely as a form payload
            response = requests.post(url, data=payload, headers=headers, timeout=10)
            
            # The server will return a 200 OK along with an internal success status text
            if response.status_code == 200:
                print("   ✅ Sync Confirmed")
                success_count += 1
            else:
                print(f"   ❌ Network Issue (HTTP Error Code {response.status_code})")
                fail_count += 1
                
        except requests.exceptions.RequestException as e:
            print(f"   💥 Connection Failed: {e}")
            fail_count += 1

        # Intentional pause so LibraryThing's security firewall doesn't block your school's IP address
        time.sleep(args.delay)

    print(f"\n🎉 Synchronization complete! Success: {success_count} | Failed: {fail_count}")
