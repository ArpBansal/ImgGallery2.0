from insightface.app import FaceAnalysis
from cv2 import imread
import pickle
import numpy as np
from ..app import utils

def represent(path:str, ctx_id:int=-1, model:str="antelopev2"):
    embeddings=[]
    sface=False
    img = imread(path)
    app = FaceAnalysis(name=model, providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'])
    app.prepare(ctx_id=ctx_id, det_size=(640, 640), det_thresh=0.4)
    embedding = app.get(img=img)
    t = len(embedding)
    if t == 0:
        return embeddings
    elif t == 1:
        sface=True
        for face in embedding:
            
            embedding = np.expand_dims(face.normed_embedding, axis=0)
            embeddings.append({'path':path, 'embedding':embedding, 'sface':sface})

        return embeddings        
    else:
        for face in embedding: 
            embedding = np.expand_dims(face.normed_embedding, axis=0)
            embeddings.append({'path':path, 'embedding':embedding, 'sface':sface})

        return embeddings


def bulk_embeddings(path:str, ctx_id:int=-1, model:str="antelopev2"):
    img_paths = utils.get_img_paths(path=path)
    sface=True
    representations=[]
    with open("constants.pkl", 'wb') as f:

    app = FaceAnalysis(name=model, providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'])
    app.prepare(ctx_id=ctx_id, det_size=(640, 640), det_thresh=0.4)
    for path in img_paths:
        img = imread(path)
        faces = app.get(img=img)
        if len(faces) == 1:
            sface=True
        for face in faces:

            embedding = face.normed_embedding
            representations.append({'path':path, 'embedding':embedding, 'sface':sface, 'key':key})

    return representations

