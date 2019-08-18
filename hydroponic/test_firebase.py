from firebase import Firebase
import datetime, json, time, os

# Build file path
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(CURRENT_FOLDER, 'firebase.json')

# Create firebase instance
firebase = Firebase(config_file)
firebase.run()

# Insert 20 sample data
for i in range(0, 20):
    firebase.pushData({
        "pHValue": 6.25,
        "timestamp": json.dumps(datetime.datetime.now(), default=str)
    })
    time.sleep(1)