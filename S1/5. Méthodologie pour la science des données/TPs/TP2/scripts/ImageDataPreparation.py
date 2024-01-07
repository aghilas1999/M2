'''
import os
from PIL import Image
import numpy as np
import pandas as pd
import glob

def load_data(folder):
    normal_images = glob.glob(os.path.join(folder, "NORMAL", "*.jpeg"))
    pneumonia_images = glob.glob(os.path.join(folder, "PNEUMONIA", "*.jpeg"))

    image_list = normal_images + pneumonia_images
    labels = ['Normal'] * len(normal_images) + ['Pneumonia'] * len(pneumonia_images)

    return pd.DataFrame({'image': image_list, 'class': labels})

def load_data(img_path):
    img_list = []
    try:
        img = Image.open(img_path)
        # resize image
        img = img.resize((224, 224,3))
        img_list.append(img)
    except Exception as e:
        print(f"Error loading image {img_path}")
    return img_list
'''

from PIL import Image

def load_data(img_path):
    img_list = []  # Initialisez la liste en dehors de la boucle try
    try:
        img = Image.open(img_path)
        # Redimensionnez l'image à la taille souhaitée (224x224)
        img = img.resize((224, 224))
        img_list.append(img)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image {img_path}: {str(e)}")
    return img_list
