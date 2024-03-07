import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

from sklearn.model_selection import learning_curve, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score, precision_score
from scipy.stats import spearmanr, pearsonr

class _DecisionTreeRegressor(DecisionTreeRegressor):
    pass

class _LinearRegression(LinearRegression):
    pass

class _RandomForestRegressor(RandomForestRegressor):
    pass

class _AdaBoostRegressor(AdaBoostRegressor):
    pass

class _SVR(SVR):
    pass

class _KNeighborsRegressor(KNeighborsRegressor):
    pass

class Modeling():
    def __init__(self, project):
        self.project = project

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        self.models = []
        self.best_models = []

    def resetModels(self):
        ''' Permet de vider la pile des models'''
        self.models = []

    def setTrainset(self, X_train, y_train):
        ''' Permet de setter le trainset '''
        self.X_train = X_train
        self.y_train = y_train

    def setTestset(self, X_test, y_test):
        ''' Permet de setter le testset '''
        self.X_test = X_test
        self.y_test = y_test

    def addModel(self, name, model, hyper_params = {}):
        ''' Permet d'ajouter un model dans la pile '''
        self.models.append({'name' : name, 'model' : model, 'hyperparams' : hyper_params})

    def getFactory(self, name, **kwargs):
        ''' Factory de différent class '''
        model = None

        if name == "DecisionTreeRegressor":
            model = _DecisionTreeRegressor(**kwargs)

        if name == "LinearRegression":
            model = _LinearRegression(**kwargs)

        if name == "RandomForestRegressor":
            model = _RandomForestRegressor(**kwargs)

        if name == "AdaBoostRegressor":
            model = _AdaBoostRegressor(**kwargs)

        if name == "SVR":
            model = _SVR(**kwargs)

        if name == "KNeighborsRegressor":
            model = _KNeighborsRegressor(**kwargs)

        return model

    def evalutionRegressor(self, model):

        model.fit(self.X_train, self.y_train)
        ypred = model.predict(self.X_test)

        mse = mean_squared_error(self.y_test, ypred)
        mae = mean_absolute_error(self.y_test, ypred)
        r2 = r2_score(self.y_test, ypred)
        sp = spearmanr(ypred, self.y_test).correlation
        pe = pearsonr(ypred, self.y_test).correlation
        ex = explained_variance_score(self.y_test, ypred)
        score = model.score(self.X_test, self.y_test)

        res = {
            'model' : model,
            'MSE' : mse,
            'RMSE' : mse**(1/2.0),
            'MAE' : mae,
            'r2_score' : r2,
            'spearmanr corr' : sp,
            'pearsonr corr' : pe,
            'ex_variance_score' : ex,
            'score' : score
        }

        return res

    def learnCurve(self, name, model):
        ''' Permet de dessiner un graphe de la learning_curve '''

        N, train_score, val_score = learning_curve(model, self.X_train, self.y_train, cv=4, train_sizes=np.linspace(0.1,1,10) )

        plt.figure(figsize=(12,8))
        plt.plot(N, train_score.mean(axis=1), label="train score")
        plt.plot(N, val_score.mean(axis=1), label="validation score")
        plt.title(f'Learning curve avec le model {name}')
        plt.legend()
        plt.show()

    def evaluateModel(self, _type="regressor", verbose=True, scoring="MSE"):
        return self.evaluate(self.models, type=_type, verbose=verbose, scoring=scoring)

    def evaluate(self, models, type="regressor", verbose=True, scoring="MSE"):
        ''' Permet de lancer l'évaluation sur l'ensemble des models '''
        results = []
        for item in models:

            if type == "regressor":

                if verbose == True:
                    print(f"[model][evaluate]... {item['name']} ... PROCESSING.")

                res = self.evalutionRegressor(item['model'])

                res['model'] = item['name']
                results.append(res)

                self.learnCurve(item['name'], item['model'])

                if verbose == True:
                    print(f"[model][evaluate]... {item['name']} ... DONE.")

        return pd.DataFrame(results).sort_values(scoring, ascending=False)

    def getBestParams(self, models = [], use_randomized=False, cv=5, n_iters=10 ):
        ''' Permet de lancer l'optimisation des models et de retourner le meilleur paramétrage'''

        self.best_models = []
        results = []
        for item in self.models:

            if item['name'] in models:

                if use_randomized == True:
                    grid = RandomizedSearchCV(item['model'], item['hyperparams'], cv=cv, n_iter=n_iters)
                else:
                    grid = GridSearchCV(item['model'], item['hyperparams'], cv=cv)

                grid.fit(self.X_train, self.y_train)
                results.append({ 'name' : item['name'], 'score' : grid.best_score_, 'params' : grid.best_params_, 'model' : grid.best_estimator_ })

        self.best_models = results

        return pd.DataFrame(results)

    def evaluateBestModels(self, type="regressor", verbose=True, scoring="MSE"):
        ''' Permet de lancer l'évaluation sur les meilleurs modèles après être optimisé'''
        return self.evaluate(self.best_models, type=type, verbose=verbose, scoring=scoring)



