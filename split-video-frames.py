'''
Script python qui permet de découper une découper une vidéo en x images
- Soit directement à partir d'une video
- Soit directement à partir d'un répertoire contenant les videos

    Argmuments :
        --dir       : Représente le dossier source où récupérer les vidéos
        --file      : Représente le fichier à découper
        --interval  : Représente l'interval de temps en seconde entre chaque découpage
        --dest      : Représente le dossier de destination où enregistrer les images

> python split-video-frames.py --dir=<path-to-directory> --file=<path-to-file> --interval=1 --dest=<path-to-directory>

'''

#########################################################################################
#   Imports
#########################################################################################

import cv2
import argparse, os
import mimetypes
import progressbar
import numpy as np
import math

#########################################################################################
#   Fonctions
#########################################################################################

def create_directory(base, filename):
    '''
        Créer un dossier au nom du fichier
        Si le dossier existe déjà alors on incrémente une valeur au dossier
    '''

    dirname_destination = os.path.join(base, filename + ".frames")

    if os.path.exists(dirname_destination) == False:
        os.mkdir(dirname_destination)
    else:
        i = 1
        while True:
            dirname_destination = os.path.join(base, filename + ".frames-" + str(i))

            if os.path.exists(dirname_destination) == False:
                os.mkdir(dirname_destination)
                break
            else:
                i += 1

    print(f"[*] Création du dossier : {dirname_destination} : OK.\n")

    return dirname_destination

def split_video(path_file_video, dir_destination, interval=1):
    ''' Permet de sectionner la vidéo en x images '''

    video = cv2.VideoCapture(path_file_video)

    count = 0
    video_length = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    fps = int(video.get(cv2.CAP_PROP_FPS))

    print(f"Nom de la video : {path_file_video}\n"
            f"Nombre total d'image : {video_length}\n"
            f"Image par seconde (fps) : {fps}\n"
            f"Intervalle en seconde: {interval}\n")

    # Effet visuel de la progressar
    for i in progressbar.progressbar( np.arange(0, video_length) ) :

        success, frame = video.read()

        if success:
            if math.floor(i % (fps * interval)) == 0:
                cv2.imwrite(f'{dir_destination}/frame_{count}.jpg', frame)
                count += 1
        else:
            break

    video.release()

    print(f"[*] {count} images créées dans le dossier {dir_destination}.\n")


parser = argparse.ArgumentParser()

parser.add_argument("--dir", help="Dossier source des vidéos à découper.")
parser.add_argument("--file", help="Fichier vidéo à découper.")
parser.add_argument("--interval", help="Interval de temps en seconde entre chaque image.")
parser.add_argument("--dest", help="Dossier de destination.")

args=parser.parse_args()

#########################################################################################
#   Initialisation des variables
#########################################################################################
MODE_DIR = 'dir'
MODE_FILE = 'file'

mode = MODE_FILE
path = '.'
interval = 1
dest = '.'

#########################################################################################
#   Contrôle des arguments
#########################################################################################

if args.dir is not None:
    if os.path.exists( args.dir ) and os.path.isdir(args.dir):
        mode = MODE_DIR
        path = args.dir
    else:
        exit("Dossier source erroné.")

if args.file is not None:
    if os.path.exists( args.file ) and os.path.isfile(args.file):
        mode = MODE_FILE
        path = args.file
    else:
        exit("Fichier source erroné.")

if args.interval is not None:
    try:
        interval = float(args.interval)

        if interval < 0:
            interval = 1
    except:
        pass

if args.dest is not None:
    if os.path.exists( args.dest ) and os.path.isdir(args.dest):
        dest = args.dest
    else:
        exit("Dossier de destination erroné.")

#########################################################################################
#   Mode Dossier
#########################################################################################

if mode == MODE_DIR:

    videos = []

    # On liste les fichiers du chemin passé en paramètre
    items = os.listdir(path)
    for i in items:
        item_path = os.path.join(path, i)

        # Si le path correspond bien à un fichier
        if os.path.isfile(item_path):
            _mimetype = mimetypes.guess_type(item_path)

            # Si ce fichier possède un mimetype video
            if _mimetype[0] is not None and _mimetype[0][:5] == 'video':
                videos.append(item_path)

    # On lance le traitement pour toutes les videos trouvés
    for v in videos:
        filename = os.path.basename(v).split('/')[-1]
        dirpath = create_directory(dest, filename)

        split_video(v, dirpath)


#########################################################################################
#   Mode Fichier
#########################################################################################

else :

    _mimetype = mimetypes.guess_type(path)
    # Si ce fichier possède un mimetype video
    if _mimetype[0] is not None and _mimetype[0][:5] == 'video':

        filename = os.path.basename(path).split('/')[-1]
        dirpath = create_directory(dest, filename)

        split_video(path, dirpath, interval=interval)

    else:
        print(f"[*] {path} ,'est pas une vidéo.\n")