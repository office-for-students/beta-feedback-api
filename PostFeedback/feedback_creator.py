import inspect
import os
import sys

# TODO investigate setting PATH in Azure so can remove this
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path.insert(0, CURRENTDIR)
sys.path.insert(0, PARENTDIR)

from SharedCode import utils


class FeedbackCreator:
    def __init__(self, client, collection_link):
        self.cosmosdb_client = client
        self.collection_link = collection_link

    def write_feedback_to_db(self, feedback_entry):
        self.cosmosdb_client.CreateItem(self.collection_link, feedback_entry)
