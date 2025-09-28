#!/usr/bin/env python3
"""
JSON Primary Key Detection Script
Analyzes JSON files to identify potential primary keys and data structure patterns.
"""

import json
import os
import glob
from collections import defaultdict, Counter
from typing import Dict, List, Set, Any, Tuple
import pandas as pd

def load_json_lines(file_path: str, max_records: int = 1000) -> List[Dict]:
    """Load JSON lines from a file, limiting to max_records for performance."""
    records = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= max_records:
                    break
                try:
                    record = json.loads(line.strip())
                    records.append(record)
                except json.JSONDecodeError as e:
                    print(f"Error parsing line {i+1} in {file_path}: {e}")
                    continue
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return records

def extract_all_paths(obj: Any, prefix: str = "") -> Set[str]:
    """Extract all possible field paths from a nested JSON object."""
    paths = set()
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{prefix}.{key}" if prefix else key
            paths.add(current_path)
            paths.update(extract_all_paths(value, current_path))
    elif isinstance(obj, list) and obj:
        # For lists, analyze the first element to understand structure
        paths.update(extract_all_paths(obj[0], f"{prefix}[0]"))
    
    return paths

def analyze_field_uniqueness(records: List[Dict], field_path: str) -> Tuple[int, int, float]:
    """Analyze uniqueness of a field across records."""
    values = []
    
    for record in records:
        try:
            # Navigate nested path
            current = record
            for part in field_path.split('.'):
                if '[0]' in part:
                    part = part.replace('[0]', '')
                    if part in current and isinstance(current[part], list) and current[part]:
                        current = current[part][0]
                    else:
                        current = None
                        break
                elif part in current:
                    current = current[part]
                else:
                    current = None
                    break
            
            if current is not None:
                values.append(str(current))
        except:
            continue
    
    total_values = len(values)
    unique_values = len(set(values))
    uniqueness_ratio = unique_values / total_values if total_values > 0 else 0
    
    return total_values, unique_values, uniqueness_ratio

def detect_primary_keys(records: List[Dict]) -> Dict[str, Any]:
    """Detect potential primary keys in the dataset."""
    if not records:
        return {}
    
    # Extract all possible field paths
    all_paths = set()
    for record in records[:10]:  # Sample first 10 records for path discovery
        all_paths.update(extract_all_paths(record))
    
    # Analyze each field for primary key characteristics
    primary_key_candidates = []
    field_analysis = {}
    
    for field_path in sorted(all_paths):
        total_count, unique_count, uniqueness_ratio = analyze_field_uniqueness(records, field_path)
        
        field_analysis[field_path] = {
            'total_count': total_count,
            'unique_count': unique_count,
            'uniqueness_ratio': uniqueness_ratio,
            'coverage': total_count / len(records) if records else 0
        }
        
        # Primary key criteria:
        # 1. High uniqueness ratio (>= 0.95)
        # 2. High coverage (>= 0.9)
        # 3. Reasonable number of values
        if (uniqueness_ratio >= 0.95 and 
            total_count >= len(records) * 0.9 and 
            unique_count > 1):
            primary_key_candidates.append({
                'field': field_path,
                'uniqueness_ratio': uniqueness_ratio,
                'coverage': total_count / len(records),
                'total_values': total_count,
                'unique_values': unique_count
            })
    
    # Sort candidates by uniqueness ratio and coverage
    primary_key_candidates.sort(key=lambda x: (x['uniqueness_ratio'], x['coverage']), reverse=True)
    
    return {
        'primary_key_candidates': primary_key_candidates,
        'field_analysis': field_analysis,
        'total_records': len(records)
    }

def analyze_data_structure(records: List[Dict]) -> Dict[str, Any]:
    """Analyze the general structure of the data."""
    if not records:
        return {}
    
    # Common top-level fields
    top_level_fields = Counter()
    for record in records:
        if isinstance(record, dict):
            top_level_fields.update(record.keys())
    
    # Sample record structure
    sample_record = records[0] if records else {}
    
    # Detect asset classes if present
    asset_classes = Counter()
    instrument_types = Counter()
    use_cases = Counter()
    
    for record in records:
        try:
            if 'Header' in record:
                header = record['Header']
                if 'AssetClass' in header:
                    asset_classes[header['AssetClass']] += 1
                if 'InstrumentType' in header:
                    instrument_types[header['InstrumentType']] += 1
                if 'UseCase' in header:
                    use_cases[header['UseCase']] += 1
        except:
            continue
    
    return {
        'top_level_fields': dict(top_level_fields.most_common()),
        'sample_record_keys': list(sample_record.keys()) if isinstance(sample_record, dict) else [],
        'asset_classes': dict(asset_classes.most_common()),
        'instrument_types': dict(instrument_types.most_common()),
        'use_cases': dict(use_cases.most_common())
    }

