from wav_file import FichierWAV
from audio_effects import EffetsAudio

def process_audio(input_file, output_file):
    # Chargement du fichier
    wav = FichierWAV(input_file)
    wav.charger()

    audio_fx = EffetsAudio(wav.echantillons)
    test_result = audio_fx.tester_amplification(1.0)
    
    echantillons_final = audio_fx.amplifier(test_result['facteur_securise'])

    # Sauvegarde
    wav.echantillons = echantillons_final
    wav.sauvegarder(output_file)

if __name__ == "__main__":
    process_audio("input.wav", "output_amplified.wav")