import os
path=r"/mnt/c/Users/HP/Pictures"
import numpy as np
def get_img_paths(path:str):
    img_paths=[]
    if not os.path.exists(path):
        print(f"Directory {path} does not exist.")
        print(f"current working dir: {os.getcwd()}")
    else:
        for root,dir, files in os.walk(path):
            r=root.removeprefix("/mnt/")
            # self.textbox.setText("checking root dir:")
            # self.textbox.setText(r)
            # print(f"checking root dir: {r}")
            print(f"Checking dir: {dir}")
            img_path=[os.path.abspath(os.path.join(root, file)) for file in files if file.endswith(('.JPG', '.jpg', '.png', '.jpeg'))]
            if img_path:
                img_paths.append(img_path)
                
        if not img_paths:
            print("no valid img file found, make sure img format is .png, .jpg, .jpeg")
    return img_paths
paths = get_img_paths(path=path)
paths = np.array(paths).flatten()
"""
from itertools import chain

def flatten(matrix):
    return list(chain.from_iterable(matrix))

Or a loop to return a concatenated list of sublists"""
print(paths)