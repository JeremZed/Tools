class Roadmap():
    def __init__(self):
        self.roadmap = {
            'objectif' : {
                'problem' : {
                    'state' : None,
                    'desc' : 'Définir un object principal.',
                    'order' : 1
                },
                'metric' : {
                    'state' : None,
                    'desc' : "Il s'agit de la metric utilisée pour valider nos résultats.",
                    'order' : 2
                },
            },

            # AED/EDA - Analyse Eploratoire des Données / Exploratory Data Analysis
            'aed' : {
                'identify-target' : {
                    'state' : None,
                    'desc' : "Identification de la target.",
                    'order' : 1
                },
                'count-rows-columns' : {
                    'state' : None,
                    'desc' : "Identifier le nombre de lignes et de colonnes du dataset.",
                    'order' : 2
                },
                'identify-type-variables' : {
                    'state' : None,
                    'desc' : "Identifier le type des variables.",
                    'order' : 3
                },
                'check-missing-values' : {
                    'state' : None,
                    'desc' : "identification des valeurs manquantes.",
                    'order' : 4
                },
                'visualize-target' : {
                    'state' : None,
                    'desc' : "Visualisation de la target avec Histogramme / Boxplot",
                    'order' : 5
                },
                'variable-information' : {
                    'state' : None,
                    'desc' : "Compréhension de chaque variable via des recherches sur internet.",
                    'order' : 6
                },
                'identify-outliers' : {
                    'state' : None,
                    'desc' : "Identifier les outliers.",
                    'order' : 7
                },

            },
            # Preprocessing
            'preprocessing' : {
                'split' : {
                    'state' : None,
                    'desc' : "Création du Train set / Test set.",
                    'order' : 1
                },
                'remove-nan' : {
                    'state' : None,
                    'desc' : "Elimination des valeurs manquantes ou imputation.",
                    'order' : 2
                },
                'encodage' : {
                    'state' : None,
                    'desc' : "Transformation des variables qualitatives en valeur numérique. (ont-hot).",
                    'order' : 3
                },
                'remove-outliers' : {
                    'state' : None,
                    'desc' : "Elimination des abérantes.",
                    'order' : 4
                },
                'feature-selection' : {
                    'state' : None,
                    'desc' : "Sélection des variables.",
                    'order' : 5
                },
                'feature-engineering' : {
                    'state' : None,
                    'desc' : "Création de variables synthétiques.",
                    'order' : 6
                },
                'feature-scaling' : {
                    'state' : None,
                    'desc' : "Centrer et réduire les datas.",
                    'order' : 7
                },
            },
            # Modelling
            'modelling' : {
                'evaluation' : {
                    'state' : None,
                    'desc' : "Définir une fonction d'évaluation.",
                    'order' : 1
                },
                'training' : {
                    'state' : None,
                    'desc' : "Entraîner les différents models.",
                    'order' : 2
                },
                'optimization' : {
                    'state' : None,
                    'desc' : "Optimisation du model avec GridSearchCV.",
                    'order' : 3
                },
                'analyze-callback' : {
                    'state' : None,
                    'desc' : "Analyser les erreurs et retour au preprocessing / EDA",
                    'order' : 4
                },
                'learning-curve' : {
                    'state' : None,
                    'desc' : "Learning Curve et prise de décision.",
                    'order' : 5
                },
            }
        }

    def getRoadmap(self):
        ''' Permet de retourner l'état globale de la roadmap du projet '''
        for r in self.roadmap:
            for t in self.roadmap[r]:
                d = '[' + str(r) + ' > ' + str(t) + '] -- ' +str(self.roadmap[r][t]['desc'])
                s = self.roadmap[r][t]['state']
                print('{:<120}'.format(d), s)
            print("")

    def setDoneRoadmap(self, group, key ):
        ''' Permet de changer l'état d'une étape de la roadmap à terminée.'''
        try:
            self.roadmap[group][key]['state'] = '✓'
        except:
            print("not found")