import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Implements the REST API endpoint for posting a feedback document.

    The endpoint implemented is:
        /feedback

    The API is documented in a swagger document.
    """

    try:
        logging.info("Process a request for an institution resource.")
        logging.info(f"url: {req.url}")
        logging.info(f"params: {req.params}")
        logging.info(f"route_params: {req.route_params}")

        # Put all the parameters together
        params = dict(req.route_params)
        version = req.params.get("version", "1")
        params["version"] = version

        # TODO validate post request (check body has relevant parameters, you will need to check for sql injection)

        # TODO Create Feedback document

        # TODO Store document in feedback collection in cosmos db

        # TODO Return success/failure response
        

    except Exception as e:
        logging.error(traceback.format_exc())

        # Raise so Azure sends back the HTTP 500
        raise e
    