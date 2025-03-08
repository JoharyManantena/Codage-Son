from flask import Flask, render_template, request, send_file
import os
from wav_file import FichierWAV
from audio_effects import EffetsAudio

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "Aucun fichier fourni", 400

    file = request.files["file"]
    if file.filename == "":
        return "Aucun fichier sélectionné", 400

    # Sauvegarde du fichier original temporairement
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Chargement du fichier WAV
    wav = FichierWAV(file_path)
    wav.charger()

    # Récupération du facteur d'amplification (par défaut 1.0)
    factor = float(request.form.get("factor", 1.0))

    # Traitement d'amplification
    audio_fx = EffetsAudio(wav.echantillons)
    wav.echantillons = audio_fx.amplifier(factor)

    # Sauvegarde du fichier traité
    output_path = os.path.join(PROCESSED_FOLDER, "amplified_" + file.filename)
    wav.sauvegarder(output_path)

    return send_file(output_path, as_attachment=True, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(debug=True)
