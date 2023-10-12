import cv2
import numpy as np
from sklearn import preprocessing

class ImageDataPreprocessing:
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size

    def preprocess_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.resize(image, self.target_size)
        image = image / 255.0  
        return image

    def preprocess_data(self, image_paths, labels):
        X = np.array([self.preprocess_image(img_path) for img_path in image_paths])
        y = labels
        return X, y

# Exemple d'utilisation de la classe
preprocessor = ImageDataPreprocessing(target_size=(224, 224))

X_train, y_train = preprocessor.preprocess_data(df_train['image'], df_train['class'])
X_test, y_test = preprocessor.preprocess_data(df_test['image'], df_test['class'])
X_val, y_val = preprocessor.preprocess_data(df_val['image'], df_val['class'])
