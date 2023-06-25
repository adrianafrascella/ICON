import pandas as pd
from sklearn.ensemble import (AdaBoostClassifier, GradientBoostingClassifier,
                              RandomForestClassifier)
from sklearn.metrics import (accuracy_score, classification_report,
                             fbeta_score, precision_score, recall_score)
from sklearn.model_selection import KFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('./CSVs/dataset_normalizzato.csv')

# divido i dati in training e test set
X = df.drop('is_canceled', axis=1)
y = df['is_canceled']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# definisco il numero di folds per la cross-validation, scelgo 10 perchè non è impiegato molto tempo per l'addestramento e per ottenere delle 
# stime più accurate delle prestazioni del modello considerando l'alto numero di dati
# con k=5 ho ottenuto dei valori leggermente migliori probabilmente perchè meno accurate
k_folds = 10

# creo il KFold object
kfold = KFold(n_splits=k_folds)

# inizializzo liste per le valutazioni di ogni fold
knn_acc_scores = []
knn_prec_scores = []
knn_rec_scores = []
knn_f2_scores = []

dtc_acc_scores = []
dtc_prec_scores = []
dtc_rec_scores = []
dtc_f2_scores = []

rd_clf_acc_scores = []
rd_clf_prec_scores = []
rd_clf_rec_scores = []
rd_clf_f2_scores = []

ada_acc_scores = []
ada_prec_scores = []
ada_rec_scores = []
ada_f2_scores = []

gb_acc_scores = []
gb_prec_scores = []
gb_rec_scores = []
gb_f2_scores = []

# k-fold cross-validation
for train_index, val_index in kfold.split(X_train):
    # divido i dati in training e validation set per fold
    X_train_fold, X_val_fold = X_train.iloc[train_index], X_train.iloc[val_index]
    y_train_fold, y_val_fold = y_train.iloc[train_index], y_train.iloc[val_index]
    
    # KNN
    knn = KNeighborsClassifier()
    knn.fit(X_train_fold, y_train_fold)
    y_pred_knn = knn.predict(X_val_fold)
    knn_acc_scores.append(accuracy_score(y_val_fold, y_pred_knn))
    knn_prec_scores.append(precision_score(y_val_fold, y_pred_knn))
    knn_rec_scores.append(recall_score(y_val_fold, y_pred_knn))
    knn_f2_scores.append(fbeta_score(y_val_fold, y_pred_knn, beta=2))
    
    # Decision Tree Classifier
    dtc = DecisionTreeClassifier()
    dtc.fit(X_train_fold, y_train_fold)
    y_pred_dtc = dtc.predict(X_val_fold)
    dtc_acc_scores.append(accuracy_score(y_val_fold, y_pred_dtc))
    dtc_prec_scores.append(precision_score(y_val_fold, y_pred_dtc))
    dtc_rec_scores.append(recall_score(y_val_fold, y_pred_dtc))
    dtc_f2_scores.append(fbeta_score(y_val_fold, y_pred_dtc, beta=2))
    
    # Random Forest Classifier
    rd_clf = RandomForestClassifier()
    rd_clf.fit(X_train_fold, y_train_fold)
    y_pred_rd_clf = rd_clf.predict(X_val_fold)
    rd_clf_acc_scores.append(accuracy_score(y_val_fold, y_pred_rd_clf))
    rd_clf_prec_scores.append(precision_score(y_val_fold, y_pred_rd_clf))
    rd_clf_rec_scores.append(recall_score(y_val_fold, y_pred_rd_clf))
    rd_clf_f2_scores.append(fbeta_score(y_val_fold, y_pred_rd_clf, beta=2))
    
    # Ada Boost Classifier
    ada = AdaBoostClassifier(estimator=dtc)
    ada.fit(X_train_fold, y_train_fold)
    y_pred_ada = ada.predict(X_val_fold)
    ada_acc_scores.append(accuracy_score(y_val_fold, y_pred_ada))
    ada_prec_scores.append(precision_score(y_val_fold, y_pred_ada))
    ada_rec_scores.append(recall_score(y_val_fold, y_pred_ada))
    ada_f2_scores.append(fbeta_score(y_val_fold, y_pred_ada, beta=2))
    
    # Gradient Boosting Classifier
    gb = GradientBoostingClassifier()
    gb.fit(X_train_fold, y_train_fold)
    y_pred_gb = gb.predict(X_val_fold)
    gb_acc_scores.append(accuracy_score(y_val_fold, y_pred_gb))
    gb_prec_scores.append(precision_score(y_val_fold, y_pred_gb))
    gb_rec_scores.append(recall_score(y_val_fold, y_pred_gb))
    gb_f2_scores.append(fbeta_score(y_val_fold, y_pred_gb, beta=2))

