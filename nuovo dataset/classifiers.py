import pandas as pd
from sklearn.ensemble import (AdaBoostClassifier, GradientBoostingClassifier,
                              RandomForestClassifier)
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, fbeta_score)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('./CSVs/dataset_normalizzato.csv')

# divido i dati tra training set and test set
X = df.drop('is_canceled', axis=1)
y = df['is_canceled']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 42)

# KNN
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)

print()
print("KNN Classification Report:")
print(classification_report(y_test, y_pred_knn))
f2_knn = fbeta_score(y_test, y_pred_knn, beta=2)
print(f"F2 Score: {f2_knn}\n")

conf = confusion_matrix(y_test, y_pred_knn)
print(f"Confusion Matrix : \n{conf}")

# DECISION TREE CLASSIFIER
dtc = DecisionTreeClassifier()
dtc.fit(X_train, y_train)
y_pred_dtc = dtc.predict(X_test)

print()
print("Decision Tree Classification Report:")
print(classification_report(y_test, y_pred_dtc))
f2_dtc = fbeta_score(y_test, y_pred_dtc, beta=2)
print(f"F2 Score: {f2_dtc}\n")

conf = confusion_matrix(y_test, y_pred_dtc)
print(f"Confusion Matrix : \n{conf}")

# RANDOM FOREST CLASSIFIER
rd_clf = RandomForestClassifier()
rd_clf.fit(X_train, y_train)
y_pred_rd_clf = rd_clf.predict(X_test)

print()
print("Random Forest Classification Report:")
print(classification_report(y_test, y_pred_rd_clf))
f2_rd_clf = fbeta_score(y_test, y_pred_rd_clf, beta=2)
print(f"F2 Score: {f2_rd_clf}")

conf = confusion_matrix(y_test, y_pred_rd_clf)
print(f"Confusion Matrix : \n{conf}")

# ADA BOOST CLASSIFIER
ada = AdaBoostClassifier(estimator = dtc)
ada.fit(X_train, y_train)
y_pred_ada = ada.predict(X_test)

print()
print("Ada Boost Classifier Classification Report:")
print(classification_report(y_test, y_pred_ada))
f2_ada = fbeta_score(y_test, y_pred_ada, beta=2)
print(f"F2 Score: {f2_ada}")

conf = confusion_matrix(y_test, y_pred_ada)
print(f"Confusion Matrix : \n{conf}")

# GRADIENT BOOSTING CLASSIFIER
gb = GradientBoostingClassifier()
gb.fit(X_train, y_train)
y_pred_gb = gb.predict(X_test)

print()
print("Gradient Boosting Classifier Classification Report:")
print(classification_report(y_test, y_pred_gb))
f2_gb = fbeta_score(y_test, y_pred_gb, beta=2)
print(f"F2 Score: {f2_gb}")

conf = confusion_matrix(y_test, y_pred_gb)
print(f"Confusion Matrix : \n{conf}")