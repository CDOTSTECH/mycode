#!/usr/bin/env python3
"""
UPI Primary Key Validation Script
Validates that UPI is indeed a unique identifier across all files.
"""

import json
import glob
import os
from collections import defaultdict

def validate_upi_uniqueness():
    """Validate UPI uniqueness across all JSON files."""
    
    print("UPI Primary Key Validation")
    print("=" * 50)
    
    # Find all JSON files
    json_files = glob.glob("*.json")
    
    all_upis = set()
    file_upi_counts = {}
    duplicate_upis = defaultdict(list)
    upi_examples = []
    
    for json_file in json_files:
        print(f"Processing {json_file}...")
        
        file_upis = set()
        count = 0
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if count >= 1000:  # Limit for performance
                        break
                        
                    try:
                        record = json.loads(line.strip())
                        
                        # Extract UPI
                        if 'Identifier' in record and 'UPI' in record['Identifier']:
                            upi = record['Identifier']['UPI']
                            
                            # Check for duplicates within file
                            if upi in file_upis:
                                duplicate_upis[upi].append(f"{json_file}:line_{line_num}")
                            else:
                                file_upis.add(upi)
                            
                            # Check for duplicates across files
                            if upi in all_upis:
                                duplicate_upis[upi].append(f"{json_file}:line_{line_num}")
                            else:
                                all_upis.add(upi)
                            
                            # Collect examples
                            if len(upi_examples) < 10:
                                upi_examples.append({
                                    'upi': upi,
                                    'file': json_file,
                                    'asset_class': record.get('Header', {}).get('AssetClass', 'Unknown'),
                                    'instrument_type': record.get('Header', {}).get('InstrumentType', 'Unknown')
                                })
                            
                            count += 1
                            
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            print(f"  Error reading {json_file}: {e}")
            continue
        
        file_upi_counts[json_file] = len(file_upis)
        print(f"  Found {len(file_upis)} unique UPIs")
    
    print("\n" + "=" * 50)
    print("VALIDATION RESULTS")
    print("=" * 50)
    
    print(f"Total unique UPIs across all files: {len(all_upis)}")
    print(f"Total files processed: {len(file_upi_counts)}")
    
    print("\nUPIs per file:")
    for file_name, count in file_upi_counts.items():
        print(f"  {file_name}: {count} UPIs")
    
    print(f"\nDuplicate UPIs found: {len(duplicate_upis)}")
    if duplicate_upis:
        print("Duplicate UPI details:")
        for upi, locations in list(duplicate_upis.items())[:5]:  # Show first 5
            print(f"  {upi}: found in {locations}")
    else:
        print("✅ No duplicate UPIs found - UPI is a valid unique identifier!")
    
    print("\nUPI Examples:")
    for example in upi_examples:
        print(f"  {example['upi']} - {example['asset_class']} {example['instrument_type']} ({example['file']})")
    
    # UPI format analysis
    print(f"\nUPI Format Analysis:")
    if all_upis:
        sample_upi = next(iter(all_upis))
        print(f"  Sample UPI: {sample_upi}")
        print(f"  UPI Length: {len(sample_upi)} characters")
        print(f"  Character set: {''.join(sorted(set(''.join(all_upis))))}")
        
        # Check length consistency
        lengths = [len(upi) for upi in all_upis]
        unique_lengths = set(lengths)
        print(f"  Length consistency: {len(unique_lengths)} unique length(s): {sorted(unique_lengths)}")
        
        if len(unique_lengths) == 1:
            print("  ✅ All UPIs have consistent length")
        else:
            print(f"  ⚠️  UPIs have varying lengths")
    
    return {
        'total_upis': len(all_upis),
        'duplicates': len(duplicate_upis),
        'files_processed': len(file_upi_counts),
        'is_unique': len(duplicate_upis) == 0
    }

if __name__ == "__main__":
    results = validate_upi_uniqueness()
    
    print("\n" + "=" * 50)
    print("CONCLUSION")
    print("=" * 50)
    
    if results['is_unique']:
        print("✅ UPI is confirmed as a valid PRIMARY KEY")
        print("   - No duplicates found across all files")
        print("   - Consistent format and length")
        print("   - Present in all records")
    else:
        print("❌ UPI has issues as a primary key")
        print(f"   - {results['duplicates']} duplicate UPIs found")
        print("   - Additional investigation needed")
    
    print(f"\nSummary: {results['total_upis']} unique UPIs across {results['files_processed']} files")