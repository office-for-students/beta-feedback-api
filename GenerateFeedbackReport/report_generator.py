"""Generates a feedback report in CSV format

Reads the feedback JSON docs from the CosmosDB feedback container.

Tries to fix broken URLs caused by characters being filtered by an earlier
version of the Feedback API.

Does some formatting e.g., make the date excel friendly.

Writes report out in CSV format
"""

import csv
import os
import re
import logging

from datetime import datetime

import azure.cosmos.cosmos_client as cosmos_client


def generate_report(csvfile):

    FIELDNAMES = ["Date", "Page", "Feedback"]

    feedback_list = get_feedback_list()

    csvwriter = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
    csvwriter.writeheader()

    logging.info(
        "Processing feedback list"
    )

    for entry in feedback_list:
        csv_entry = get_entry_for_csv(entry)
        csvwriter.writerow(csv_entry)

    logging.info(
        "Finished processing feedback list"
    )


def get_feedback_list():
    logging.info(
        "Retrieving feedback list from cosmosdb"
    )

    cosmos_db_client = get_cosmos_client()
    collection_link = get_collection_link(
        "AzureCosmosDbDatabaseId", "AzureCosmosDbFeedbackCollectionId"
    )

    query = "SELECT * from c"
    options = {"enableCrossPartitionQuery": True}

    logging.info(
        "Finished retrieving feedback list from cosmosdb"
    )
    return list(cosmos_db_client.QueryItems(collection_link, query, options))


def get_entry_for_csv(entry):
    csv_entry = {}
    csv_entry["Date"] = convert_to_excel_date(entry["created_at"])
    csv_entry["Page"] = get_fixed_url(entry["page"])
    csv_entry["Feedback"] = ""

    questions = entry["questions"]
    for question in questions:
        if question["feedback"]:
            csv_entry["Feedback"] = question["feedback"]
            break

    return csv_entry


def convert_to_excel_date(entry_date):
    dt = datetime.strptime(entry_date, "%Y-%m-%dT%H:%M:%S.%f")
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_cosmos_client():
    cosmosdb_uri = os.environ["AzureCosmosDbUri"]
    cosmosdb_key = os.environ["AzureCosmosDbKey"]

    master_key = "masterKey"

    return cosmos_client.CosmosClient(
        url_connection=cosmosdb_uri, auth={master_key: cosmosdb_key}
    )


def get_collection_link(db_id, collection_id):
    """Return a link to to CosmosDB based on values passed in"""

    cosmosdb_database_id = os.environ[db_id]
    cosmosdb_collection_id = os.environ[collection_id]

    return "dbs/" + cosmosdb_database_id + "/colls/" + cosmosdb_collection_id


def get_fixed_url(url):
    """Fix some issues that may appear in urls that were over sanitised"""

    if re.search(r"https[^:]{1}", url):
        url = re.sub(r"^https", "https://", url)
        url = re.sub(r"azurewebsites\.net", "azurewebsites.net/", url)
    return url
