## Setting Up the Environment

### .env File

You must include a `.env` file in the root directory of the project. This file should contain the following information:

```plaintext
location=<your-location>
datasetId=<your-dataset-id>
projectId=<your-project-id>
```

### config File
In addition to the .env file, a credentials configuration file is required for the project. The path to this credentials file must be specified in the get_client method found in the enablers file.

Insert the Credentials Configuration File
Ensure the credentials configuration file is properly set up and contains all necessary credentials for your project.

Update the get_client Method
1. Open the enablers file.
2. Locate the get_client method.
3. Specify the path to your credentials configuration file where prompted in the code.

### Packages
1. https://pypi.org/project/python-dotenv/
2. https://pypi.org/project/google-cloud-bigquery/1.1.0/
3. https://pypi.org/project/requests/
