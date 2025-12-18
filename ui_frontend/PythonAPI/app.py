from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# --- ÖNEMLİ DEĞİŞİKLİK BURADA ---
# ml_core klasörü olmadığı için sys.path eklemelerine gerek kalmadı.
# Direkt yanındaki dosyadan import ediyoruz.
try:
    from predictor import ModelPredictor
except ImportError as e:
    print(f"HATA: predictor.py dosyası bulunamadı! Detay: {e}")
    sys.exit(1)

# Flask Uygulamasını Başlat
app = Flask(__name__)
CORS(app) 

# Modeli Hafızaya Yükle
print("⏳ API Başlatılıyor, modeller yükleniyor...")
predictor = ModelPredictor()
print("✅ API Hazır! İstek bekliyor...")

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "running", "message": "API Aktif."})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Lütfen 'text' parametresi gönderin."}), 400
        
        input_text = data['text']
        
        # Tahmin yap
        result = predictor.predict(input_text)
        
        if "error" in result:
            return jsonify(result), 400
            
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Sunucu Hatası: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)