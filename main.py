from wav_file import FichierWAV
from audio_effects import EffetsAudio

def process_audio(input_file, output_file):
    wav = FichierWAV(input_file)
    wav.charger()
    
    print(f"✅ Fichier chargé : {input_file}")
    print(f"🔹 Nombre d'échantillons : {len(wav.echantillons)}")

    # Création de l'effet audio
    audio_fx = EffetsAudio(wav.echantillons)

    # Test de l'amplification avec un facteur initial de 1.0
    test_result = audio_fx.tester_amplification(1.0)

    print("\n📊 Résultats avant amplification :")
    print(f"   🔸 Max original : {test_result['max_original']}")
    print(f"   🔸 Facteur sécurisé : {test_result['facteur_securise']:.3f}")
    print(f"   🔸 Écrêtage détecté : {test_result['ecrêtage_detecte']}")

    echantillons_final = audio_fx.amplifier(test_result['facteur_securise'])

    test_result_after = audio_fx.tester_amplification(test_result['facteur_securise'])

    print("\n📊 Vérification après amplification :")
    print(f"   🔸 Max amplifié : {test_result_after['max_amplifie']}")
    print(f"   🔸 Nombre d'échantillons écrêtés : {test_result_after['nb_echantillons_ecretés']}")
    
    
    # if test_result_after['nb_echantillons_ecretés'] > 0:
    #     print("⚠️ Distorsion détectée, application de l'anti-distorsion...")
    #     audio_fx.anti_distorsion()
    #     test_result_final = audio_fx.tester_amplification(1.0)
    #     print(f"✅ Après anti-distorsion, max : {test_result_final['max_amplifie']}, écrêtage : {test_result_final['ecrêtage_detecte']}")

    # Sauvegarde du fichier amplifié
    wav.echantillons = echantillons_final
    wav.sauvegarder(output_file)
    
    print(f"\n✅ Fichier sauvegardé sous : {output_file}")

if __name__ == "__main__":
    process_audio("COMCell_Message 2 (ID 1112)_LS.wav", "output_amplified.wav")



