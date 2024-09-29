
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))
from insightface.app import FaceAnalysis
from cv2 import imread
import numpy as np
from app import utils
import mobileclip
import torch
from PIL import Image
import os

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
            embedding = np.expand_dims  (face.normed_embedding, axis=0)
            embeddings.append({'path':path, 'embedding':embedding, 'sface':sface})

        return embeddings


def bulk_embeddings(path:str, ctx_id:int=-1, model:str="antelopev2"):
    img_paths = utils.get_img_metadata(path=path)
    sface=False
    representations=[]
    

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

def bulk_embeddings_clip(path:str):
    img_paths = utils.get_img_metadata(path=path, onlyPath=True)
    representations=[]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pretrained_model_path = os.path.join(script_dir, 'local_dir', 'mobileClipB', 'mobileclip_b.pt')
    model, _, preprocess = mobileclip.create_model_and_transforms('mobileclip_b', pretrained=pretrained_model_path)
    tokenizer = mobileclip.get_tokenizer('mobileclip_b')
    for path in img_paths:
        image = preprocess(Image.open(path).convert('RGB')).unsqueeze(0)
        with torch.no_grad():
            image_features = model.encode_image(image)
            image_features /= image_features.norm(dim=-1, keepdim=True)
        image_features_np = image_features.cpu().numpy()
        representations.append(image_features_np)

    return representations