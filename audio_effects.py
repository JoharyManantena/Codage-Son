class EffetsAudio:
    def __init__(self, echantillons):
        self.echantillons = echantillons  # Stocker les échantillons dans l'instance

    def amplifier(self, facteur, profondeur_bits=16):
        """Amplifie les échantillons avec un facteur donné en évitant l'écrêtage"""
        val_max = (1 << (int(profondeur_bits) - 1)) - 1
        val_min = - (1 << (int(profondeur_bits) - 1))

        return [int(max(min(s * facteur, val_max), val_min)) for s in self.echantillons]

    def tester_amplification(self, facteur):
        """Teste l'amplification et retourne les statistiques"""
        max_original = max(abs(s) for s in self.echantillons) if self.echantillons else 1
        echantillons_test = [s * facteur for s in self.echantillons]
        max_amplifie = max(abs(s) for s in echantillons_test)

        ecrêtage = max_amplifie > 32767
        return {
            'max_original': max_original,
            'max_amplifie': max_amplifie,
            'ecrêtage_detecte': ecrêtage,
            'facteur_securise': 32767 / max_original if max_original else 1.0
        }