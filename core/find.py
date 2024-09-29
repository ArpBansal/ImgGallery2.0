import faiss
import sqlite3
import os
import sys
import torch
import mobileclip

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from core import representation
from numpy import argsort

def find(img_path:str):
    """ Only pass photo of single face\n
    finding single face in the photo
    return sorted list based on ascending order of distance"""
    base_index = faiss.IndexFlatL2(512)
    index = faiss.IndexIDMap2(base_index)
    rep = representation.represent(img_path)
    
    for r in rep:
        if rep['sface']==True:  
            lim, d, i = index.range_search(rep['embedding'], 1.29)
            sorted_indices = argsort(d)
            # d_sort = d[sorted_indices]
            i_sort = i[sorted_indices]
            return i_sort

def group_find(img_path:str, index_path:str, db_path:str):
    """ can be used for finding similar faces in a photo, taking more than one faces
    can be used for one face too."""
    try:
        indexes=[]
        common_paths=None
        index = faiss.read_index(index_path)
        rep = representation.represent(img_path)

        # update this as range_search may also work for embeddings in batches, may no need for a loop here
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
        return None


def find_clip(index_path:str, query:str, img_path:str):
    try:
        index = faiss.read_index(index_path)
        model, _, _ = mobileclip.create_model_and_transforms('mobileclip_b', pretrained="../../local_dir/mobileClipB/mobileclip_b.pt") # change path to script
        tokenizer = mobileclip.get_tokenizer("mobileclip_b")
        tokens = tokenizer([query])
        with torch.no_grad():
            text_feature = model.encode_text(tokens)
            text_feature /= text_feature.norm(dim=-1, keepdim=True)
            text_feature = text_feature.cpu().numpy()


        _, d, i = index.range_search(text_feature, 0.18)
        sorted_indices = argsort(d)

        return i[sorted_indices] # modify it returning paths i.e. adding with db    
    except Exception as e:
        print(f"error ({e}) couldn't find and return image")
        
    finally:
        return None