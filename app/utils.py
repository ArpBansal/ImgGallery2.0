import os
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
from datetime import datetime
from pathlib import Path

from core.logger import logger

def get_img_metadata(path:str, onlyPath:bool):
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
            
            
            img_path=[(os.path.abspath(os.path.join(root, file)),datetime.fromtimestamp(
                os.path.getmtime(os.path.join(root, file)))
            ) for file in files if file.lower().endswith(('jpg', 'jpeg', 'png'))]
            if img_path:
                img_metadata.extend(str(img_path))
                
        if not img_metadata:
            print("no valid img file found, make sure img format is .png, .jpg, .jpeg")
    return img_metadata



# img_path = repr(os.path.abspath(img_path))[1:-1]

#         paths = dfs[0]['identity']
#         add_pkl_file(label=label, img_paths=list(paths))

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

def remove_duplicates(input_list): # maintain the order of elements
    return list(dict.fromkeys(input_list))


from core import storage
def ImgsToProcess(dir:str, db:str):
    try:
        p_set=get_parent_dirs(dir)
        old_dirs = storage.RETdirTracked(db)
        if old_dirs:
            pset&=old_dirs
            if pset:
                paths ={path for path,_ in get_img_metadata(path=dir)}

    except Exception as e:
        logger.error(e)

'''REPLACEMENT for PosixPath.parents method'''

def get_parent_dirs(path:str):
  """Returns a set of all parent directories of the given path."""
  parent_dirs = set()
  while True:
    parent_dir = os.path.dirname(path)
    if parent_dir == path:
      break
    parent_dirs.add(parent_dir)
    path = parent_dir
  return parent_dirs

def get_sub_dirs(path:str):
    subdirs=set()
    for _, dirs, _ in os.walk(top=path):
        subdirs.add(dirs)

    return subdirs

def scirpt_dir():
    return os.path.dirname(os.path.abspath(__file__))

