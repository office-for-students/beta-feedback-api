"""Generates a feedback report in CSV format

Reads the feedback JSON docs from the CosmosDB feedback container.

Tries to fix broken URLs caused by characters being filtered by an earlier
version of the Feedback API.

Does some formatting e.g., make the date excel friendly.

Writes report out in CSV format
"""

from datetime import datetime
import json
import os
import re
import csv

import azure.cosmos.cosmos_client as cosmos_client


def generate_report():

    FIELDNAMES = [
        "Date",
        "Page",
        "Is Useful",
        "How Was This Useful",
        "How Could We Improve",
    ]

    feedback_list = get_feedback_list()
    with open("feedback_report.csv", "w", newline="") as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        csvwriter.writeheader()

        for entry in feedback_list:
            csv_entry = get_entry_for_csv(entry)
            csvwriter.writerow(csv_entry)


def get_feedback_list():
    cosmos_db_client = get_cosmos_client()
    collection_link = get_collection_link(
        "AzureCosmosDbDatabaseId", "AzureCosmosDbFeedbackCollectionId"
    )

    query = "SELECT * from c"
    options = {"enableCrossPartitionQuery": True}
    return list(cosmos_db_client.QueryItems(collection_link, query, options))


def get_entry_for_csv(entry):
    csv_entry = {}

    csv_entry["Date"] = convert_to_excel_date(entry["created_at"])
    csv_entry["Page"] = get_fixed_url(entry["page"])
    csv_entry["Is Useful"] = "Yes" if entry["is_useful"] else "No"
    csv_entry["How Was This Useful"] = ""
    csv_entry["How Could We Improve"] = ""

    questions = entry["questions"]
    assert len(questions) == 2, "We expect CMS to add exactly 2 questions"

    for question in questions:
        if "useful" in question["title"]:
            csv_entry["How Was This Useful"] = question["feedback"]
        elif "improve" in question["title"]:
            csv_entry["How Could We Improve"] = question["feedback"]
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


if __name__ == "__main__":
    generate_report()
