import logging
import os
import io
import sys
import inspect
import traceback

from datetime import datetime
from report_generator import generate_report

import azure.functions as func

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from SharedCode.mail_helper import MailHelper
from SharedCode.blob_helper import BlobHelper


def main(req: func.HttpRequest) -> None:
    try:
        logging.info("GenerateReport http triggered.")

        function_start_datetime = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        function_start_date = datetime.today().strftime("%d.%m.%Y")

        mail_helper = MailHelper()
        environment = os.environ["Environment"]
        mail_helper.send_message(f"Automated feedback report generator started on {function_start_datetime}", f"Automated Feedback Report {environment} - {function_start_date} - Started")

        logging.info(
            f"GenerateReport function started on {function_start_datetime}"
        )

        storage_container_name = os.environ["AzureStorageAccountFeedbackContainerName"]
        storage_blob_name = os.environ["AzureStorageBlobName"]

        csvfile = io.BytesIO()

        generate_report(csvfile)

        logging.info(
            "Writing feedback report csv file to blob"
        )

        blob_helper = BlobHelper()

        blob_helper.blob_service.create_blob_from_stream(storage_container_name, storage_blob_name, csvfile, max_connections=1)

        function_end_datetime = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        function_end_date = datetime.today().strftime("%d.%m.%Y")

        mail_helper.send_message(f"Automated feedback report generator failed on {function_end_datetime} at EtlPipeline", f"Automated Feedback Report {environment} - {function_end_date} - Failed")

        logging.info(
            f"GenerateReport function finished on {function_end_datetime}"
        )
        return func.HttpResponse(status_code=201)

    except Exception as e:
        logging.error(traceback.format_exc())

        function_fail_datetime = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        function_fail_date = datetime.today().strftime("%d.%m.%Y")

        mail_helper.send_message(f"Automated feedback report generator failed on {function_fail_datetime} at EtlPipeline", f"Automated Feedback Report {environment} - {function_fail_date} - Failed")

        logging.info(
            f"GenerateReport function failed on {function_fail_datetime}"
        )

        # Raise so Azure sends back the HTTP 500
        raise e
