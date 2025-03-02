# create.py

import wave
import numpy as np

# Paramètres de l'audio
frequence_echantillonnage = 44100  # Fréquence d'échantillonnage (Hz)
duree = 10  # Durée du son en secondes
frequence = 650.0  # Fréquence du son (Hz, 440 Hz correspond à La)

# Création du signal sinusoidal
temps = np.linspace(0, duree, int(frequence_echantillonnage * duree), endpoint=False)
echantillons = (np.sin(2 * np.pi * frequence * temps) * 32767).astype(np.int16)

# Sauvegarde du signal dans un fichier WAV
with wave.open("input.wav", "w") as fichier_wav:
    fichier_wav.setnchannels(1)  # Mono
    fichier_wav.setsampwidth(2)  # 16 bits (2 octets)
    fichier_wav.setframerate(frequence_echantillonnage)
    fichier_wav.writeframes(echantillons.tobytes())

print("Fichier input.wav créé avec succès !")