def analyze_file(file_path: str, max_records: int = 1000) -> Dict[str, Any]:
    """Analyze a single JSON file."""
    print(f"\nAnalyzing {os.path.basename(file_path)}...")
    
    records = load_json_lines(file_path, max_records)
    
    if not records:
        return {'error': 'No records loaded', 'file': file_path}
    
    print(f"  Loaded {len(records)} records")
    
    # Detect primary keys
    pk_analysis = detect_primary_keys(records)
    
    # Analyze data structure
    structure_analysis = analyze_data_structure(records)
    
    return {
        'file': os.path.basename(file_path),
        'file_path': file_path,
        'records_analyzed': len(records),
        'primary_key_analysis': pk_analysis,
        'structure_analysis': structure_analysis
    }

def main():
    """Main analysis function."""
    print("JSON Primary Key Detection Analysis")
    print("=" * 50)
    
    # Find all JSON files in the current directory
    json_files = glob.glob("*.json")
    
    if not json_files:
        print("No JSON files found in the current directory.")
        return
    
    print(f"Found {len(json_files)} JSON files:")
    for file in json_files:
        print(f"  - {file}")
    
    all_results = {}
    
    # Analyze each file
    for json_file in json_files:
        try:
            result = analyze_file(json_file, max_records=500)  # Limit for performance
            all_results[json_file] = result
        except Exception as e:
            print(f"Error analyzing {json_file}: {e}")
            all_results[json_file] = {'error': str(e)}
    
    # Generate summary report
    print("\n" + "=" * 80)
    print("PRIMARY KEY DETECTION SUMMARY")
    print("=" * 80)
    
    for file_name, result in all_results.items():
        if 'error' in result:
            print(f"\n{file_name}: ERROR - {result['error']}")
            continue
            
        print(f"\n{file_name}:")
        print(f"  Records analyzed: {result['records_analyzed']}")
        
        # Primary key candidates
        pk_candidates = result['primary_key_analysis'].get('primary_key_candidates', [])
        if pk_candidates:
            print(f"  Primary Key Candidates ({len(pk_candidates)}):")
            for i, candidate in enumerate(pk_candidates[:5], 1):  # Top 5
                print(f"    {i}. {candidate['field']}")
                print(f"       Uniqueness: {candidate['uniqueness_ratio']:.3f}")
                print(f"       Coverage: {candidate['coverage']:.3f}")
                print(f"       Values: {candidate['unique_values']}/{candidate['total_values']}")
        else:
            print("  No strong primary key candidates found")
        
        # Data structure info
        structure = result['structure_analysis']
        if 'asset_classes' in structure and structure['asset_classes']:
            print(f"  Asset Classes: {list(structure['asset_classes'].keys())}")
        if 'instrument_types' in structure and structure['instrument_types']:
            print(f"  Instrument Types: {list(structure['instrument_types'].keys())}")
    
    # Generate detailed CSV report
    print(f"\n" + "=" * 50)
    print("Generating detailed reports...")
    
    # Create primary key candidates report
    pk_report_data = []
    for file_name, result in all_results.items():
        if 'error' in result:
            continue
        pk_candidates = result['primary_key_analysis'].get('primary_key_candidates', [])
        for candidate in pk_candidates:
            pk_report_data.append({
                'file': file_name,
                'field': candidate['field'],
                'uniqueness_ratio': candidate['uniqueness_ratio'],
                'coverage': candidate['coverage'],
                'unique_values': candidate['unique_values'],
                'total_values': candidate['total_values']
            })
    
    if pk_report_data:
        pk_df = pd.DataFrame(pk_report_data)
        pk_df.to_csv('primary_key_candidates.csv', index=False)
        print("  - primary_key_candidates.csv")
    
    # Create structure summary report
    structure_data = []
    for file_name, result in all_results.items():
        if 'error' in result:
            continue
        structure = result['structure_analysis']
        structure_data.append({
            'file': file_name,
            'records_analyzed': result['records_analyzed'],
            'top_level_fields': ', '.join(structure.get('top_level_fields', {}).keys()),
            'asset_classes': ', '.join(structure.get('asset_classes', {}).keys()),
            'instrument_types': ', '.join(structure.get('instrument_types', {}).keys()),
            'use_cases': ', '.join(structure.get('use_cases', {}).keys())
        })
    
    if structure_data:
        structure_df = pd.DataFrame(structure_data)
        structure_df.to_csv('data_structure_summary.csv', index=False)
        print("  - data_structure_summary.csv")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()