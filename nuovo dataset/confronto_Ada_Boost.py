import pickle

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import (accuracy_score, fbeta_score, precision_score,
                             recall_score)
from sklearn.model_selection import train_test_split

df = pd.read_csv('./CSVs/dataset_normalizzato.csv')

# Divido i dati in training e test set
X = df.drop('is_canceled', axis=1)
y = df['is_canceled']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Carico il modello Ada Boost Classifier salvato
with open("best_model_Ada Boost Classifier.pkl", "rb") as file:
    best_ada_boost = pickle.load(file)

# Creo un nuovo Ada Boost Classifier con learning rate 0.01 e 150 stimatori
ada_boost_new = AdaBoostClassifier(learning_rate=1.00, n_estimators=150)
ada_boost_new.fit(X_train, y_train)

# Calcolo i punteggi F2, accuracy, recall e precision per best_model_Ada Boost Classifier
y_train_pred_best = best_ada_boost.predict(X_train)
y_test_pred_best = best_ada_boost.predict(X_test)

best_accuracy_train = accuracy_score(y_train, y_train_pred_best)
best_accuracy_test = accuracy_score(y_test, y_test_pred_best)

best_f2_train = fbeta_score(y_train, y_train_pred_best, beta=2)
best_f2_test = fbeta_score(y_test, y_test_pred_best, beta=2)

best_precision_train = precision_score(y_train, y_train_pred_best)
best_precision_test = precision_score(y_test, y_test_pred_best)

best_recall_train = recall_score(y_train, y_train_pred_best)
best_recall_test = recall_score(y_test, y_test_pred_best)

# Calcolo i punteggi F2, accuracy, recall e precision per Ada Boost Classifier con nuovi parametri
y_train_pred_new = ada_boost_new.predict(X_train)
y_test_pred_new = ada_boost_new.predict(X_test)

new_accuracy_train = accuracy_score(y_train, y_train_pred_new)
new_accuracy_test = accuracy_score(y_test, y_test_pred_new)

new_f2_train = fbeta_score(y_train, y_train_pred_new, beta=2)
new_f2_test = fbeta_score(y_test, y_test_pred_new, beta=2)

new_precision_train = precision_score(y_train, y_train_pred_new)
new_precision_test = precision_score(y_test, y_test_pred_new)

new_recall_train = recall_score(y_train, y_train_pred_new)
new_recall_test = recall_score(y_test, y_test_pred_new)

# Creao del grafico per l'accuracy di test e training per best_model_Ada Boost Classifier e Ada Boost con nuovi parametri
models = ['best_model_Ada Boost Classifier', 'Ada Boost (LR=1.00, n_est=150)']
accuracy_train = [best_accuracy_train, new_accuracy_train]
accuracy_test = [best_accuracy_test, new_accuracy_test]

plt.figure(figsize=(8, 6))
bar_width = 0.35
index = np.arange(len(models))

plt.bar(index, accuracy_train, bar_width, label='Train Accuracy')
plt.bar(index + bar_width, accuracy_test, bar_width, label='Test Accuracy')

plt.xticks(index + bar_width / 2, models, rotation=45)
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Accuracy Comparison for Ada Boost Models')
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
plt.tight_layout()

# Aggiungo le etichette per accuracy sopra le barre
for i, value in enumerate(accuracy_train):
    plt.text(i - 0.12, value + 0.005, f'{value:.4f}', color='black')
for i, value in enumerate(accuracy_test):
    plt.text(i + bar_width - 0.12, value + 0.005, f'{value:.4f}', color='black')

plt.show()

# Creo il grafico per l'F2 score di test e training per best_model_Ada Boost Classifier e Ada Boost con nuovi parametri
f2_train = [best_f2_train, new_f2_train]
f2_test = [best_f2_test, new_f2_test]

plt.figure(figsize=(8, 6))
plt.bar(index, f2_train, bar_width, label='Train F2 Score')
plt.bar(index + bar_width, f2_test, bar_width, label='Test F2 Score')

plt.xticks(index + bar_width / 2, models, rotation=45)
plt.xlabel('Model')
plt.ylabel('F2 Score')
plt.title('F2 Score Comparison for Ada Boost Models')
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
plt.tight_layout()

# Aggiungo le etichette per F2 score sopra le barre
for i, value in enumerate(f2_train):
    plt.text(i - 0.12, value + 0.005, f'{value:.4f}', color='black')
for i, value in enumerate(f2_test):
    plt.text(i + bar_width - 0.12, value + 0.005, f'{value:.4f}', color='black')

plt.show()

# Creo il grafico per la precision di test e training per best_model_Ada Boost Classifier e Ada Boost con nuovi parametri
precision_train = [best_precision_train, new_precision_train]
precision_test = [best_precision_test, new_precision_test]

plt.figure(figsize=(8, 6))
plt.bar(index, precision_train, bar_width, label='Train Precision')
plt.bar(index + bar_width, precision_test, bar_width, label='Test Precision')

plt.xticks(index + bar_width / 2, models, rotation=45)
plt.xlabel('Model')
plt.ylabel('Precision')
plt.title('Precision Comparison for Ada Boost Models')
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
plt.tight_layout()

# Aggiungo le etichette per precision sopra le barre
for i, value in enumerate(precision_train):
    plt.text(i - 0.12, value + 0.005, f'{value:.4f}', color='black')
for i, value in enumerate(precision_test):
    plt.text(i + bar_width - 0.12, value + 0.005, f'{value:.4f}', color='black')

plt.show()

# Creo il grafico per la recall di test e training per best_model_Ada Boost Classifier e Ada Boost con nuovi parametri
recall_train = [best_recall_train, new_recall_train]
recall_test = [best_recall_test, new_recall_test]

plt.figure(figsize=(8, 6))
plt.bar(index, recall_train, bar_width, label='Train Recall')
plt.bar(index + bar_width, recall_test, bar_width, label='Test Recall')

plt.xticks(index + bar_width / 2, models, rotation=45)
plt.xlabel('Model')
plt.ylabel('Recall')
plt.title('Recall Comparison for Ada Boost Models')
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
plt.tight_layout()

# Aggiungo le etichette per recall sopra le barre
for i, value in enumerate(recall_train):
    plt.text(i - 0.12, value + 0.005, f'{value:.4f}', color='black')
for i, value in enumerate(recall_test):
    plt.text(i + bar_width - 0.12, value + 0.005, f'{value:.4f}', color='black')

plt.show()
