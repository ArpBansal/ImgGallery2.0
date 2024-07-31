import pickle
import os
import time

path = f"pathsRetrieval.pkl"

def add_pkl_file(label:str, img_paths, path="pathsRetrieval.pkl"):

    data = {"identity":label,
            "paths":img_paths}
    if not os.path.exists(path):
        with open(path, "wb") as f:
            pickle.dump([], f)

    with open(path, "rb") as f:
        existing_data = pickle.load(f)

    existing_data.append(data)
    with open(path, "wb") as f:
        pickle.dump(existing_data, f)

    # del existing_data
# for r in data:
    # r['identity'] == f"label"
    # return r['paths']
    
    
# add_pkl_file("mikasa", ['sexy', 'jpg', 'png'])
# with open(path, "rb") as f:
#     rep = pickle.load(f)
# print(rep)

# data = [{
#     "identity":'arjun',
#     'path':repr('im\ngz/g')[1:-1]
# },
# {"identity":"nama",
#  'path':('im\ngz/g'}]
# with open(path, "wb") as f:
#     pickle.dump(data, f)


# retrieve from the database, that is pickle file
def retrieve_imgList(identity:str):
    with open(path, "rb") as f:
        rep = pickle.load(f)
        
    for r in rep:
        if r["identity"] == identity:
            return r["paths"]


