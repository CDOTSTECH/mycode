-- Step 1: Read the JSON file as a DataFrame
CREATE OR REPLACE TEMP VIEW raw_other_json AS
SELECT *
FROM json.`/FileStore/tables/Other-20250913.json`;

-- Step 2: Flatten the JSON and create a table
CREATE OR REPLACE TABLE flattened_other AS
SELECT
  TemplateVersion,
  Header.AssetClass,
  Header.InstrumentType,
  Header.UseCase,
  Header.Level,
  Identifier.UPI,
  Identifier.Status,
  Identifier.StatusReason,
  Identifier.LastUpdateDateTime,
  Derived.ClassificationType,
  Derived.ShortName,
  Derived.UnderlyingAssetClass.Rates.UnderlierName,
  Derived.FurtherGrouping,
  attr.Version AS CFI_Version,
  attr.VersionStatus AS CFI_VersionStatus,
  attr.Value AS CFI_Value,
  attr.Category.Code AS CFI_CategoryCode,
  attr.Category.Value AS CFI_CategoryValue,
  attr.Group.Code AS CFI_GroupCode,
  attr.Group.Value AS CFI_GroupValue,
  att.Name AS CFI_AttributeName,
  att.Code AS CFI_AttributeCode,
  att.Value AS CFI_AttributeValue,
  Attributes.UnderlyingAssetClass.Rates.NotionalCurrency,
  Attributes.UnderlyingAssetClass.Rates.UnderlierCharacteristic,
  Attributes.UnderlyingAssetClass.Rates.ReferenceRate,
  Attributes.UnderlyingAssetClass.Rates.ReferenceRateTermValue,
  Attributes.UnderlyingAssetClass.Rates.ReferenceRateTermUnit,
  Attributes.DeliveryType
FROM raw_other_json
LATERAL VIEW explode(Derived.CFI) cfiTable AS attr
LATERAL VIEW explode(attr.Attributes) attrTable AS att;