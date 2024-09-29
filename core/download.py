from huggingface_hub import snapshot_download
import os
import sqlite3
from logger import logger
def model_download(root:str):
    try:
        path=root+'Gallery/models'
        if not os.path.exits(path):
            os.makedirs(path)
        snapshot_download(repo_id='Arpit-Bansal/insightface_models', local_dir=path)

    except Exception as e:
        logger.error(e)


conn=sqlite3.connect()
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS dirTracked (
dir TEXT UNIQUE)''')


