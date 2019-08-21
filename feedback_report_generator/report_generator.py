"""Generates a feedback report in CSV format

Reads the feedback JSON docs from the CosmosDB feedback container.

Tries to fix broken URLs caused by characters being filtered by an earlier
version of the Feedback API.

Formats as necessary e.g., make the date excel friendly.

Writes report out in CSV format


"""

from datetime import datetime
import json
import os
import re
import csv

import azure.cosmos.cosmos_client as cosmos_client

def build_report():

    FIELDNAMES = [
        "date",
        "page",
        "is useful",
        "how was this useful",
        "how could we improve",
    ]

    feedback_list = get_feedback_list()
    csvfile = open("feedback_report.csv", "w", newline="")
    csvwriter = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
    csvwriter.writeheader()

    for entry in feedback_list:
        csv_entry = get_entry_for_csv(entry)
        csvwriter.writerow(csv_entry)
    csvfile.close()


def get_feedback_list():
    cosmos_db_client = get_cosmos_client()
    collection_link = get_collection_link(
        "AzureCosmosDbDatabaseId", "AzureCosmosDbFeedbackCollectionId"
    )

    #
    # If you wish to query all records after a specific date, specify the
    # date as shown in the example below:
    # "SELECT * from c where c.created_at >= \"2019-08-21T10:00:03Z\""
    #

    query = "SELECT * from c"
    options = {"enableCrossPartitionQuery": True}
    return list(cosmos_db_client.QueryItems(collection_link, query, options))


def get_entry_for_csv(entry):
    csv_entry = {}

    csv_entry["date"] = convert_to_excel_date(entry["created_at"])
    csv_entry["page"] = get_fixed_url(entry["page"])
    csv_entry["is useful"] = "Yes" if entry["is_useful"] else "No"
    csv_entry["how was this useful"] = ""
    csv_entry["how could we improve"] = ""
    questions = entry["questions"]

    # Currently CMS always writes exactly two questions to the array.
    assert len(questions) == 2
    for question in questions:
        if "useful" in question["title"]:
            csv_entry["how was this useful"] = question["feedback"]
        elif "improve" in question["title"]:
            csv_entry["how could we improve"] = question["feedback"]
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
    """Fix some of issues that may appear in urls that were over sanitised"""

    if re.search(r"https[^:]{1}", url):
        url = re.sub(r"^https", "https://", url)
        url = re.sub(r"azurewebsites\.net", "azurewebsites.net/", url)
    return url


if __name__ == "__main__":
    build_report()
