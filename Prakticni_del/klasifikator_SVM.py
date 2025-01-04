import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score

# Define paths to the folders containing the CSV files
csvFile = "audioZnacilke.csv"
category1 = "Cavitation/"
category2 = "Flow/"
category3 = "Rattling/"
category4 = "Whistling/"
root_folder = "./Dataset/kavitacija/mp3_files/"
folders = [root_folder + category1, root_folder + category2 , root_folder + category3, root_folder + category4]

# Load and combine all CSV files
dataframes = []
for folder in folders:
    for file_name in os.listdir(folder):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder, file_name)
            df = pd.read_csv(file_path)
            dataframes.append(df)

# Combine all dataframes into one
data = pd.concat(dataframes, ignore_index=True)

# Drop the 'file_name' column (if present) as it's not relevant for training
if 'file_name' in data.columns:
    data = data.drop(columns=['file_name'])

# Split data into features (X) and labels (y)
X = data.drop(columns=['category'])  # Features
y = data['category']                 # Labels

# Normalize the features
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)

# Train an SVM classifier
svm_model = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
svm_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = svm_model.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
