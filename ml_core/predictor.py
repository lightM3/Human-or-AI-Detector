import joblib
import re
import os
import sys
# Hata almamak için sklearn sınıfını açıkça import ediyoruz
from sklearn.feature_extraction.text import TfidfVectorizer

class ModelPredictor:
    def __init__(self):
        # --- DİNAMİK YOL AYARI ---
        # Şu anki dosyanın (predictor.py) olduğu klasörü bul
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Modeller bu dosya ile aynı seviyedeki 'models' klasöründe mi?
        path1 = os.path.join(current_dir, "models")
        # Yoksa bir üst dizinde mi? (Testler için)
        path2 = os.path.join(current_dir, "..", "models")
        
        if os.path.exists(path1) and os.path.exists(os.path.join(path1, "best_model.pkl")):
            self.model_path = path1
        elif os.path.exists(path2) and os.path.exists(os.path.join(path2, "best_model.pkl")):
            self.model_path = path2
        else:
            # Fallback (Varsayılan)
            self.model_path = "models/"

        print(f"📂 Modeller yükleniyor... (Konum: {self.model_path})")
        
        try:
            # 1. Vektörleştirici
            self.vectorizer = joblib.load(os.path.join(self.model_path, 'tfidf_vectorizer.pkl'))
            
            # 2. En İyi Model
            self.best_model = joblib.load(os.path.join(self.model_path, 'best_model.pkl'))
            
            # 3. Diğer 3 Model (SENİN DOSYALARINDAKİ İSİMLERLE GÜNCELLENDİ)
            # nb_model.pkl -> naive_bayes_model.pkl
            self.nb_model = joblib.load(os.path.join(self.model_path, 'naive_bayes_model.pkl'))
            
            # lr_model.pkl -> logistic_regression_model.pkl
            self.lr_model = joblib.load(os.path.join(self.model_path, 'logistic_regression_model.pkl'))
            
            # rf_model.pkl -> random_forest_model.pkl
            self.rf_model = joblib.load(os.path.join(self.model_path, 'random_forest_model.pkl'))
            
            print("✅ Tüm modeller ve vektörleştirici başarıyla yüklendi.")
            
        except FileNotFoundError as e:
            print(f"❌ HATA: Model dosyası bulunamadı! -> {e}")
            # Hata durumunda vectorizer yoksa None yapalım ki test çökmesin
            self.vectorizer = None

    def clean_text(self, text):
        """Metin temizleme (Eğitimdeki ile AYNI olmalı)"""
        if not isinstance(text, str): return ""
        text = text.lower()
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def predict(self, text):
        """
        Metni alır, temizler ve tahmin sonuçlarını döner.
        """
        if not text:
            return {"error": "Boş metin girildi."}
        
        if self.vectorizer is None:
            return {"error": "Model dosyaları yüklenemediği için tahmin yapılamıyor."}

        cleaned_text = self.clean_text(text)
        vectorized_text = self.vectorizer.transform([cleaned_text])
        
        results = {
            "main_prediction": None,  # En iyi modelin kararı
            "models_comparison": {}   # 3 modelin detaylı oranları
        }
        
        # --- 1. En İyi Model Tahmini ---
        main_pred = self.best_model.predict(vectorized_text)[0]
        results["main_prediction"] = str(main_pred)

        # --- 2. Üç Modelin Karşılaştırmalı Oranları ---
        models = {
            "Naive Bayes": self.nb_model,
            "Logistic Regression": self.lr_model,
            "Random Forest": self.rf_model
        }
        
        for name, model in models.items():
            # Tahmin edilen sınıf
            pred_class = model.predict(vectorized_text)[0]
            
            # Olasılıklar (predict_proba)
            probs = model.predict_proba(vectorized_text)[0]
            classes = list(model.classes_)
            
            # Human ve AI indekslerini bul (Hata almamak için try-except)
            try:
                ai_index = classes.index('AI')
                human_index = classes.index('Human')
            except ValueError:
                # Eğer sınıflar 0 ve 1 ise (Genelde 0:Human, 1:AI varsayımı)
                ai_index = 1
                human_index = 0
            
            results["models_comparison"][name] = {
                "prediction": str(pred_class),
                "ai_prob": float(round(probs[ai_index] * 100, 2)),
                "human_prob": float(round(probs[human_index] * 100, 2))
            }
            
        return results

# --- TEST BLOĞU ---
if __name__ == "__main__":
    predictor = ModelPredictor()
    
    ornek_metin = "Deep learning models have achieved state-of-the-art results in image recognition."
    
    if hasattr(predictor, 'vectorizer') and predictor.vectorizer:
        sonuc = predictor.predict(ornek_metin)
        
        print("\n🔎 --- TAHMİN SONUCU ---")
        print(f"🏆 ANA TAHMİN (Best Model): {sonuc.get('main_prediction')}")
        print("\n📊 DETAYLI ORANLAR:")
        comparison = sonuc.get('models_comparison', {})
        for model_name, data in comparison.items():
            print(f"   🔹 {model_name:<20}: AI %{data['ai_prob']} | Human %{data['human_prob']}")