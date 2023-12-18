#!/bin/bash

# AWS credentials and region configuration
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
export AWS_DEFAULT_REGION="YOUR_AWS_REGION"

# Redshift cluster details
redshift_cluster="YOUR_REDSHIFT_CLUSTER_ENDPOINT"
database_name="YOUR_DATABASE_NAME"
user_name="YOUR_USERNAME"
password="YOUR_PASSWORD"

# Query to execute
query="SELECT * FROM your_table;"

# Run Redshift query using AWS CLI
result=$(aws redshift-data execute-statement \
    --cluster-identifier "$redshift_cluster" \
    --database "$database_name" \
    --db-user "$user_name" \
    --db-password "$password" \
    --sql "$query" \
    --output json)

# Print query result
echo "$result"
