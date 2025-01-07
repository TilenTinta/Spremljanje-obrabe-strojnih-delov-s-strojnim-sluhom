import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.metrics import classification_report, accuracy_score, roc_curve, auc
import matplotlib.pyplot as plt

# Poti do datotek s CSV-ji z značilkami
csvFile = "audioZnacilke.csv"
category1 = "Cavitation/"
category2 = "Flow/"
category3 = "Rattling/"
category4 = "Whistling/"
root_folder = "./Dataset/kavitacija/mp3_files/"
folders = [root_folder + category1, root_folder + category2, root_folder + category3, root_folder + category4]

# Nalaganje in združevanje značilk 
dataframes = []
for folder in folders:
    for file_name in os.listdir(folder):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder, file_name)
            df = pd.read_csv(file_path)
            dataframes.append(df)

data = pd.concat(dataframes, ignore_index=True)

# Brisanje 'file_name' stolpca - ni uporabno za naš primer
if 'file_name' in data.columns:
    data = data.drop(columns=['file_name'])

# Posebej shrani ounake in značilke
X = data.drop(columns=['category'])  # Značilke
y = data['category']                 # Oznake

# Normalizacija
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)

# Binarizacija za izris ROC krivulje
unique_classes = y.unique()
y_binarized = label_binarize(y, classes=unique_classes)
n_classes = y_binarized.shape[1]

# Ločevanje na test in train množico (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y_binarized, test_size=0.2, random_state=42)

# Učenje SVM-ja - One-vs-Rest strategy
svm_model = OneVsRestClassifier(SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42))
svm_model.fit(X_train, y_train)

# Predikcijske verjetnosti
y_score = svm_model.decision_function(X_test)

# Test naučenega modela
y_test_labels = np.argmax(y_test, axis=1)
y_pred_labels = np.argmax(y_score, axis=1)

print("Accuracy:", accuracy_score(y_test_labels, y_pred_labels))
print("\nClassification Report:\n", classification_report(y_test_labels, y_pred_labels, target_names=unique_classes))

# Računanje in izris ROC krivulje
fpr = {}
tpr = {}
roc_auc = {}

for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Izris ROC krivulj za vsak razred posebej
plt.figure(figsize=(10, 8))
for i, class_name in enumerate(unique_classes):
    plt.plot(fpr[i], tpr[i], label=f"ROC curve for {class_name} (AUC = {roc_auc[i]:.2f})")

plt.plot([0, 1], [0, 1], "k--", lw=2)  # Diagonal line
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC curves for each class")
plt.legend(loc="lower right")
plt.grid()
plt.show()
