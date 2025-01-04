import os
from pydub import AudioSegment

# Vhodna in izhodna mapa (isti)
audio_folder = './Dataset/kavitacija/mp3_files/Whistling'  
output_folder = audio_folder


# Parametri za chunke
chunk_length = 500  # Chunk size: 0.5 sekunde
overlap = 100       # Overlap size: 0.1 sekunde
step_size = chunk_length - overlap  # Step size za sliding window

# Procesiraj vsak file 
for file_name in os.listdir(audio_folder):
    if file_name.lower().endswith(('.mp3', '.wav', '.flac')):  
        file_path = os.path.join(audio_folder, file_name)

        # Naloadaj file
        audio = AudioSegment.from_file(file_path)

        # Split file v chunke
        chunks = []
        for start_time in range(0, len(audio) - chunk_length + step_size, step_size):
            chunk = audio[start_time:start_time + chunk_length]
            chunks.append(chunk)

        # Shrani chunke v output file
        base_name = os.path.splitext(file_name)[0]
        for i, chunk in enumerate(chunks):
            chunk_name = f"{base_name}_chunk_{i + 1}.mp3"
            chunk_path = os.path.join(output_folder, chunk_name)
            chunk.export(chunk_path, format="mp3")

        # Briši original file
        os.remove(file_path)
        print(f"Processed {file_name} into {len(chunks)} chunks and deleted the original file.")
