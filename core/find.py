import faiss
import sqlite3
import os
from representation import represent
from numpy import argsort

def find(img_path:str):
    base_index = faiss.IndexFlatL2(512)
    index = faiss.IndexIDMap2(base_index)
    # index.add_with_ids()
    rep = represent(img_path)
    for r in rep:
        if rep['sface']==True:  
            lim, d, i = index.range_search(rep['embedding'], 1.29)
            sorted_indices = argsort(d)
            # d_sort = d[sorted_indices]
            i_sort = i[sorted_indices]
            return i_sort

def group_find(img_path:str, index_path:str, db_path:str):
    try:
        indexes=[]
        common_paths=None
        index = faiss.read_index(index_path)
        rep = represent(img_path)

        for r in rep:
            _, _, i = index.range_search(r['embedding'], 1.29)
            indexes.append(i)


        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for sublist in indexes:
        # Convert sublist to a tuple for the SQL query
            l = sublist.tolist() #sqlite not working properly if converted to tuple directly from numpyArray
            keys_tuple = tuple(l)
        
        
            cursor.execute(f"SELECT path FROM keys_imgs WHERE key IN ({','.join(['?']*len(keys_tuple))})", keys_tuple)
            # rows = cursor.fetchall()
            # print(rows)
            
            
            
            paths = {row[0] for row in cursor.fetchall()}
            
            
            # Initialize common_paths or find intersection with current paths
            if common_paths is None:
                common_paths = paths
            else:
                common_paths &= paths


        return list(common_paths)
    except Exception as e:
        print(e)
        
    finally:
        if conn:
            conn.close()


