import os
import numpy as np
import pandas as pd
from pydub import AudioSegment
from scipy.fft import fft
from scipy.signal import find_peaks

# Definicija datotek in poti
category = "Cavitation"
audio_folder = "./Dataset/kavitacija/mp3_files/" + category
output_csv = audio_folder + "/audioZnacilke.csv"

def extract_features(audio, sample_rate):
    # audio v mono in normalizacija
    audio_data = np.array(audio.get_array_of_samples())
    if audio.channels > 1:
        audio_data = audio_data.reshape((-1, audio.channels)).mean(axis=1)  # stereo v mono

    N = len(audio_data)
    fft_data = np.abs(fft(audio_data))[:N // 2] / N  # normaliziranje FFT-ja z dolžino posnetka
    freqs = np.fft.fftfreq(N, 1 / sample_rate)[:N // 2]

    # Posebne značilke
    peak_indices, _ = find_peaks(fft_data)
    peaks = freqs[peak_indices]
    spectral_centroid = np.sum(freqs * fft_data) / (np.sum(fft_data) + 1e-7)
    spectral_bandwidth = np.sqrt(np.sum(((freqs - spectral_centroid)**2) * fft_data) / (np.sum(fft_data) + 1e-7))
    
    total_energy = np.sum(fft_data)
    energy_low = np.sum(fft_data[freqs < 1000]) / (total_energy + 1e-7)
    energy_high = np.sum(fft_data[freqs > 3000]) / (total_energy + 1e-7)

    # Statistične značilke
    mean_amplitude = np.mean(fft_data)
    variance = np.var(fft_data)
    skewness = np.mean(((fft_data - mean_amplitude)**3)) / (np.std(fft_data)**3 + 1e-7)  
    kurtosis = np.mean(((fft_data - mean_amplitude)**4)) / (np.std(fft_data)**4 + 1e-7)

    # Nabor končnih značilk
    features = {
        "spectral_centroid": spectral_centroid,  # Hz
        "spectral_bandwidth": spectral_bandwidth,  # Hz
        "energy_low": energy_low,  # %
        "energy_high": energy_high,  # %
        "mean_amplitude": mean_amplitude,
        "variance": variance,
        "skewness": skewness,
        "kurtosis": kurtosis,
        "peak_count": len(peaks)
    }
    return features

# Obdelava vseh posnetkov
all_features = []
for file_name in os.listdir(audio_folder):
    if file_name.endswith('.mp3'):
        file_path = os.path.join(audio_folder, file_name)

        # Naloži posnetek
        audio = AudioSegment.from_file(file_path)
        sample_rate = audio.frame_rate

        # Pridobi značilke
        features = extract_features(audio, sample_rate)
        features["category"] = category
        features["file_name"] = file_name
        all_features.append(features)

# Shrani v CSV s formatiranjem za slovenski excel (samo odpri ne uvažat!)
df = pd.DataFrame(all_features)
df = df.round({
    "spectral_centroid": 6,
    "spectral_bandwidth": 6,
    "energy_low": 6,
    "energy_high": 6,
    "mean_amplitude": 6,
    "variance": 6,
    "skewness": 6,
    "kurtosis": 6
})
df = pd.DataFrame(all_features)
df.to_csv(output_csv, index=False, float_format="%.6f", decimal=".")

print(f"Features saved to {output_csv}")
