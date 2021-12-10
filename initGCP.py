from google.cloud import firestore
from google.cloud import storage
class InitGCP:
    def initDB():
        # Explicitly use service account credentials by specifying the private key
        # file.
        firestore_client = firestore.Client.from_service_account_json(
            "<YOUR_ACCOUNT_FILE>.json"
        )


        return firestore_client



    def initStorage():

        # Explicitly use service account credentials by specifying the private key
        # file.
        storage_client = storage.Client.from_service_account_json(
            "<YOUR_ACCOUNT_FILE>.json"
        )

        return storage_client

    

   
