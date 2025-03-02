from wav_file import FichierWAV
from audio_effects import EffetsAudio

def process_audio(input_file, output_file):
    # Chargement du fichier
    wav = FichierWAV(input_file)
    wav.charger()

    # Instancier EffetsAudio directement avec les samples originaux
    audio_fx = EffetsAudio(wav.echantillons)

    # Déterminer le facteur d'amplification maximal sécurisé
    test_result = audio_fx.tester_amplification(1.0)
    
    # Amplification avec le facteur calculé
    echantillons_final = audio_fx.amplifier(test_result['facteur_securise'])

    # Sauvegarde
    wav.echantillons = echantillons_final
    wav.sauvegarder(output_file)

if __name__ == "__main__":
    process_audio("input.wav", "output_amplified.wav")