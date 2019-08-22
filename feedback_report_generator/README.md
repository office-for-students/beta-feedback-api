create feedback reports
=================
Program to create feedback reports.

### Configuration Settings

Before running the script, set the following environment variables.

| Variable                            | Default                | Description                                              |
| ----------------------------------- | ---------------------- | -------------------------------------------------------- |
| AzureCosmosDbDatabaseId | retrieve from portal | The id of a CosmosDB instance that holds the latest feedback data in a container called urkrlp.|
| AzureCosmosDbFeedbackCollectionId | feedback | the container name holding the feedback data |
| AzureCosmosDbUri | retrieve from portal | the uri to CosmosDB |
| AzureCosmosDbKey | retrieve from portal | the key to authenticate to CosmosDB |


### Setup

* Ensure python 3.6 ot greater is installed
* Create a Python virtualenv to run this tool in
* Activate the virtualenv

```
pip install -r requirements.txt
```

### Running the report generator

1. Created a file called setup_env_vars.sh as shown below:

export AzureCosmosDbUri="<uri>"
export AzureCosmosDbKey="<connection_key>"
export AzureCosmosDbDatabaseId="<database_id>"
export AzureCosmosDbFeedbackCollectionId="<collection_id>"

2. Run 
```
source setup_env_vars.sh
```

3. Run 
```
python report_generator.py
```

