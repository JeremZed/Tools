import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class Description():
    ''' A pour rôle de réunir un ensemble d'outils pour effectuer une description du dataset '''
    def __init__(self, project):
        self.project = project

    def getCountRowColumns(self):
        ''' Permet de retourner le nombre de ligne et de colonne du dataset '''
        s = self.project.dataset.shape
        return { 'rows' : s[0], 'columns' : s[1] }

    def getTypesVariables(self, type="all"):
        ''' Permet de retourner les types des variables du dataset '''
        if type == "count":
            return self.project.dataset.dtypes.value_counts()
        else:
            return self.project.dataset.dtypes

    def heatmapNanValue(self):
        ''' Permet de produire une image de l'ensemble du dataset pour visualiser les valeurs manquantes '''
        plt.figure(figsize=(20,10))
        plt.title("Représentation des valeurs manquante.")
        sns.heatmap( self.project.dataset.isna(), cbar=True )
        plt.show()

    def getRatioMissingValues(self):
        ''' Permet de retourner le ratio de valeur manquante pour chaque variable '''

        pd.set_option('display.max_row', len(self.project.dataset.columns))

        a = self.project.dataset.isna().sum() / self.project.dataset.shape[0]
        df = pd.DataFrame(a, columns=['ratio'])
        df['sum'] = self.project.dataset.isna().sum()

        return df.sort_values('ratio', ascending=False)

    def getRatioTarget(self):
        ''' Permet de retourner le ratio des différentes classes présente dans la colonne target '''

        a = self.project.column_target.value_counts(normalize=True).reset_index()
        b = self.project.column_target.value_counts(normalize=False).reset_index()

        df = pd.DataFrame(a)
        df['sum'] = b['count']

        return df.sort_values('proportion', ascending=False)


