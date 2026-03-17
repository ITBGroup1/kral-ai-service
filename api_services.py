from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # PHP sunucundan gelen isteklere izin verir

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return {"error": "Resim dosyası bulunamadı!"}, 400

    try:
        # Gelen resmi oku
        file = request.files['image']
        input_image = Image.open(file.stream)

        # Arka planı sil (rembg motoru burada çalışır)
        output_image = remove(input_image)

        # Sonucu belleğe (RAM) kaydet (Disk doldurmaz, hızlıdır)
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/', methods=['GET'])
def health_check():
    return "AI Servisi Aktif ve Calisiyor! - Kral Studio", 200

if __name__ == "__main__":
    # Render.com veya diğer sunucuların dinamik port ataması için:
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' her yerden erişime açar (Render için şart)
    app.run(host='0.0.0.0', port=port)