# calcolo i valori medi
knn_avg_acc_score = sum(knn_acc_scores) / len(knn_acc_scores)
knn_avg_prec_score = sum(knn_prec_scores) / len(knn_prec_scores)
knn_avg_rec_score = sum(knn_rec_scores) / len(knn_rec_scores)
knn_avg_f2_score = sum(knn_f2_scores) / len(knn_f2_scores)

dtc_avg_acc_score = sum(dtc_acc_scores) / len(dtc_acc_scores)
dtc_avg_prec_score = sum(dtc_prec_scores) / len(dtc_prec_scores)
dtc_avg_rec_score = sum(dtc_rec_scores) / len(dtc_rec_scores)
dtc_avg_f2_score = sum(dtc_f2_scores) / len(dtc_f2_scores)

rd_clf_avg_acc_score = sum(rd_clf_acc_scores) / len(rd_clf_acc_scores)
rd_clf_avg_prec_score = sum(rd_clf_prec_scores) / len(rd_clf_prec_scores)
rd_clf_avg_rec_score = sum(rd_clf_rec_scores) / len(rd_clf_rec_scores)
rd_clf_avg_f2_score = sum(rd_clf_f2_scores) / len(rd_clf_f2_scores)

ada_avg_acc_score = sum(ada_acc_scores) / len(ada_acc_scores)
ada_avg_prec_score = sum(ada_prec_scores) / len(ada_prec_scores)
ada_avg_rec_score = sum(ada_rec_scores) / len(ada_rec_scores)
ada_avg_f2_score = sum(ada_f2_scores) / len(ada_f2_scores)

gb_avg_acc_score = sum(gb_acc_scores) / len(gb_acc_scores)
gb_avg_prec_score = sum(gb_prec_scores) / len(gb_prec_scores)
gb_avg_rec_score = sum(gb_rec_scores) / len(gb_rec_scores)
gb_avg_f2_score = sum(gb_f2_scores) / len(gb_f2_scores)

# stampo i valori medi
with open("./Valutazioni/k_fold_on_ts.txt", "w") as file:
    file.write("KNN: ")
    file.write(f"Average Accuracy Score: {knn_avg_acc_score}, ")
    file.write(f"Average Precision Score: {knn_avg_prec_score}, ")
    file.write(f"Average Recall Score: {knn_avg_rec_score}, ")
    file.write(f"Average F2 Score: {knn_avg_f2_score}\n\n")

    file.write("Decision Tree: ")
    file.write(f"Average Accuracy Score: {dtc_avg_acc_score}, ")
    file.write(f"Average Precision Score: {dtc_avg_prec_score}, ")
    file.write(f"Average Recall Score: {dtc_avg_rec_score}, ")
    file.write(f"Average F2 Score: {dtc_avg_f2_score}\n\n")

    file.write("Random Forest: ")
    file.write(f"Average Accuracy Score: {rd_clf_avg_acc_score}, ")
    file.write(f"Average Precision Score: {rd_clf_avg_prec_score}, ")
    file.write(f"Average Recall Score: {rd_clf_avg_rec_score}, ")
    file.write(f"Average F2 Score: {rd_clf_avg_f2_score}\n\n")

    file.write("Ada Boost Classifier: ")
    file.write(f"Average Accuracy Score: {ada_avg_acc_score}, ")
    file.write(f"Average Precision Score: {ada_avg_prec_score}, ")
    file.write(f"Average Recall Score: {ada_avg_rec_score}, ")
    file.write(f"Average F2 Score: {ada_avg_f2_score}\n\n")

    file.write("Gradient Boosting Classifier: ")
    file.write(f"Average Accuracy Score: {gb_avg_acc_score}, ")
    file.write(f"Average Precision Score: {gb_avg_prec_score}, ")
    file.write(f"Average Recall Score: {gb_avg_rec_score}, ")
    file.write(f"Average F2 Score: {gb_avg_f2_score}")