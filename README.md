beta-feedback-api
=================
Service to allow users of the discover uni site to send feedback of the site and for this information to be stored for later analysis.

### Important Note for API Users 
Do not display unfiltered errors from the API to the users of the website. The errors returned by the API contain the data provided by the user as part of the request and they may not be safe to render in the browser.

### Configuration Settings

Add the following to your local.settings.json:

| Variable                                 | Default                | Description                                                  |
| ---------------------------------------- | ---------------------- | ------------------------------------------------------------ |
| FUNCTIONS_WORKER_RUNTIME                 | python                 | The programming language the function worker runs on         |
| AzureWebJobsStorage                      | {retrieve from portal} | The default endpoint to access storage account               |
| StopEtlPipelineOnWarning                 | false                  | Boolean flag to stop function worker on a warning            |
| AzureCosmosDbUri                         | {retrieve from portal} | The uri to the cosmosdb instance                             |
| AzureCosmosDbKey                         | {retrieve from portal} | The database key to access cosmosdb instance                 |
| AzureCosmosDbConnectionString            | {retrieve from portal} | The string to enable a connection to the cosomos db resource |
| AzureCosmosDbDatabaseId                  | discoverUni            | The name of the cosmosdb database                            |
| AzureCosmosDbFeedbackCollectionId        | feedback               | The name of the feedback collection/container in cosmosdb    |
| AzureStorageAccountFeedbackContainerName | feedback               | The name of the feedback container in the azure storage      |
| AzureStorageBlobName                     | feedback_report.csv    | The name of the feedback blob in the azure storage           |
| AzureStorageReportUri                    | {retrieve from portal} | The URI to download the feedback report                      |
| Environment                              | {retrieve from portal} | The name of the environment on which the function is running |
| SendGridAPIKey                           | {retrieve from portal} | The API key used by the SendGrid client                      |
| SendGridFromEmail                        |                        | The e-mail address used to send automated e-mails            |
| SendGridFromName                         |                        | The name used to send automated e-mails                      |
| SendGridToEmailList                      |                        | The list of e-mails that will recieve automated e-mails      |

### Setup

### Pre-Setup

1) Install [.Net Core 2.2 SDK](https://dotnet.microsoft.com/download), if you haven't already.
2) Install python 3.6.8 - the latest stable version that works with Azure client.
```
Mac user:
Install homebrew:
1) /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
2) brew install sashkab/python/python36
3) pip3.6 install -U pip setuptools

Windows user:
```
3) Make sure Python 3.6.8 is set on your PATH, you can check this by running `python3 -v` in terminal window.
4) Install Azure Client
```
Mac user:
brew tap azure/functions
brew install azure-functions-core-tools

Windows user:
```
5) Setup Visual Studio Code, install [visual studio code](https://code.visualstudio.com/)
6) Also install the following extensions for visual studio code - documentation [here](https://code.visualstudio.com/docs/editor/extension-gallery)

```
Python
Azure CLI Tools
Azure Account
Azure Functions
Azure Storage
```

7) Sign into Azure with Visual Studio Code - follow documentation [here](https://docs.microsoft.com/en-us/azure/azure-functions/tutorial-vs-code-serverless-python#_sign-in-to-azure)

#### Building resources and running azure function locally

1) Requires [beta-data-pipelines](https://github.com/office-for-students/beta-data-pipelines) to have been built and run once to load data into search index as well as the [beta-postcode-builder](https://github.com/office-for-students/beta-postcode-builder)

2) Retrieve SearchURL and SearchAPIKey from azure search instance that your search API will be connecting to.

3) Retrieve the Azure Storage conection string from azure storage container instance.

3) Create your local.settings.json file at root level of repository and include all environment variables in the configuration settings table above.

6) Create a virtual machine to run the azure function application by running `venv .env` at root level of repository.

7) Run service on virtual machine by doing the following:
```
source .env/bin/activate
pip install -r requirements.txt
func host start
```

### Tests

To run tests, run the following command: `pytest -v`

### Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details.

### License

See [LICENSE](LICENSE.md) for details.