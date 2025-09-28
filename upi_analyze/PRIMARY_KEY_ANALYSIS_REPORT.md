# JSON Primary Key Detection Analysis Report

## Executive Summary

I have analyzed 7 JSON files containing financial instrument data (UPI - Unique Product Identifier records) and identified the primary keys and data structure patterns. The analysis processed 500 records from each file for performance optimization.

## Key Findings

### 🔑 Primary Key Detection Results

**The clear primary key across all files is: `Identifier.UPI`**

- **Uniqueness**: 100% across all files
- **Coverage**: 100% across all files  
- **Consistency**: Present in all asset classes

### 📊 Data Structure Overview

All files follow a consistent JSON structure with these top-level fields:
- `TemplateVersion`
- `Header` (contains AssetClass, InstrumentType, UseCase, Level)
- `Identifier` (contains **UPI**, Status, StatusReason, LastUpdateDateTime)
- `Derived` (contains ClassificationType, ShortName, etc.)
- `Attributes` (contains asset-specific details)

## Detailed Analysis by File

### Asset Classes Identified:
1. **Commodities** - Commodity swaps and derivatives
2. **Credit** - Credit default swaps and instruments
3. **Equity** - Equity forwards, options, and swaps
4. **Foreign_Exchange** - FX forwards, swaps, and options
5. **Rates** - Interest rate swaps and derivatives
6. **Other** - Mixed derivative products

### Primary Key Candidates Ranking:

| Field | Uniqueness | Coverage | Best For |
|-------|------------|----------|----------|
| `Identifier.UPI` | 100% | 100% | **PRIMARY KEY** ✅ |
| `Identifier` | 100% | 100% | Alternative composite key |
| `Attributes` | 98.6-100% | 100% | Business logic grouping |
| `Derived` | 100% | 100% | Classification purposes |

## Data Quality Insights

### Record Counts Analyzed:
- **Other-20250920.json**: 500 records
- **Commodities-20250920.json**: 500 records  
- **Credit-20250920.json**: 500 records
- **Equity-20250920.json**: 500 records
- **Foreign_Exchange-20250920.json**: 500 records
- **Rates-20250920.json**: 500 records
- **Other-20250913.json**: 500 records

### Key Characteristics:
- **UPI Format**: 12-character alphanumeric codes (e.g., "QZPHZRJ0L2WH")
- **Status Values**: Primarily "New" status across records
- **Template Version**: Consistently "1" across all records
- **Level**: All records are "UPI" level

## Business Context

These files appear to contain **Unique Product Identifier (UPI)** data for financial derivatives, which is part of regulatory reporting requirements. Each UPI represents a unique standardized OTC derivative product.

### Asset Class Distribution:
- **Foreign Exchange**: Highest variety of use cases (15+ types)
- **Equity**: Second highest variety (13+ types)
- **Rates**: 7 different swap types
- **Commodities**: Primarily basis swaps
- **Credit**: Primarily index swaps
- **Other**: Non-standard derivative products

## Recommendations

### For Database Design:
1. **Use `Identifier.UPI` as the primary key** - it's unique, consistent, and business-meaningful
2. **Create indexes on**:
   - `Header.AssetClass` (for asset class filtering)
   - `Header.InstrumentType` (for instrument type queries)
   - `Header.UseCase` (for use case analysis)
   - `Identifier.LastUpdateDateTime` (for temporal queries)

### For Data Processing:
1. **Data Validation**: Ensure UPI follows 12-character format
2. **Referential Integrity**: UPI should be consistent across related tables
3. **Temporal Tracking**: Use `LastUpdateDateTime` for change tracking
4. **Business Rules**: Validate combinations of AssetClass + InstrumentType + UseCase

### For Analytics:
1. **Dimensional Modeling**: Use Header fields as dimensions
2. **Fact Tables**: Center around UPI as the grain
3. **Time Series**: Track UPI changes over time using LastUpdateDateTime

## Technical Notes

- **File Format**: JSON Lines (one JSON object per line)
- **File Sizes**: Large files (>50MB) suggest production-scale data
- **Data Freshness**: Recent dates (2023-2025) indicate active maintenance
- **Consistency**: High structural consistency across asset classes

## Files Generated:
- `primary_key_candidates.csv` - Detailed primary key analysis
- `data_structure_summary.csv` - Data structure overview
- `analyze_json_primary_keys.py` - Analysis script for reproducibility

---
*Analysis completed on: $(date)*
*Total records analyzed: 3,500 across 7 files*