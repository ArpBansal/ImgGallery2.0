import faiss
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
            lim, d, i = index.range_search(rep['embedding'], radius=1.3)
            sorted_indices = argsort(d)
            # d_sort = d[sorted_indices]
            i_sort = i[sorted_indices]
            return i_sort

def group_find(img_path:str):
    indexes=[]
    index = faiss.read_index()
    rep = represent(img_path)
    for r in rep:
        lim, d, i = index.range_search()
        sorted_indices = argsort(d)
        i_sort = i[sorted_indices]
        indexes.append(i_sort)

    return indexes

