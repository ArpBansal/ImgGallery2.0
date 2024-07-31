import json
import pickle
import pandas as pd

# opens the pickle file
with open('pathsRetrieval.pkl', 'rb') as input_file:
    # loads the pickle file into a pandas DataFrame
    data = pd.read_pickle(input_file)

    with open('embedings.json', 'w') as f:
        json.dump(data, f)

