import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
import numpy as np

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

    def heatmapNanValue(self, cbar=True):
        ''' Permet de produire une image de l'ensemble du dataset pour visualiser les valeurs manquantes '''
        plt.figure(figsize=(20,10))
        plt.title("Représentation des valeurs manquante.")
        sns.heatmap( self.project.dataset.isna(), cbar=cbar )
        plt.show()

    def getRatioMissingValues(self):
        ''' Permet de retourner le ratio de valeur manquante pour chaque variable '''

        # pd.set_option('display.max_row', len(self.project.dataset.columns))

        a = self.project.dataset.isna().sum() / self.project.dataset.shape[0]
        df = pd.DataFrame(a, columns=['ratio'])
        df['sum'] = self.project.dataset.isna().sum()

        return df.sort_values('ratio', ascending=False)

    def getRatioTarget(self):
        ''' Permet de retourner le ratio des différentes classes présente dans la colonne target '''

        a = self.project.dataset[self.project.column_target].value_counts(normalize=True).reset_index()
        b = self.project.dataset[self.project.column_target].value_counts(normalize=False).reset_index()

        df = pd.DataFrame(a)
        df['sum'] = b['count']

        return df.sort_values('proportion', ascending=False)

    def getHistoVariable(self, type='float'):
        ''' Permet d'afficher un graphique de répartition des données en fonction de leur type '''

        if type == 'float' or type == 'int':
            for col in self.project.dataset.select_dtypes(type):
                plt.figure(figsize=(15,8))
                sns.displot(data=self.project.dataset[col], kde=True)
                plt.show()

    def getRatioVariableQuality(self):
        ''' Permet de retourner le ratio des différentes classes présente dans les colonnes de type qualitative '''
        res = []

        for col in self.project.dataset.select_dtypes('object'):
            a = self.project.dataset[col].value_counts(normalize=True).reset_index()
            b = self.project.dataset[col].value_counts(normalize=False).reset_index()

            a['count'] = b['count']

            res.append(a)

        return res

    def getCorrelationPearson(self, variables, target, fillna=False):
        ''' Permet de retourner une vision de corrélation Pearson entre les variables et la target dans le cas variable continue / continue '''
        res = []
        data = self.project.dataset.copy()

        if fillna == True:
            data = data.fillna(0)

        for col in variables:
            p = st.pearsonr(data[col], data[target] )
            res.append( {"name" : col, "statistic" : p[0], "pvalue" : p[1] } )

        df = pd.DataFrame(res).sort_values('statistic')

        return df

    def getCorrelationSpearman(self, variables, target, fillna=False):
        ''' Permet de retourner une vision de corrélation Spearman entre les variables et la target dans le cas variable continue / continue '''
        res = []
        data = self.project.dataset.copy()

        if fillna == True:
            data = data.fillna(0)

        for col in variables:
            p = st.spearmanr(data[col], data[target] )
            res.append( {"name" : col, "statistic" : p[0], "pvalue" : p[1] } )

        df = pd.DataFrame(res).sort_values('statistic')

        return df

    def getHistoVariableToTarget(self, variables, target):
        ''' Permet de générer les histogrammes de chaque colonne par rapport à la target '''

        for col in variables:
            plt.figure()

            sns.histplot(self.project.dataset[col], label=col, kde=True, stat="density")
            sns.histplot(self.project.dataset[target], label=target, kde=True, stat="density")
            plt.legend()

            plt.pause(0.001)

        plt.show(block=True)

    def showCrossTab(self, variables, target):
        ''' Permet de visualiser la crosstab de pandas en fonctions des variables qualitatives '''
        for col in variables:
            print( pd.crosstab(self.project.dataset[target], self.project.dataset[col]) )


    def getHeatCrossTab(self, variables, target):
        ''' Permet de visualiser une heatmap des crosstab des variables qualitatives '''
        for col in variables:
            plt.figure()
            sns.heatmap( pd.crosstab(self.project.dataset[target], self.project.dataset[col]), annot=True, fmt="d" )
            plt.pause(0.001)

        plt.show(block=True)

    def getHeatCorrelation(self, variables, cluster=False):
        ''' Permet d'afficher une heatmap des corrélations entre variables continue '''
        # plt.figure(figsize=(15,8))
        sns.heatmap(self.project.dataset[ variables ].corr(), annot=True)
        if cluster == True:
            sns.clustermap(self.project.dataset[ variables ].corr(), annot=True)

    def getClassesInfos(self, data, column_x, column_y, size=5):
        ''' Permet de retourner un aggréga d'information par tranches '''

        classes = []
        tranches = np.arange(0, max(data[column_x]), size, dtype=int )
        indices = np.digitize(data[column_x], tranches)

        for i, tranche in enumerate(tranches):
            values = data.loc[ indices == i, column_y ]
            if len(values) > 0:
                c = {
                    'valeurs' : values,
                    'centre_classe' : tranche,
                    'taille' : len(values),
                    'quartiles' : [np.percentile(values, p) for p in [25,50,75]],
                    'mean' : values.mean(),
                    'mean_square' : values.mean()**2,
                    'median' : values.median(),
                    'median_square' : values.median()**2,
                    'max' : values.max(),
                    'min' : values.min()
                }
                classes.append(c)

        return pd.DataFrame(classes)

    def showTimelineClassesVariables(self, data, variables_y, variable_x, size=5, x_indicator="centre_classe", y_indicator="median"):
        ''' Permet de retourner les courbes des informations issu de getClassesInfos, exemple pour une serie temporelle on souhaite regrouper
        les jours en paquet de 30 jours au lieu d'afficher  jour apres jour '''
        for c in variables_y:
            i = self.getClassesInfos(data, variable_x, c, size)
            sns.lineplot(data=i, x=x_indicator, y=y_indicator, label=c)
        plt.show()

