import faiss
import numpy as np

from core import representation

from storage import add_keysPath, rm_keysPath, logger

def addVecWithIds(index_path:str, db_path:str, emdeddings):
    try:
        index = faiss.read_index(index_path)
        last_id = faiss.vector_to_array(index.id_map)[-1]
        if len(emdeddings) == 1:
            key=last_id+1
            embedding=np.expand_dims(emdeddings[0], axis=0)
            index.add_with_ids(embedding, key)
            add_keysPath(db_path=db_path)
        else:
            start=last_id+1
            end = start+len(emdeddings)
            index.add_with_ids(np.array(emdeddings, dtype='f'), list(range(start, end)))

    except Exception as e:
        logger.error(e)

    finally:
        if index:
            faiss.write_index(index_path)

def remVecWithIds(index_path:str, db_path:str, ids):
    try:
        index = faiss.read_index(index_path)
        index.remove_ids(np.array(ids, dtype=np.int64))
        rm_keysPath(db_path=db_path, keys=ids)

    except Exception as e:
        logger.error(e)

    finally:
        if index:
            faiss.write_index(index_path)

