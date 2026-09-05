#!/usr/bin/env python3

import csv
import argparse
import sys
import logging





    












        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stage custom barcodes onto a LibraryThing/TinyCat TSV export.")
    parser.add_argument("input_file", help="Path to the exported TSV file from LibraryThing")
    parser.add_argument("--start", type=int, required=True, help="Starting sequence integer (e.g., 10), default 0",default=0)
    parser.add_argument("--location", required=True, help="Branch location code (e.g., B116, G201), default B116",default="B116")
    parser.add_argument("--output", help="Optional path to save the modified TSV. If omitted, prints preview to screen.")
    args=parser.parse_args()



    
    with open(args.input_file, mode='r', encoding='utf-8') as f:
        # LibraryThing TSV exports use tab delimiters
        reader = list(csv.DictReader(f, delimiter='\t'))

    if not reader:
        logging.error("Error: The input file is empty or formatted incorrectly.")
        sys.exit(1)

    # Check for critical identification field
    if 'Book Id' not in reader[0].keys():
        print("Error: Could not find 'bookid' column. Ensure you exported your file with account IDs included. Without this the updated barcodes cannot be uploaded.")
        sys.exit(1)
        


    current_number = args.start
    updated_records = []

    print(f"\n--- Processing {len(reader)} rows using pattern: {args.location}0000d ---")

    for row in reader:

        # Do barcode
        # Generate padded 5-digit sequence suffix
        barcode_string = f"{args.location}{current_number:05d}"
        # Staging the updates
        row['Barcode'] = barcode_string

        # do call number
        raw_lcc = row.get('LC Classification', '').strip()
        pub_year = row.get('Date', '').strip()
        if raw_lcc:
            if pub_year and pub_year in raw_lcc:
                lcc_year = raw_lcc
            elif pub_year:
                lcc_year = f"{raw_lcc} {pub_year}"
            else:
                lcc_year = raw_lcc
        else:
            lcc_year = ""
        row['LC Classification'] = lcc_year
        
        updated_records.append(row)
        current_number += 1





        
    # Output Pathway A: Screen Check Preview
    if not args.output:
        print(f"{'Book Id':<12} | {'Title':<40} | {'LC Classification':<20} | {'Updated Barcode':<15}")
        for row in updated_records:
            title_trunc = row.get('Title', 'Unknown Title')[:40]
            print(f"{row['Book Id']:<12} | {title_trunc:<40} | {row['LC Classification']:<20} | {row['Barcode']:<15}")
        print("\n💡 Run the script again adding '--output marked_catalog.tsv' to save this dataset once verified.")

    # Output Pathway B: Save to Local Staging File
    else:
        with open(args.output, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()
            writer.writerows(updated_records)
        print(f"💾 Success! Staged records exported cleanly to: {args.output}")


