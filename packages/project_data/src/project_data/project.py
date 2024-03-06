import pandas as pd
from project_data.description import Description
from project_data.preprocessing import Preprocessing
from project_data.modeling import Modeling
from project_data.roadmap import Roadmap

from sklearn.model_selection import train_test_split

class Project():
    '''
    Représente le projet datascience.
    C'est à partir de cette classe qu'il est possible de construire les différentes étapes du projet (description, analyse, featuring, modeling...)
    '''
    def __init__(self):
        self.version = "It works!"
        self.dataset = None
        self.dataset_origin = None

        self.description = Description(self)
        self.preprocessing = Preprocessing(self)
        self.modeling = Modeling(self)
        self.roadmap = Roadmap()

        self.column_target = None
        self.random_state = 0

    def loadDataset(self, path, type = 'csv', sep=","):
        ''' Permet charger un dataset via pandas en fonction du type passé en paramètre '''
        if type == "csv":
            self.__loadDatasetCSV(path, sep=sep)
        elif type == "excel":
            self.__loadDatasetExcel(path)
        else:
            pass

    def __loadDatasetCSV(self, path, sep=","):
        ''' Permet de charger le dataset en fonction du chemin du fichier CSV passé en paramètre via pandas'''
        self.dataset = pd.read_csv(path, sep=sep)
        self.dataset_origin = self.dataset.copy()

    def __loadDatasetExcel(self, path):
        ''' Permet de charger le dataset en fonction du chemin du fichier Excel passé en paramètre via pandas'''
        self.dataset = pd.read_excel(path)
        self.dataset_origin = self.dataset.copy()

    def setTarget(self, column_name):
        ''' Permet de définir la colonne "target" de notre dataset '''
        self.column_target = column_name

    def getTarget(self):
        ''' Permet de retourner la colonne target du dataset '''
        return self.dataset[self.column_target]

    def resetDataset(self):
        ''' Permet de reset toutes les modications faites sur le dataset '''
        self.dataset = self.dataset_origin.copy()

    def runPreprocessing(self, custom_fct, *args):
        ''' Permet de diviser le dataset en deux parties. '''

        self.dataset = custom_fct(*args)

        X = self.dataset.drop(self.column_target, axis=1)
        y = self.dataset[self.column_target]

        return X, y

