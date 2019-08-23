import json
import os
from firebase import Firebase
from hydroponic import Hydroponic
from multiprocessing import Process

# Setup firebase
# Build file path
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
config = os.path.join(CURRENT_FOLDER, 'config.json')
firebase_config = os.path.join(CURRENT_FOLDER, 'firebase.json')
firebase = Firebase(firebase_config)
firebase.run()

if __name__ == '__main__':
    with open(config) as json_file:
        config = json.load(json_file)

    hydroponics = {}
    processes = {}
    for i in range(len(config["hydroponics"])):
        hydroponics[i] = Hydroponic(config["hydroponics"][i], firebase)
        processes[i] = Process(target=hydroponics[i].run)
        processes[i].start()
        
    for p in processes:
        p.join()