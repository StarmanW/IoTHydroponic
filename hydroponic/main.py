import json
import os
from firebase import Firebase
from hydroponic import Hydroponic

# Build file path
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
config = os.path.join(CURRENT_FOLDER, 'config.json')
firebase_config = os.path.join(CURRENT_FOLDER, 'firebase.json')

if __name__ == '__main__':
    with open(config) as json_file:
        config = json.load(json_file)

    firebase = Firebase(firebase_config)
    firebase.run()
    
    hydroponic = Hydroponic(config["hydroponics"][0], firebase)
    hydroponic.run()
    