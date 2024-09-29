# from PIL import Image
# import requests
# from huggingface_hub import snapshot_download
# from transformers import AutoProcessor, AutoModel
# import torch, os

# # snapshot_download(repo_id="google/siglip-so400m-patch14-384", local_dir="../../cache_dir")

# model = AutoModel.from_pretrained("google/siglip-so400m-patch14-384", cache_dir="../../cache_dir")
# processor = AutoProcessor.from_pretrained("google/siglip-so400m-patch14-384", cache_dir="../../cache_dir")
# if os.path.isdir("../../cache_dir"):
#     print(True)
    
# image = Image.open("app/IMG_1500.JPG")
# resized_img = image.resize((384, 384))

# texts = ["a photo of 2 cats", "a photo of 2 dogs", "a photo of humans", "a photo of trees"]
# inputs = processor(text=texts, images=image, padding="max_length", return_tensors="pt")

# with torch.no_grad():
#     outputs = model(**inputs)

# logits_per_image = outputs.logits_per_image
# probs = torch.sigmoid(logits_per_image) # these are the probabilities
# for i in range(len(texts)):
#     print(f"{probs[0][i]:.1%} that image 0 is '{texts[i]}'")


import torch
from PIL import Image
import mobileclip
import faiss
import numpy as np

# image_cv = imread("./testing_imgs/image.png")
# image_cv = torch.tensor(image_cv).unsqueeze(0)
# image_cv = model.encode_image(image_cv)
# image_cv /= image_cv.norm(dim=-1, keepdim=True)
# text_probs_cv = (100.0 * image_cv @ text_features.T).softmax(dim=-1)

model, _, preprocess = mobileclip.create_model_and_transforms('mobileclip_b', pretrained='./local_dir/mobileClipB/mobileclip_b.pt')
tokenizer = mobileclip.get_tokenizer('mobileclip_b')

image_pil = preprocess(Image.open("./testing_imgs/image.png").convert('RGB')).unsqueeze(0)
text = tokenizer(["diagram"])

with torch.no_grad(), torch.cuda.amp.autocast():
    image_features_pil = model.encode_image(image_pil)
    text_features = model.encode_text(text)
    image_features_pil /= image_features_pil.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    
    # Alternative way to calculate distance using cosine similarity
    cosine_similarity = torch.nn.functional.cosine_similarity(image_features_pil, text_features)
    print("Cosine similarity between text_features and image_features:", cosine_similarity)
    distance = torch.cdist(image_features_pil, text_features, p=2)
    print("Distance between text_features and image_features:", distance)
    
    text_probs_pil = (100.0 * image_features_pil @ text_features.T).softmax(dim=-1)

print(f"img {image_features_pil.shape}, \ntype text {text_features.shape}")

print("PIL Label probs:", text_probs_pil)
print("PIL Label probs:", text_probs_pil[0].argmax())

# '''TODO check the below code later on'''
# Convert the image and text features to numpy arrays
image_features_np = image_features_pil.cpu().numpy()
text_features_np = text_features.cpu().numpy()
print(f"imgnp {image_features_np.shape}, \ntype textnp {text_features_np.shape}")


# Create a FAISS index
dimension = image_features_np.shape[1]
print(dimension)

# base_index = faiss.IndexFlatL2(dimension)
# index = faiss.IndexIDMap2(base_index)

# ids =np.arange(n)
# # Add image features to the index
# index.add_with_ids(image_features_np, ids)

# # Save the index to a file
# faiss.write_index(index, 'image_features.index')

# # To add text features to the index, you can create another index or use the same one
# text_index = faiss.IndexFlatL2(dimension)
# text_index.add(text_features_np)
# faiss.write_index(text_index, 'text_features.index')

def search_index(query, index_path='image_features.index', model=model, tokenizer=tokenizer, preprocess=preprocess):
    # Tokenize and preprocess the query
    text = tokenizer([query])
    
    # Encode the query text
    with torch.no_grad(), torch.cuda.amp.autocast():
        text_features = model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)
    
    # Convert text features to numpy array
    text_features_np = text_features.cpu().numpy()
    
    # Load the FAISS index
    index = faiss.read_index(index_path)
    
    # Search the index
    distances, indices = index.search(text_features_np, k=5)  # k is the number of nearest neighbors to return
    
    return distances, indices

# Example usage
# query = "a photo of a cat"
# distances, indices = search_index(query)
# print(f"Distances: {distances}")
# print(f"Indices: {indices}")