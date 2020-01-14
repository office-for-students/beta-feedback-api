import logging
import os
import traceback
import json
import sys
import inspect

from datetime import datetime

import azure.functions as func

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from SharedCode.utils import (
    add_created_at_to_feedback,
    get_collection_link,
    get_cosmos_client,
    get_http_error_response_json,
    sanitise_feedback,
)
from SharedCode.exceptions import ValidationError


from .feedback_creator import FeedbackCreator
from .validators import validate_feedback

cosmosdb_uri = os.environ["AzureCosmosDbUri"]
cosmosdb_key = os.environ["AzureCosmosDbKey"]
cosmosdb_database_id = os.environ["AzureCosmosDbDatabaseId"]
cosmosdb_collection_id = os.environ["AzureCosmosDbFeedbackCollectionId"]

# Intialise cosmos db client
client = get_cosmos_client(cosmosdb_uri, cosmosdb_key)


def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        logging.info("PostFeedback http triggered.")

        function_start_datetime = datetime.today().strftime("%d-%m-%Y %H:%M:%S")

        logging.info(
            f"PostFeedback function started on {function_start_datetime}"
        )

        try:
            feedback = req.get_json()
        except ValueError as e:
            logging.error(f"JSON decode error {e}")

            function_fail_datetime = datetime.today().strftime("%d-%m-%Y %H:%M:%S")

            logging.info(
                f"PostFeedback function failed on {function_fail_datetime}"
            )
            return func.HttpResponse(
                get_http_error_response_json(
                    "Bad Request", "json decoding error", str(e)
                ),
                headers={"Content-Type": "application/json"},
                status_code=400,
            )

        try:
            validate_feedback(feedback)
        except ValidationError as e:
            logging.error(f"The feedback data is not valid {feedback}")
            logging.error(f"validate_feedback error message {e.message}")

            function_fail_datetime = datetime.today().strftime("%d-%m-%Y %H:%M:%S")

            logging.info(
                f"PostFeedback function failed on {function_fail_datetime}"
            )
            return func.HttpResponse(
                get_http_error_response_json(
                    "Bad Request", "JSON Validation Error", e.message
                ),
                headers={"Content-Type": "application/json"},
                status_code=400,
            )

        logging.info(f"received feedback: {feedback}")

        sanitise_feedback(feedback)

        logging.info(f"received feedback after sanitise: {feedback}")

        add_created_at_to_feedback(feedback)

        collection_link = get_collection_link(
            cosmosdb_database_id, cosmosdb_collection_id
        )
        feedback_creator = FeedbackCreator(client, collection_link)

        feedback_creator.write_feedback_to_db(feedback)

        function_end_datetime = datetime.today().strftime("%d-%m-%Y %H:%M:%S")

        logging.info(
            f"PostFeedback function finished on {function_end_datetime}"
        )
        return func.HttpResponse(status_code=201)

    except Exception as e:
        logging.error(traceback.format_exc())

        function_fail_datetime = datetime.today().strftime("%d-%m-%Y %H:%M:%S")

        logging.info(
            f"PostFeedback function failed on {function_fail_datetime}"
        )

        # Raise so Azure sends back the HTTP 500
        raise e
