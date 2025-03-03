import numpy as np

class ReductionBruit:
    def __init__(self, taux_echantillonnage):
        self.taux_echantillonnage = taux_echantillonnage
        self.profil_bruit = None

    def creer_profil_bruit(self, echantillons, duree=0.5):
        """Capture le profil de bruit sur les premières X secondes"""
        nb_echantillons = int(duree * self.taux_echantillonnage)
        self.profil_bruit = np.array(echantillons[:nb_echantillons], dtype=float)
        return self.profil_bruit

    def _tfc(self, x, taille_fenetre=1024, pas=512):
        """Calcul de la Transformée de Fourier à Court Terme (STFT) de manière vectorisée"""
        x = np.array(x, dtype=float)
        window = np.hanning(taille_fenetre)
        frames = []
        for i in range(0, len(x) - taille_fenetre, pas):
            frame = x[i:i + taille_fenetre] * window
            fft_frame = np.fft.fft(frame)
            frames.append(fft_frame)
        return frames

    def _tfc_inverse(self, frames, taille_fenetre=1024, pas=512):
        """Transformée de Fourier inverse avec recouvrement et addition de trames"""
        window = np.hanning(taille_fenetre)
        sortie = np.zeros(len(frames) * pas + taille_fenetre, dtype=float)
        for i, frame in enumerate(frames):
            inverse = np.fft.ifft(frame).real
            start = i * pas
            sortie[start:start + taille_fenetre] += inverse * window
        return self._normaliser(sortie)

    def _normaliser(self, x):
        """Normalisation du signal pour qu'il occupe toute l'échelle d'un signal 16 bits"""
        max_val = np.max(np.abs(x))
        if max_val == 0:
            return x.astype(np.int16)
        norm = (x / max_val * 32767).astype(np.int16)
        return norm

    def reduire_bruit(self, echantillons, taille_fenetre=1024, reduction_bruit=0.5, pas=512):
        """Réduction de bruit par soustraction spectrale optimisée"""
        if self.profil_bruit is None:
            raise ValueError("Profil de bruit non créé")
        
        # Calcul du profil de bruit
        frames_bruit = self._tfc(self.profil_bruit, taille_fenetre, pas)
        # Pour une estimation plus robuste, on peut moyenner sur toutes les trames de bruit
        spectres_bruit = np.array([np.abs(frame) for frame in frames_bruit])
        spectre_bruit = np.mean(spectres_bruit, axis=0)

        # Traitement du signal complet
        frames_signal = self._tfc(echantillons, taille_fenetre, pas)
        frames_nettoyees = []
        for frame in frames_signal:
            magnitude = np.abs(frame)
            phase = np.angle(frame)
            # Soustraction spectrale avec protection contre les valeurs négatives
            magnitude_nettoyee = np.maximum(magnitude - reduction_bruit * spectre_bruit, 0)
            frame_nettoye = magnitude_nettoyee * np.exp(1j * phase)
            frames_nettoyees.append(frame_nettoye)

        return self._tfc_inverse(frames_nettoyees, taille_fenetre, pas)
