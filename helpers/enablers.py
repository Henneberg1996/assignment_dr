from google.cloud import bigquery
from google.oauth2 import service_account

#Get client method
def get_client(projectId):
    creds_file_path = "C:/Users/jhs/dr_2/drdk-portal-dataops-playground-75914bbd40e2-jesper.json" 
    credentials = service_account.Credentials.from_service_account_file(creds_file_path)
    client = bigquery.Client(credentials=credentials, project=projectId)
    return client;

#Retrieves alle users
def get_user_rows(users_formatted):
    rows_to_insert = []
    for user in users_formatted:
        print(user)
        rows_to_insert.append({
            "id": user["id"],
            "name": user["name"],
            "username": user["username"],
            "email": user["email"],
            "address": {
                "street": user["address"]["street"],
                "suite": user["address"]["suite"],
                "city": user["address"]["city"],
                "zipcode": user["address"]["zipcode"],
                "geo": {
                    "lat": user["address"]["geo"]["lat"],
                    "lng": user["address"]["geo"]["lng"]
                }
            },
            "phone": user["phone"],
            "website": user["website"],
            "company": {
                "name": user["company"]["name"],
                "catchPhrase": user["company"]["catchPhrase"],
                "bs": user["company"]["bs"]
            }
        })
    return rows_to_insert

#Method responsible for accessing all users in table
def get_all_users(client):
    # Define your query to count the rows
    query = """
    SELECT *
    FROM `drdk-portal-dataops-playground.candidate_assignment.jesper_users`
    """
    query_job = client.query(query)

    # Wait for the query to finish and fetch the results
    results = query_job.result()

    # Process the results
    for row in results:
        print("-----------------------------------------------------------------------")
        print(f"Name: {row['name']}")
        print(f"Email: {row['email']}")
        print("Address:")
        print("-----------------------------------------------------------------------")
        print("")


def estimateQuery(client, job_config):
    # Start the query, passing in the extra configuration.
    query_job = client.query(
        (
            "SELECT *"
            "FROM `bigquery-public-data.github_repos.commits` "
        ),
        job_config=job_config,
    )  # Make an API request.

    # A dry run query completes immediately.
    bytes = query_job.total_bytes_processed
    tib = bytes / (1 << 40)
    price_per_tib_dollar = 7.5
    total_price = tib*price_per_tib_dollar
    dollar_rate = 6.94

    price_in_dkk = dollar_rate * total_price

    print("This query will process {} bytes.".format(query_job.total_bytes_processed))
    print("This query will process {} TiB.".format(tib))
    print("This query will cost {} DKK.".format(price_in_dkk))
