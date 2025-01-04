import os
import shutil
import pandas as pd

# Poti do map s posnetki
categories = {
    "Cavitation": "./Dataset/kavitacija/mp3_files/Cavitation",
    "Flow noise": "./Dataset/kavitacija/mp3_files/Flow",
    "Rattling": "./Dataset/kavitacija/mp3_files/Rattling",
    "Whistling": "./Dataset/kavitacija/mp3_files/Whistling"
}

# Če mapa ne obstaja jo naredi
for folder in categories.values():
    os.makedirs(folder, exist_ok=True)

# Branje excel fila z oznakami
data_file = "./Dataset/kavitacija/mp3_file_list_and_classes.xlsx"
df = pd.read_excel(data_file)

# Print the column names
print("Column names:", df.columns)

# vsak file iz map preveri kam spada in ga kopiraj
for index, row in df.iterrows():
    file_name = row['mp3 file']

    # preveri razred
    for category, column in zip(categories.keys(), categories.keys()):
        if row[column] == 1: 
            source_path = f"./Dataset/kavitacija/mp3_files/Skupaj/{file_name}"
            destination_path = os.path.join(categories[category], file_name)

            # Copy v mapo
            if os.path.exists(source_path):
                shutil.copy(source_path, destination_path)
                print(f"Copied {file_name} to {categories[category]}")
            else:
                print(f"File not found: {source_path}")
            break
