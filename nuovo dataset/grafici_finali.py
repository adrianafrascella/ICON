import pickle

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import (accuracy_score, fbeta_score, precision_score,
                             recall_score)
from sklearn.model_selection import train_test_split

df = pd.read_csv('./CSVs/dataset_normalizzato.csv')

# Divido i dati in training e test set
X = df.drop('is_canceled', axis=1)
y = df['is_canceled']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Carico i modelli salvati
model_filenames = [
    "best_model_KNN.pkl",
    "best_model_Decision Tree.pkl",
    "best_model_Random Forest.pkl",
    "best_model_Ada Boost Classifier.pkl",
    "best_model_Gradient Boosting Classifier.pkl"
]
best_models = {}

for model_filename in model_filenames:
    with open(model_filename, "rb") as file:
        clf = pickle.load(file)
        classifier_name = model_filename.split("_")[2].split(".")[0]
        best_models[classifier_name] = clf

# Calcolo i punteggi F2, accuracy e recall sui dati di addestramento e di test
f2_scores_train = {}
f2_scores_test = {}
accuracy_scores_train = {}
accuracy_scores_test = {}
recall_scores_train = {}
recall_scores_test = {}
precision_scores_train = {}
precision_scores_test = {}

for classifier_name, classifier in best_models.items():
    y_train_pred = classifier.predict(X_train)
    y_test_pred = classifier.predict(X_test)

    train_f2 = fbeta_score(y_train, y_train_pred, beta=2)
    test_f2 = fbeta_score(y_test, y_test_pred, beta=2)

    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)

    train_recall = recall_score(y_train, y_train_pred)
    test_recall = recall_score(y_test, y_test_pred)

    train_precision = precision_score(y_train, y_train_pred)
    test_precision = precision_score(y_test, y_test_pred)

    f2_scores_train[classifier_name] = train_f2
    f2_scores_test[classifier_name] = test_f2

    accuracy_scores_train[classifier_name] = train_accuracy
    accuracy_scores_test[classifier_name] = test_accuracy

    recall_scores_train[classifier_name] = train_recall
    recall_scores_test[classifier_name] = test_recall

    precision_scores_train[classifier_name] = train_precision
    precision_scores_test[classifier_name] = test_precision

# Creo il grafico per i punteggi F2 dei migliori modelli
plt.figure(figsize=(10, 6))
plt.bar(range(len(f2_scores_test)), list(f2_scores_test.values()), align='center')
plt.xticks(range(len(f2_scores_test)), list(f2_scores_test.keys()), rotation=45)
plt.xlabel('Model')
plt.ylabel('F2 Score')
plt.title('F2 Score Comparison for Best Models')
plt.tight_layout()

for i, value in enumerate(f2_scores_test.values()):
    plt.text(i, value + 0.01, f'{value:.4f}', color='black', ha='center')

plt.show()

# Creo il grafico per i punteggi F2 dei migliori modelli su train e test
plt.figure(figsize=(12, 6))
bar_width = 0.35
index = np.arange(len(f2_scores_train))

plt.bar(index, list(f2_scores_train.values()), bar_width, label='Train F2 Score')
plt.bar(index + bar_width, list(f2_scores_test.values()), bar_width, label='Test F2 Score')

plt.xticks(index + bar_width / 2, list(f2_scores_train.keys()), rotation=45)
plt.xlabel('Model')
plt.ylabel('F2 Score')
plt.title('F2 Score Comparison for Best Models (Train vs Test)')
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
plt.tight_layout()

# Aggiungo le etichette per precision sopra le barre
for i, value in enumerate(precision_scores_train.values()):
    plt.text(i, value + 0.005, f'{value:.4f}', color='black', ha='center')
for i, value in enumerate(precision_scores_test.values()):
    plt.text(i + bar_width, value + 0.005, f'{value:.4f}', color='black', ha='center')

plt.show()

# Creo il grafico per l'accuracy di test e training per ogni modello
plt.figure(figsize=(12, 6))
index = np.arange(len(accuracy_scores_train))
bar_width = 0.35

plt.bar(index, list(accuracy_scores_train.values()), bar_width, label='Train Accuracy')
plt.bar(index + bar_width, list(accuracy_scores_test.values()), bar_width, label='Test Accuracy')

plt.xticks(index + bar_width / 2, list(accuracy_scores_train.keys()), rotation=45)
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Accuracy Comparison for Best Models (Train vs Test)')
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
plt.tight_layout()

# Aggiungo le etichette per accuracy sopra le barre
for i, value in enumerate(accuracy_scores_train.values()):
    plt.text(i - 0.12, value + 0.005, f'{value:.4f}', color='black')
for i, value in enumerate(accuracy_scores_test.values()):
    plt.text(i + bar_width - 0.12, value + 0.005, f'{value:.4f}', color='black')

plt.show()

# Creo il grafico per la recall di test e training per ogni modello
plt.figure(figsize=(12, 6))
index = np.arange(len(recall_scores_train))
bar_width = 0.35

plt.bar(index, list(recall_scores_train.values()), bar_width, label='Train Recall')
plt.bar(index + bar_width, list(recall_scores_test.values()), bar_width, label='Test Recall')

plt.xticks(index + bar_width / 2, list(recall_scores_train.keys()), rotation=45)
plt.xlabel('Model')
plt.ylabel('Recall')
plt.title('Recall Comparison for Best Models (Train vs Test)')
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
plt.tight_layout()

# Aggiungo le etichette per recall sopra le barre
for i, value in enumerate(recall_scores_train.values()):
    plt.text(i - 0.12, value + 0.005, f'{value:.4f}', color='black')
for i, value in enumerate(recall_scores_test.values()):
    plt.text(i + bar_width - 0.12, value + 0.005, f'{value:.4f}', color='black')

plt.show()

# Creo il grafico per la precision di test e training per ogni modello
plt.figure(figsize=(12, 6))
index = np.arange(len(precision_scores_train))
bar_width = 0.35

plt.bar(index, list(precision_scores_train.values()), bar_width, label='Train Precision')
plt.bar(index + bar_width, list(precision_scores_test.values()), bar_width, label='Test Precision')

plt.xticks(index + bar_width / 2, list(precision_scores_train.keys()), rotation=45)
plt.xlabel('Model')
plt.ylabel('Precision')
plt.title('Precision Comparison for Best Models (Train vs Test)')
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
plt.tight_layout()

# Aggiungo le etichette per precision sopra le barre
for i, value in enumerate(precision_scores_train.values()):
    plt.text(i - 0.12, value + 0.005, f'{value:.4f}', color='black')
for i, value in enumerate(precision_scores_test.values()):
    plt.text(i + bar_width - 0.12, value + 0.005, f'{value:.4f}', color='black')

plt.show()
