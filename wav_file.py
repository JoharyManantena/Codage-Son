class FichierWAV:
    def __init__(self, nom_fichier=None):
        self.nom_fichier = nom_fichier
        self.en_tete = bytearray(44)
        self.echantillons = []
        self.taux_echantillonnage = 0
        self.profondeur_bits = 16
        
        self.format_en_tete = {
            'id_chunk': (0, 4),
            'taille_chunk': (4, 8),
            'format': (8, 12),
            'id_sous_chunk1': (12, 16),
            'taille_sous_chunk1': (16, 20),
            'format_audio': (20, 22),
            'nombre_canaux': (22, 24),
            'taux_echantillonnage': (24, 28),
            'taux_octets': (28, 32),
            'alignement_bloc': (32, 34),
            'profondeur_bits': (34, 36),
            'id_sous_chunk2': (36, 40),
            'taille_sous_chunk2': (40, 44)
        }

    def charger(self):
        """Charge le fichier WAV et décode l'en-tête"""
        with open(self.nom_fichier, 'rb') as f:
            donnees_brutes = f.read()
            
        # Extraction des paramètres depuis l'en-tête
        self.en_tete = donnees_brutes[:44]
        self.taux_echantillonnage = self._parser_en_tete('taux_echantillonnage')
        self.profondeur_bits = self._parser_en_tete('profondeur_bits')
        taille_donnees = self._parser_en_tete('taille_sous_chunk2')
        
        # Extraction des données audio (16 bits signés)
        self.donnees = donnees_brutes[44:44+taille_donnees]
        self.echantillons = []
        for i in range(0, len(self.donnees), 2):
            echantillon = int.from_bytes(self.donnees[i:i+2], byteorder='little', signed=True)
            self.echantillons.append(echantillon)

    def sauvegarder(self, fichier_sortie):
        """Enregistre le fichier WAV modifié"""
        # Conversion des échantillons en octets
        donnees_brutes = bytearray()
        for echantillon in self.echantillons:
            donnees_brutes += echantillon.to_bytes(2, byteorder='little', signed=True)
        
        # Mise à jour de l'en-tête
        self._mettre_a_jour_en_tete(len(donnees_brutes))
        
        # Écriture du fichier
        with open(fichier_sortie, 'wb') as f:
            f.write(self.en_tete)
            f.write(donnees_brutes)

    def _parser_en_tete(self, parametre):
        """Extrait les paramètres de l'en-tête"""
        debut, fin = self.format_en_tete[parametre]
        return int.from_bytes(self.en_tete[debut:fin], byteorder='little')

    def _mettre_a_jour_en_tete(self, nouvelle_taille_donnees):
        """Met à jour l'en-tête avec la nouvelle taille des données"""
        # Mise à jour de la taille du chunk principal (offset 4)
        taille_chunk = 36 + nouvelle_taille_donnees
        self.en_tete = self.en_tete[:4] + taille_chunk.to_bytes(4, 'little') + self.en_tete[8:]
        
        # Mise à jour de la taille des données (offset 40)
        self.en_tete = self.en_tete[:40] + nouvelle_taille_donnees.to_bytes(4, 'little') + self.en_tete[44:]