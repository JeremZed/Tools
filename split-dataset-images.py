'''
Script python qui permet de dispatcher le jeu d'images dans un dossier train, un dossier validate, et un dossier test par classe
    --dir=      : Représente le path du dossier où sont stockés les images à dispatcher
    --dest=     : Représente le path du dossier de destination
    --ratio     : Représente le quota pour chaque dossier
    --limit     : Représente le nombre limite d'image à copier

> python split-dataset-images.py --dir=<path-to-directory> --dest=<path-to-directory> --ratio=0.8,0.15,0.05 --limit=1000

'''

#########################################################################################
#   Imports
#########################################################################################

import argparse
import os
import random
import numpy as np
import pandas as pd
import shutil
import progressbar

#########################################################################################
#   Fonctions
#########################################################################################

# random.seed(10)

parser = argparse.ArgumentParser()

parser.add_argument("--dir", help="Dossier source des images à dispatcher.")
parser.add_argument("--dest", help="Dossier de destination où copier les images.")
parser.add_argument("--ratio", help="Quota attribué pour chaque dataset (train, validation, test).")
parser.add_argument("--limit", help="Nombre limite d'image à copier.")

args=parser.parse_args()

#########################################################################################
#   Initialisation des variables
#########################################################################################

source = '.'
dest = '.'
ratio = (0.8,0.15,0.15)
limit = -1

DIR_TRAIN = 'train'
DIR_VALIDATION = 'validation'
DIR_TEST = 'test'

#########################################################################################
#   Contrôle des arguments
#########################################################################################

if args.dir is not None:
    if os.path.exists( args.dir ) and os.path.isdir(args.dir):
        source = args.dir
    else:
        exit("Dossier source erroné.")

if args.dest is not None:
    if os.path.exists( args.dest ) and os.path.isdir(args.dest):
        dest = args.dest
    else:
        exit("Dossier de destination erroné.")

if args.ratio is not None:
    t = np.array(args.ratio.split(','))
    if len(t) == 3:
        try:
            ratio = tuple(np.asarray(t, dtype=float))
        except:
            print(t)
            exit('Ratio erroné.')

    else:
        exit("Le quota doit comporter 3 ratio. Ex: 0.8,0.15,0.15")

if args.limit is not None:
    try:
        limit = abs(int(args.limit))
    except:
        exit("La limite est erronée.")


#########################################################################################
#   Récupération des classes et de la valeur limite d'image à traiter
#   pour que toutes les classes possèdent le même nombre d'images
#########################################################################################

classes = sorted(os.listdir(source))
folders = []

for c in classes:

    _path = os.path.join(source, c)

    if os.path.exists( _path ) and os.path.isdir( _path ):

        images = os.listdir(_path)
        images_count = len(images)

        folders.append({ 'classe' : c, 'count' : images_count, 'path' : _path })

df = pd.DataFrame(folders)

class_min_idx = df['count'].argmin()
count_image_min = df.iloc[class_min_idx, :]['count']

limit_images = count_image_min if limit == -1 else limit

#########################################################################################
#   Création des répertoires d'entraînement, de validation et de test
#########################################################################################

directories_data = [os.path.join(dest, DIR_TRAIN), os.path.join(dest, DIR_VALIDATION), os.path.join(dest, DIR_TEST)]
path_dir_train, path_dir_validation, path_dir_test = directories_data

for d in directories_data:
    if os.path.exists( d ) == False:
        os.mkdir(d)

#########################################################################################
#   Traitement des images par classe
#########################################################################################

for idx, row in df.iterrows():

    # Création du dossier de la classe pour chaque étape (train, validation, test)
    path_train_classe = os.path.join(path_dir_train, str(idx))
    path_validation_classe = os.path.join(path_dir_validation, str(idx))
    path_test_classe = os.path.join(path_dir_test, str(idx))

    if os.path.exists( path_train_classe ) == False:
        os.mkdir(path_train_classe)

    if os.path.exists( path_validation_classe ) == False:
        os.mkdir(path_validation_classe)

    if os.path.exists( path_test_classe ) == False:
        os.mkdir(path_test_classe)


    # Récupération de la liste des images
    images = os.listdir(row['path'])
    random.shuffle(images)

    # On limite la liste d'images
    images = images[:limit_images]

    # On attribue le nombre d'images par catégorie
    size_train = int(len(images) * ratio[0])
    size_validation = int(len(images) * ratio[1])
    size_test = int(len(images) * ratio[2])

    print(f"\n[*] Classe  : {row['classe']} \n"
          f"Images : {len(images)} ( {row['count']} ) \n"
          f"Nb train: {size_train} - Nb validation : {size_validation} - Nb test :{size_test}\n")

    # On copie les images de la classe dans les bons répertoire
    for i in progressbar.progressbar( np.arange(0, len(images)) ) :
        if i < size_train:
            dest_folder = path_train_classe
        elif i < size_train + size_validation:
            dest_folder = path_validation_classe
        else:
            dest_folder = path_test_classe

        shutil.copy(os.path.join(row['path'], images[i]), os.path.join(dest_folder, images[i]))


# Création du fichier de correspondance des labels
df.to_csv( os.path.join(dest, 'labels.csv'), columns=['classe'] )
