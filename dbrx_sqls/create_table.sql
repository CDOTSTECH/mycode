CREATE OR REPLACE TABLE commodities_raw
USING json
OPTIONS (path "/FileStore/Commodities-20250913.json");

-----
CREATE OR REPLACE TABLE commodities_flat AS
SELECT
  -- (same SELECT as above)
FROM commodities_raw
LATERAL VIEW explode(Derived.CFI) cfiTable AS cfi
LATERAL VIEW explode(cfi.Attributes) attrTable AS attr