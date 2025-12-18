from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# --- ÖNEMLİ: ml_core klasörünü Python yoluna ekle ---
# Bu sayede yan klasördeki predictor.py dosyasını import edebiliriz.
current_dir = os.path.dirname(os.path.abspath(__file__))
ml_core_path = os.path.join(current_dir, '..')
sys.path.append(ml_core_path)

# Predictor sınıfını çağır
try:
    from ml_core.predictor import ModelPredictor
except ImportError as e:
    print(f"HATA: ml_core modülü bulunamadı. Lütfen klasör yapısını kontrol edin. Detay: {e}")
    sys.exit(1)

# Flask Uygulamasını Başlat
app = Flask(__name__)
CORS(app)  # Frontend'den (React/HTML) gelen isteklere izin ver

# Modeli Hafızaya Yükle (Uygulama başlarken 1 kere çalışır)
print("⏳ API Başlatılıyor, modeller yükleniyor...")
predictor = ModelPredictor()
print("✅ API Hazır! İstek bekliyor...")

@app.route('/', methods=['GET'])
def home():
    """API'nin ayakta olduğunu kontrol etmek için basit endpoint"""
    return jsonify({
        "status": "running",
        "message": "Human or AI Detection API is active.",
        "endpoints": {
            "POST /predict": "Send JSON {'text': '...'} to get prediction."
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Ana Tahmin Endpoint'i
    Girdi: JSON {"text": "Analiz edilecek metin..."}
    Çıktı: JSON (Tahmin sonuçları)
    """
    try:
        # Gelen JSON verisini al
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Lütfen JSON formatında 'text' parametresi gönderin."}), 400
        
        input_text = data['text']
        
        # ml_core içindeki predictor ile tahmin yap
        result = predictor.predict(input_text)
        
        # Eğer predictor hata döndürdüyse (örn: boş metin)
        if "error" in result:
            return jsonify(result), 400
            
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Sunucu Hatası: {str(e)}"}), 500

if __name__ == '__main__':
    # Sunucuyu başlat (Port 5000)
    app.run(debug=True, host='0.0.0.0', port=5000)