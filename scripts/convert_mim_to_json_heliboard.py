#!/usr/bin/env python3
"""
Convert bn-khipro.mim file to structured JSON format.

This script parses the M17N input method file and organizes mappings
into categories like SHOR (vowels), FKAR (vowel marks), BYANJON (consonants), etc.
"""

import json
import re
from collections import OrderedDict


def parse_mim_file(filename):
    """Parse the .mim file and extract mappings by category."""
    
    mappings = {
        "SHOR": {},      # Vowels (স্বরবর্ণ)
        "FKAR": {},      # Vowel marks/diacritics (কার/স্বরচিহ্ন)
        "BYANJON": {},   # Consonants (ব্যঞ্জনবর্ণ)
        "JUKTOBORNO": {},  # Conjuncts (যুক্তবর্ণ)
        "NG": {},        # Anusvara and related (ং)
        "REPH": {},      # Reph (র্)
        "PHOLA": {},     # Phola (র, য)
        "KAR": {},       # Vowel signs after consonants
        "ONGKO": {},     # Numbers and letters (অঙ্ক)
        "DIACRITIC": {}, # Special marks (hasant, visarga, etc.)
        "BIRAM": {},     # Punctuation (বিরাম চিহ্ন)
        "PRITHAYOK": {}, # Separator
        "AE": {}         # Special AE
    }
    
    current_map = None
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith(';;'):
                continue
            
            # Detect map sections
            if line.startswith('(') and not line.startswith('("'):
                # Check for map section headers
                if '(shor' in line:
                    current_map = 'SHOR'
                elif '(fkar' in line:
                    current_map = 'FKAR'
                elif '(byanjon' in line:
                    current_map = 'BYANJON'
                elif '(juktoborno' in line:
                    current_map = 'JUKTOBORNO'
                elif '(ng' in line and current_map != 'NG':
                    current_map = 'NG'
                elif '(reph' in line:
                    current_map = 'REPH'
                elif '(phola' in line:
                    current_map = 'PHOLA'
                elif '(kar' in line:
                    current_map = 'KAR'
                elif '(ongko' in line:
                    current_map = 'ONGKO'
                elif '(diacritic' in line:
                    current_map = 'DIACRITIC'
                elif '(biram' in line:
                    # Skip BIRAM - we'll add custom entry manually
                    current_map = None
                elif '(prithayok' in line:
                    current_map = 'PRITHAYOK'
                elif '(ae' in line:
                    current_map = 'AE'
                elif '(state' in line or '(init' in line:
                    # End of mappings section
                    current_map = None
                continue
            
            # Parse mappings in the format ("key" "value")
            if current_map and line.startswith('("'):
                # Extract all mappings from the line
                pattern = r'\("([^"]+)"\s+"([^"]*)"\)'
                matches = re.findall(pattern, line)
                for key, value in matches:
                    mappings[current_map][key] = value
    
    return mappings


def main():
    """Main function to convert .mim to JSON."""
    input_file = 'bn-khipro.mim'
    output_file = 'khipro-mappings-heliboard.json'
    
    print(f"Parsing {input_file}...")
    mappings = parse_mim_file(input_file)
    
    # Create BIRAM with only custom entry (not converted from .mim)
    mappings["BIRAM"] = {
        "।ff": "৺"
    }
    
    # Filter DIACRITIC to only include specific entries
    if "DIACRITIC" in mappings:
        allowed_diacritics = ["qq", "xx", "t/", "x", "/", "//"]
        mappings["DIACRITIC"] = {
            key: value for key, value in mappings["DIACRITIC"].items() 
            if key in allowed_diacritics
        }
    
    # Remove ONGKO category entirely
    if "ONGKO" in mappings:
        del mappings["ONGKO"]
    
    # Display statistics
    print("\nMapping Statistics:")
    for category, items in mappings.items():
        if items:
            print(f"  {category}: {len(items)} mappings")
    
    # Save to JSON with proper formatting
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mappings, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Successfully converted to {output_file}")
    
    # Display a sample
    print("\nSample output (SHOR and FKAR):")
    sample = {
        "SHOR": dict(list(mappings["SHOR"].items())[:5]),
        "FKAR": dict(list(mappings["FKAR"].items())[:5])
    }
    print(json.dumps(sample, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
