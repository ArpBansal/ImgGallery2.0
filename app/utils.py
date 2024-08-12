import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# path=r"/mnt/c/Users/HP/Pictures/Camera Roll"
import numpy as np
from datetime import datetime
# from typing import Optional
def get_img_metadata(path:str):
    img_metadata=[]
    if not os.path.exists(path):
        print(f"Directory {path} does not exist.")
        print(f"current working dir: {os.getcwd()}")
    else:
        for root,dir, files in os.walk(path):
            # self.textbox.setText("checking root dir:")
            # self.textbox.setText(r)
            print(f"checking root dir: {root}")
            print(f"Checking dir: {dir}")
            
            # for file in files:
            #     if file.lower().endswith(('jpg', 'jpeg', 'png')):
            #             pass
            
            img_path=[(os.path.abspath(os.path.join(root, file)),datetime.fromtimestamp(
                os.path.getmtime(os.path.join(root, file)))
            ) for file in files if file.lower().endswith(('jpg', 'jpeg', 'png'))]
            if img_path:
                img_metadata.extend(img_path)
                
        if not img_metadata:
            print("no valid img file found, make sure img format is .png, .jpg, .jpeg")
    return img_metadata



# detector_backend = 'retinaface'
# from deepface import DeepFace
# from label_paths import add_pkl_file, retrieve_imgList
# def img_find(img_path:str, db_path:str, label:str):
#     paths = retrieve_imgList(identity=label)
#     if paths is not None:
#         return paths
#     else:
#         img_path = repr(os.path.abspath(img_path))[1:-1]
#         db_path = repr(os.path.abspath(db_path))[1:-1]
#         dfs=DeepFace.find(
#             img_path=img_path,
#             db_path=db_path,
#             detector_backend=detector_backend,
#             model_name="Facenet512",
#             enforce_detection=False
#         )
#         paths = dfs[0]['identity']
#         add_pkl_file(label=label, img_paths=list(paths))

#         return paths
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ImageChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.added_image_paths = []
        self.deleted_image_paths = []

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Image file created: {event.src_path}")
            self.added_image_paths.append(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Image file deleted: {event.src_path}")
            self.deleted_image_paths.append(event.src_path)

def track_image_changes(directory, refresh:bool=False, db_embed:str=None, track:bool=True):
    event_handler = ImageChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=True)
    observer.start()

    try:
        while track:
            print(event_handler.added_image_paths) 
            print(event_handler.deleted_image_paths)
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    return event_handler.added_image_paths, event_handler.deleted_image_paths

def remove_duplicates(input_list):
    return list(dict.fromkeys(input_list))


