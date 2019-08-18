import json
import pyrebase
import time

# Firebase class


class Firebase():
    def __init__(self, config_file_dir):
        self.config_file_dir = config_file_dir
        self.config = None
        self.firebase = None
        self.auth = None
        self.user = None
        self.db = None
        self.read_config_file()

    # Read configuration file and initialize
    # firebase configuration.
    def read_config_file(self):
        with open(self.config_file_dir) as json_file:
            self.config = json.load(json_file)
        time.sleep(1)

    # Run firebase initialization steps
    def run(self):
        self.firebase = pyrebase.initialize_app(self.config)
        # Get a reference to the auth service
        self.auth = self.firebase.auth()
        # Login user
        self.user = self.auth.sign_in_with_email_and_password(
            self.config["email"], self.config["password"])
        # Get a reference to the database service
        self.db = self.firebase.database()

    # Push data up to firebase
    def pushData(self, data=None):
        # Pass the user's idToken to the push method
        return self.db.child(self.config["tableName"]).push(data, self.user["idToken"])
