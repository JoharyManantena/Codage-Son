import wave
import struct

class FichierWAV:
    def __init__(self, fichier):
        self.fichier = fichier
        self.echantillons = []
        self.taux_echantillonnage = 44100  # Valeur par défaut
        self.nb_canaux = 1
        self.profondeur_bits = 16

    def charger(self):
        """Charge les échantillons audio du fichier WAV."""
        with wave.open(self.fichier, 'rb') as wav:
            self.nb_canaux = wav.getnchannels()
            self.taux_echantillonnage = wav.getframerate()
            self.profondeur_bits = wav.getsampwidth() * 8
            frames = wav.readframes(wav.getnframes())

            # Convertir les données binaires en entiers
            fmt = f"{len(frames) // (self.profondeur_bits // 8)}h"
            self.echantillons = list(struct.unpack(fmt, frames))

    def sauvegarder(self, fichier_sortie):
        """Sauvegarde les échantillons audio dans un fichier WAV."""
        with wave.open(fichier_sortie, 'wb') as wav:
            wav.setnchannels(self.nb_canaux)
            wav.setsampwidth(self.profondeur_bits // 8)
            wav.setframerate(self.taux_echantillonnage)

            # Convertir les entiers en données binaires
            frames = struct.pack(f"{len(self.echantillons)}h", *self.echantillons)
            wav.writeframes(frames)
