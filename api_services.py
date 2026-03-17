from flask import Flask, request, send_file
from rembg import remove, new_session
from PIL import Image
import io
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# RAM Dostu Küçük Model (u2netp)
# Bu satır, modelin sadece bir kez belleğe yüklenmesini sağlar
session = new_session("u2netp") 

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return {"error": "Resim yok"}, 400

    try:
        file = request.files['image']
        input_image = Image.open(file.stream)

        # Küçük modeli zorla kullanıyoruz
        output_image = remove(input_image, session=session)

        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/', methods=['GET'])
def health():
    return "Hafif Model Aktif!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)