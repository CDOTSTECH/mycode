CREATE OR REPLACE VIEW upi_data.upi_instruments_flat_fixed AS
SELECT 
    -- All your regular fields
    TemplateVersion as template_version,
    Header.AssetClass as asset_class,
    -- ... other fields ...
    
    -- FIXED: CFIDeliveryType properly included
    Derived.CFIDeliveryType as cfi_delivery_type,
    
    -- FIXED: All CFI elements properly extracted
    Derived.CFI[0].Version as current_cfi_version,
    Derived.CFI[0].Value as current_cfi_value,
    Derived.CFI[0].Category.Code as current_category_code,
    Derived.CFI[0].Category.Value as current_category_value,
    
    -- FIXED: All CFI attributes properly extracted
    Derived.CFI[0].Attributes[0].Name as underlying_assets_name,
    Derived.CFI[0].Attributes[0].Value as underlying_assets_value,
    Derived.CFI[0].Attributes[1].Name as return_payout_name,
    Derived.CFI[0].Attributes[1].Value as return_payout_value,
    Derived.CFI[0].Attributes[2].Name as not_applicable_name,
    Derived.CFI[0].Attributes[2].Value as not_applicable_value,
    Derived.CFI[0].Attributes[3].Name as delivery_name,
    Derived.CFI[0].Attributes[3].Value as delivery_value,
    
    -- FIXED: Validation to check CFI completeness
    size(Derived.CFI) as cfi_elements_count,
    CASE 
        WHEN size(Derived.CFI) >= 2 THEN 'Complete'
        WHEN size(Derived.CFI) = 1 THEN 'Partial'
        ELSE 'Missing'
    END as cfi_completeness_status

FROM upi_data.upi_instruments;
