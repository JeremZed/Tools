import pandas as pd
from sklearn.model_selection import train_test_split

class Preprocessing():
    def __init__(self, project) -> None:
        self.project = project
        self.split_test_size = 0.2

    def applyDictToVariableQuality(self, variables, dictionnary, df ):
        ''' Permet d'appliquer une valeur en fonction d'un dictionnaire de valeur '''
        for col in variables:
            df[col] = df[col].map(dictionnary)

        return df

    def applyDummiesToVariableQuality(self, variables, df):
        ''' Permet d'effectuer un hot-shot sur les variables quantitatives '''
        for col in variables:
            df = df.join(pd.get_dummies(df[col], dtype=int)).drop([col], axis=1)

        return df

    def split(self, dataset):
        ''' Permet de diviser le dataset en une portion pour l'entrainement et une portion pour les tests '''
        trainset, testset = train_test_split(dataset, test_size=self.split_test_size, random_state=self.project.random_state)

        return trainset, testset

    def runPreprocessing(self, custom_fct, *args):
        ''' Permet de lancer les traitements personnalisés sur le dataset passé en paramètre et de retourner la partie X et y '''
        df = custom_fct(*args)

        X = df.drop(self.project.column_target, axis=1)
        y = df[self.project.column_target]

        return X, y

    def run(self, f):
        ''' Permet de lancer la division et le preprocessing sur le dataset du projet '''

        trainset, testset = self.split(self.project.dataset)

        X_train, y_train = self.runPreprocessing( f, self, trainset )
        X_test, y_test = self.runPreprocessing( f, self, testset )

        self.project.modeling.setTrainset(X_train, y_train)
        self.project.modeling.setTestset(X_test, y_test)

        return X_train, X_test, y_train, y_test

