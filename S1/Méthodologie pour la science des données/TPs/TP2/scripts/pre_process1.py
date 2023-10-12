import numpy as np
import cv2
'''
def pre_process(images, labels):
    train = np.empty((len(images), 128, 128))
    for i, image in enumerate(images):
        l = [value / 255.0 for value in image.convert('L').getdata()]
        for j in range (128):
            for k in range (128):
                train[i][j][k] = l[j*128+k]

    return train, np.array(labels)
    '''



def preprocess_image(image_path):
    image = cv2.imread(image_path)
    target_size = (224, 224,3)  # Spécifiez la taille cible de l'image
    image = cv2.resize(image, target_size)  # Utilisez la taille cible pour redimensionner l'image
    image = image / 255.0  # Normalisez l'image
    return image
