from pyspark.sql.functions import col

def flatten_df(df):
    flat_cols = []
    nested_cols = []

    for field in df.schema.fields:
        if str(field.dataType).startswith("StructType"):
            nested_cols.append(field.name)
        else:
            flat_cols.append(field.name)

    flat_df = df.select(flat_cols + [
        col(f"{nested}.{sub}").alias(f"{nested}_{sub}")
        for nested in nested_cols
        for sub in df.select(f"{nested}.*").columns
    ])

    if len(nested_cols) != 0:
        return flatten_df(flat_df)
    else:
        return flat_df

df_flat = flatten_df(df)
