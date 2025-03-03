class EffetsAudio:
    def __init__(self, echantillons, profondeur_bits=16):
        self.echantillons = echantillons
        self.profondeur_bits = int(profondeur_bits)

    def _get_limits(self):
        """Calcule les limites maximale et minimale en fonction de la profondeur."""
        val_max = (1 << (self.profondeur_bits - 1)) - 1
        val_min = - (1 << (self.profondeur_bits - 1))
        return val_min, val_max

    def amplifier(self, facteur):
        """Amplifie les échantillons avec un facteur donné en évitant l'écrêtage."""
        val_min, val_max = self._get_limits()
        return [int(max(min(s * facteur, val_max), val_min)) for s in self.echantillons]

    def tester_amplification(self, facteur):
        """
        Teste l'amplification et retourne plusieurs statistiques :
         - max_original : valeur absolue maximale du signal original
         - max_amplifie : valeur absolue maximale du signal amplifié (sans limitation)
         - ecrêtage_detecte : booléen indiquant si l'amplification dépasserait les limites
         - nb_echantillons_ecretés : nombre d'échantillons qui dépasseraient les bornes
         - facteur_securise : facteur maximum sécurisé pour éviter l'écrêtage
        """
        val_min, val_max = self._get_limits()
        if self.echantillons:
            max_original = max(abs(s) for s in self.echantillons)
        else:
            max_original = 1  # éviter la division par zéro

        echantillons_test = [s * facteur for s in self.echantillons]
        max_amplifie = max(abs(s) for s in echantillons_test) if echantillons_test else 0

        # Vérification de l'écrêtage
        ecrêtage = any(s < val_min or s > val_max for s in echantillons_test)
        nb_echantillons_ecretés = sum(1 for s in echantillons_test if s < val_min or s > val_max)

        return {
            'max_original': max_original,
            'max_amplifie': max_amplifie,
            'ecrêtage_detecte': ecrêtage,
            'nb_echantillons_ecretés': nb_echantillons_ecretés,
            'facteur_securise': val_max / max_original if max_original else 1.0
        }

    def anti_distorsion(self, seuil=30000):
        """Réduit la distorsion en appliquant une compression douce aux échantillons écrêtés"""
        val_max = 32767
        val_min = -32768

        def compresser(s):
            if s > seuil:
                return int(seuil + (s - seuil) * 0.5)  # Compression douce des valeurs trop élevées
            elif s < -seuil:
                return int(-seuil + (s + seuil) * 0.5)  # Compression douce des valeurs trop basses
            return s

        self.echantillons = [compresser(s) for s in self.echantillons]