import pickle

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import (AdaBoostClassifier, GradientBoostingClassifier,
                              RandomForestClassifier)
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, fbeta_score, precision_score,
                             recall_score)
from sklearn.model_selection import (GridSearchCV, KFold, ParameterGrid,
                                     train_test_split)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('./CSVs/dataset_normalizzato.csv')

# Divido i dati in training e test set
X = df.drop('is_canceled', axis=1)
y = df['is_canceled']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Definisco il numero di folds 
k_folds = 10

# Creo il KFold object
kfold = KFold(n_splits=k_folds)

# Lista dei classificatori
classifiers = [
    ('KNN', KNeighborsClassifier(), {'n_neighbors': range(2, 11)}),
    ('Decision Tree', DecisionTreeClassifier(), {'max_depth': range(3, 21)}),
    ('Random Forest', RandomForestClassifier(), {'n_estimators': range(50, 301, 50), 'max_depth': range(5, 31, 5)}),
    ('Ada Boost Classifier', AdaBoostClassifier(estimator=DecisionTreeClassifier()), {'n_estimators': range(50, 301, 50), 'learning_rate': [0.01, 0.1, 1.0]}),
    ('Gradient Boosting Classifier', GradientBoostingClassifier(), {'n_estimators': range(50, 201, 50), 'learning_rate': [0.01, 0.1, 1.0]})
]

# Dizionario per memorizzare i modelli migliori
best_models = {}

with open("./Valutazioni/valutazione_k_fold_&_grid_search_2.txt", "w") as file:
    file.write("Valori medi ottenuti tramite kfold:\n\n")

    # K-fold cross-validation
    for classifier_name, classifier, param_grid in classifiers:
        best_f2_score = 0  # Miglior punteggio F2 ottenuto
        best_params = None  # Migliori parametri trovati
        best_avg_scores = None  # Migliori punteggi medi delle metriche
        
        for params in ParameterGrid(param_grid):
            acc_scores = []
            prec_scores = []
            rec_scores = []
            f2_scores = []

            for train_index, val_index in kfold.split(X_train):
                # Divido i dati in training e validation set per il fold
                X_train_fold, X_val_fold = X_train.iloc[train_index], X_train.iloc[val_index]
                y_train_fold, y_val_fold = y_train.iloc[train_index], y_train.iloc[val_index]

                # Creo il classificatore con i parametri correnti
                clf = classifier.set_params(**params)
                clf.fit(X_train_fold, y_train_fold)

                # Ottengo le predizioni sul validation set
                y_pred = clf.predict(X_val_fold)

                # Calcolo le misure di valutazione
                acc_scores.append(accuracy_score(y_val_fold, y_pred))
                prec_scores.append(precision_score(y_val_fold, y_pred))
                rec_scores.append(recall_score(y_val_fold, y_pred))
                f2_scores.append(fbeta_score(y_val_fold, y_pred, beta=2))

            # Calcolo i valori medi delle misure di valutazione per i parametri correnti
            avg_acc_score = sum(acc_scores) / len(acc_scores)
            avg_prec_score = sum(prec_scores) / len(prec_scores)
            avg_rec_score = sum(rec_scores) / len(rec_scores)
            avg_f2_score = sum(f2_scores) / len(f2_scores)

            # Stampo i valori medi delle misure di valutazione per i parametri correnti con la grid search
            file.write(str(classifier_name + "\n"))
            file.write("Parameters: {}\n".format(params))
            file.write("Average Accuracy Score: {:.4f}, ".format(avg_acc_score))
            file.write("Average Precision Score: {:.4f}, ".format(avg_prec_score))
            file.write("Average Recall Score: {:.4f}, ".format(avg_rec_score))
            file.write("F2 Score: {:.4f}.".format(avg_f2_score))
            file.write("\n")

            # Memorizzo il modello addestrato per i parametri correnti se ottengo un punteggio F2 migliore
            if avg_f2_score > best_f2_score:
                best_f2_score = avg_f2_score
                best_params = params
                best_avg_scores = (avg_acc_score, avg_prec_score, avg_rec_score)

        # Stampo i valori medi delle misure di valutazione per i parametri migliori con la grid search
        file.write(str(classifier_name + " best parameters: {}\n".format(best_params)))
        file.write("Average Accuracy Score: {:.4f},".format(best_avg_scores[0]))
        file.write(" Average Precision Score: {:.4f},".format(best_avg_scores[1]))
        file.write(" Average Recall Score: {:.4f},".format(best_avg_scores[2]))
        file.write(" F2 Score: {:.4f}.\n".format(best_f2_score))
        file.write("\n\n")

        # Addestramento del miglior modello con i parametri migliori
        clf = classifier.set_params(**best_params)
        clf.fit(X_train, y_train)
        best_models[classifier_name] = clf

for classifier_name, classifier in best_models.items():
    filename = f"best_model_{classifier_name}.pkl"
    with open(filename, "wb") as file:
        pickle.dump(classifier, file)

f2_scores_test = {}
f2_scores_train = {} 

with open("./Valutazioni/valutazione_test_set_2.txt", "w") as file:
    file.write("Valutazione dei modelli sul test set:\n\n") 
    # Valutazione dei migliori modelli sul test set
    for classifier_name, classifier in best_models.items():
        y_test_pred = classifier.predict(X_test)

        file.write(str(classifier_name) + "\n")
        file.write("Confusion Matrix:\n" + str(confusion_matrix(y_test, y_test_pred)) + "\n")
        test_f2 = fbeta_score(y_test, y_test_pred, beta=2)
        file.write("F2 Score: " + str(test_f2) + "\n")
        file.write(classification_report(y_test, y_test_pred) + "\n")