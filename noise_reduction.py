import cmath
import math

class ReductionBruit:
    def __init__(self, taux_echantillonnage):
        self.taux_echantillonnage = taux_echantillonnage
        self.profil_bruit = None
        

    def creer_profil_bruit(self, echantillons, duree=0.5):
        """Capture le profil de bruit sur les premières X secondes"""
        nb_echantillons = int(duree * self.taux_echantillonnage)
        self.profil_bruit = echantillons[:nb_echantillons]
        return self.profil_bruit
    
    

    def _tfc(self, x, taille_fenetre=1024, pas=512):
        """Transformée de Fourier à Court Terme (manuellement)"""
        trames = []
        for i in range(0, len(x) - taille_fenetre, pas):
            trame = x[i:i + taille_fenetre]
            fenetree = [trame[n] * self._fenetre_hann(n, taille_fenetre) for n in range(taille_fenetre)]
            trames.append(self._tfd(fenetree))
        return trames
    
    

    def _tfc_inverse(self, trames, taille_fenetre=1024, pas=512):
        """Transformée inverse"""
        sortie = [0.0] * (len(trames) * pas + taille_fenetre)
        for i, trame in enumerate(trames):
            inverse = self._tfd_inverse(trame)
            debut = i * pas
            for n in range(taille_fenetre):
                sortie[debut + n] += inverse[n].real * self._fenetre_hann(n, taille_fenetre)
        return self._normaliser(sortie)
    
    

    def _tfd(self, x):
        """Implémentation FFT récursive (Cooley-Tukey)"""
        N = len(x)
        if N <= 1: return x
        pair = self._tfd(x[0::2])
        impair =  self._tfd(x[1::2])
        T = [cmath.exp(-2j * cmath.pi * k / N) * impair[k] for k in range(N // 2)]
        return [pair[k] + T[k] for k in range(N // 2)] + [pair[k] - T[k] for k in range(N // 2)]



    def _tfd_inverse(self, x):
        """Inverse FFT"""
        N = len(x)
        # Calcul de la FFT du conjugué
        tfd_conjugue = self._tfd([echantillon.conjugate() for echantillon in x])
        # Application du conjugué et normalisation
        return [ (tfd_conjugue[k].conjugate() / N).real for k in range(N) ]


    def _fenetre_hann(self, n, taille_fenetre):
        return 0.5 * (1 - math.cos(2 * math.pi * n / (taille_fenetre - 1)))


    def _normaliser(self, x):
        max_val = max(abs(num) for num in x)
        return [int((num / max_val) * 32767) for num in x]


    def reduire_bruit(self, echantillons, taille_fenetre=1024, reduction_bruit=0.5):
        """Réduction de bruit par soustraction spectrale"""
        if not self.profil_bruit:
            raise ValueError("Profil de bruit non créé")

        # Calcul du profil de bruit
        trames_bruit = self._tfc(self.profil_bruit, taille_fenetre)
        spectre_bruit = [abs(trame) for trame in trames_bruit[0]]

        # Traitement du signal
        trames_signal = self._tfc(echantillons, taille_fenetre)
        trames_nettoyees = []

        for trame in trames_signal:
            magnitude = [abs(bin) for bin in trame]
            phase = [cmath.phase(bin) for bin in trame]

            # Soustraction spectrale
            nettoye = [max(mag - reduction_bruit * bruit, 0) * cmath.exp(1j * ph)
                      for mag, bruit, ph in zip(magnitude, spectre_bruit, phase)]

            trames_nettoyees.append(nettoye)

        return self._tfc_inverse(trames_nettoyees, taille_fenetre)