import os
import matplotlib.pyplot as plt

def plot_class_distribution(test_folder):
    test_c = os.listdir(test_folder)

    # Initialisez les compteurs pour chaque classe pour le test
    test = {'NORMAL': 0, 'PNEUMONIA': 0}

    # Calculer le nombre d'images pour chaque classe donnée et l'afficher pour savoir si c'est NORMAL ou PNEUMONIA
    for classN in test_c:
        class_f = os.path.join(test_folder, classN)
        image_f = os.listdir(class_f)

        if classN == 'NORMAL':
            test['NORMAL'] += len(image_f)
        elif classN == 'PNEUMONIA':
            test['PNEUMONIA'] += len(image_f)

        print(f'Le nombre d images dans la classe "{classN}" dans le TEST est : {len(image_f)}')

    # Afficher la distribution des classes dans le répertoire de test
    plt.bar(test.keys(), test.values())
    plt.title('La distribution dans la classe TEST')
    plt.show()

test_folder = 'Dataset/chest_xray/test'
plot_class_distribution(test_folder)
