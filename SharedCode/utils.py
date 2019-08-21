"""Functions shared by Azure Functions"""

import datetime
import json
import os

import azure.cosmos.cosmos_client as cosmos_client


# Need to allow some of these becuase the unencoded URL is written to the feedback db
PERMITTED_CHARS = (
    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ- ,*.!@?/:#=&%+_"
)


def get_collection_link(db_id, collection_id):
    """Create and return collection link based on values passed in"""

    # Get the relevant properties from Application Settings
    cosmosdb_database_id = os.environ[db_id]
    cosmosdb_collection_id = os.environ[collection_id]

    # Return a link to the relevant CosmosDB Container/Document Collection
    return "dbs/" + cosmosdb_database_id + "/colls/" + cosmosdb_collection_id


def get_cosmos_client():
    cosmosdb_uri = os.environ["AzureCosmosDbUri"]
    cosmosdb_key = os.environ["AzureCosmosDbKey"]

    master_key = "masterKey"

    return cosmos_client.CosmosClient(
        url_connection=cosmosdb_uri, auth={master_key: cosmosdb_key}
    )


def get_http_error_response_json(error_title, error_key, error_value):
    """Returns a JSON object indicating an Http Error"""
    http_error_resp = {}
    http_error_resp["errors"] = []
    http_error_resp["errors"].append(
        {"error": error_title, "error_values": [{error_key: error_value}]}
    )
    return json.dumps(http_error_resp)


def add_created_at_to_feedback(feedback):
    feedback["created_at"] = datetime.datetime.utcnow().isoformat()


def sanitise_feedback(feedback):
    """Only allow whitelisted characters"""
    feedback["page"] = sanitise_input_string(feedback["page"])
    if "questions" in feedback:
        sanitise_questions(feedback["questions"])


def sanitise_questions(questions):
    for question in questions:
        if "title" in question:
            question["title"] = sanitise_input_string(question["title"])
        if "feedback" in question:
            question["feedback"] = sanitise_input_string(question["feedback"])


def sanitise_input_string(input_str):
    return "".join(c for c in input_str if c in PERMITTED_CHARS)
