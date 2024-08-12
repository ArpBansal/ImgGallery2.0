import sqlite3
from typing import List
import logging
import os
import numpy as np
from platform import system
if system() == "Windows":
    dir_path=r"C:\gallery_2.0\data"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        path = r"C:\gallery_2.0\data\test.db"
    
else :
    dir_path=r"/mnt/c/gallery_2.0/data"
    if not os.path.exists(dir_path):
        os.makedirs()
        path = r"/mnt/c/gallery_2.0/data/test.db"

logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger()


def insert_data(name, img_paths:List[str]):
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS face_image_lists (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            img_paths TEXT NOT NULL
        )
        ''')
        img_path_str = ','.join(img_paths)
        cursor.execute('''
        INSERT INTO face_image_lists (name, img_paths)
        VALUES (?, ?)''', (name, img_path_str)
        )

    except Exception as e:
        logger.error(e)

    finally:
        if conn:
            conn.close()
        
def update_data(name:str, add_imgs, subtract_imgs):
    pass


    
def retrieve_imgs(name):
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT img_paths FROM face_images_lists WHERE name = ?''', (name))
        result = cursor.fetchone()[0].split(',')
        return result
    except Exception as e:
        logger.error(e)

    finally:
        if conn:
            conn.close()


def retrieve_keys2path(db_path, keys):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = f"SELECT DISTINCT path FROM keys_imgs WHERE key IN ({','.join(['?']*len(keys))})"
        cursor.execute(query, keys)
        paths = cursor.fetchall()
        unique_paths = [path[0] for path in paths]
        return unique_paths

    except Exception as e:
        logger.error(e)
        return []

    finally:
        if conn:
            conn.close()

def add_keysPath(db_path, keys, paths):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys_imgs (
        key INTEGER PRIMARY KEY,
        path TEXT NOT NULL)
        ''')
        if len(keys) != len(paths):
            raise ValueError("The length of keys and paths lists must be the same.")
        
        entries = list(zip(keys, paths))
        cursor.executemany('INSERT INTO keys_imgs (key, path) VALUES (?, ?)', entries)
        conn.commit()

    except Exception as e:
        logger.error(e)

    finally:
        if conn:
            conn.close()

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS image_indexing (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        path TEXT
    )
""")

cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON image_indexing (timestamp)")
conn.commit()
conn.close()

# os.makedirs(path)

# conn.close()

# path = r"/mnt/c"

# # Get the status of the file
# status = os.stat(path)
# os.access()
# # Extract the permission bits
# permissions = oct(status.st_mode)[-3:]

# print(f"Permissions: {permissions}")
