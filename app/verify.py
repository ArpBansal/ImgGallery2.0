import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# import tensorflow as tf
# print(tf.__version__)
import warnings
warnings.filterwarnings('ignore')
# import tensorrt
import torch
if torch.cuda.is_available():

    torch.device("cuda")
else:
    torch.device('cpu')
    print("No GPU available. Training will run on CPU.")
from deepface import DeepFace
res = DeepFace.verify("app/IMG_1526.JPG", "app/IMG_1518.JPG", enforce_detection=False, detector_backend='retinaface',
                      model_name='Facenet512')
print(res['verified'])
print(res)
# embed = DeepFace.represent(img_path)
