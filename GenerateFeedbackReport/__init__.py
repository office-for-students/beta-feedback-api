import logging
import os
import io
import sys
import inspect
import traceback

from datetime import datetime

import azure.functions as func

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from SharedCode.mail_helper import MailHelper
from SharedCode.blob_helper import BlobHelper

from .report_generator import generate_report


def main(req: func.HttpRequest) -> None:
    mail_helper = MailHelper()
    environment = os.environ["Environment"]

    try:
        logging.info("GenerateReport http triggered.")

        function_start_datetime = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        function_start_date = datetime.today().strftime("%d.%m.%Y")

        mail_helper.send_message(f"Automated feedback report generator started on {function_start_datetime}", f"Automated Feedback Report {environment} - {function_start_date} - Started")

        logging.info(
            f"GenerateReport function started on {function_start_datetime}"
        )

        storage_container_name = os.environ["AzureStorageAccountFeedbackContainerName"]
        storage_blob_name = os.environ["AzureStorageBlobName"]

        csvfile = io.StringIO()

        generate_report(csvfile)

        logging.info(
            "Writing feedback report csv file to blob"
        )

        encoded_file = csvfile.getvalue().encode('utf-8')

        blob_helper = BlobHelper()

        blob_helper.blob_service.create_blob_from_bytes(storage_container_name, storage_blob_name, encoded_file, max_connections=1)

        function_end_datetime = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        function_end_date = datetime.today().strftime("%d.%m.%Y")

        report_uri = os.environ["AzureStorageReportUri"]

        mail_helper.send_message(f"Automated feedback report generator completed on {function_end_datetime}. Download at {report_uri}", f"Automated Feedback Report {environment} - {function_end_date} - Completed")

        logging.info(
            f"GenerateReport function finished on {function_end_datetime}"
        )

    except Exception as e:
        logging.error(traceback.format_exc())

        function_fail_datetime = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        function_fail_date = datetime.today().strftime("%d.%m.%Y")

        mail_helper.send_message(f"Automated feedback report generator failed on {function_fail_datetime}", f"Automated Feedback Report {environment} - {function_fail_date} - Failed")

        logging.info(
            f"GenerateReport function failed on {function_fail_datetime}"
        )

        # Raise so Azure sends back the HTTP 500
        raise e
