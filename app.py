import json
import os
import requests
from dotenv import load_dotenv, find_dotenv
from google.cloud import bigquery
from helpers.enablers import get_client, get_user_rows, get_all_users, estimateQuery
from helpers.model import schema

'''
The following code is highly inspired by the docs found here: https://cloud.google.com/bigquery/docs/tables#python_1
'''

# Load environment variables from a .env file
load_dotenv(find_dotenv())  

# Fetch user data from the API and parse JSON response to a list of dictionaries
res = requests.get('https://jsonplaceholder.typicode.com/users')
users_formatted = res.json()


# Get the BigQuery client using a helper function
client = get_client(os.getenv('projectId'))

# Construct the table ID: "your-project.your_dataset.your_table_name"
table_id = f"{os.getenv('projectId')}.{os.getenv('datasetId')}.jesper_users"


# Inspect the structure of the first user
print(users_formatted[0])

# Create the BigQuery table using the defined schema
table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # API request to create the table
print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")


# Generate rows formatted for BigQuery insertion using a helper method
rows_to_insert = get_user_rows(users_formatted)

# Insert rows into the table
is_inserted = client.insert_rows_json(table_id, rows_to_insert)
if not is_inserted:
    print("New rows have been added.")
else:
    print(f"Encountered errors while inserting rows: {is_inserted}")

# ARCHEIVED NEEDED TO FIX BUG IN THE PROCESS
client.delete_table(table_id, not_found_ok=True)

#Print user from query accessing all users at once
get_all_users(client)


# Configure the query job settings
job_config = bigquery.QueryJobConfig(
                                     dry_run=True,  # Enable dry run mode to estimate the cost without running the query
                                     use_query_cache=False # Disable query cache to always process the data for up-to-date results
                                     )

estimateQuery(client, job_config)

