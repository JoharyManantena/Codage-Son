import wave
import numpy as np

# Paramètres audio
frequence_echantillonnage = 44100  # Fréquence d'échantillonnage (Hz)
duree = 5  # Durée du son en secondes
nombre_echantillons = frequence_echantillonnage * duree

# Générer du bruit blanc
bruit_blanc = np.random.normal(0, 0.5, nombre_echantillons)

# Générer du bruit rose (approximation)
def generer_bruit_rose(taille):
    impair = taille % 2
    X = np.random.randn(taille // 2 + 1 + impair) + 1j * np.random.randn(taille // 2 + 1 + impair)
    S = np.arange(len(X))**-0.5  # Loi de puissance pour bruit rose
    S[0] = 0  # Éviter l'infini
    y = (np.fft.irfft(X * S)).real
    return y[:taille] if impair == 0 else y[:taille-1]

bruit_rose = generer_bruit_rose(nombre_echantillons)

# Ajouter un bruit de fond basse fréquence (ex: vibrations)
bruit_de_fond = np.sin(2 * np.pi * np.linspace(0, 10, nombre_echantillons)) * 0.3

# Mélanger les bruits ensemble
bruit_combine = bruit_blanc + bruit_rose + bruit_de_fond
bruit_combine = (bruit_combine / np.max(np.abs(bruit_combine)) * 32767).astype(np.int16)  # Normalisation

# Sauvegarde en fichier WAV
with wave.open("input_noise.wav", "w") as fichier_wav:
    fichier_wav.setnchannels(1)  # Mono
    fichier_wav.setsampwidth(2)  # 16 bits (2 octets)
    fichier_wav.setframerate(frequence_echantillonnage)
    fichier_wav.writeframes(bruit_combine.tobytes())

print("Fichier input_noise.wav créé avec plusieurs types de bruit ! ✅")
