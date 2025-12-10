import google.generativeai as genai
import pandas as pd
import time
import random
import os

GOOGLE_API_KEY = "AIzaSyD8FeMk8w75sbf1KazNoyY3g7nAtt5QEuA"
genai.configure(api_key=GOOGLE_API_KEY)

MODEL_LISTESI = [
    'models/gemini-2.5-flash',
    'models/gemini-2.0-flash',
    'models/gemini-2.0-flash-001',
    'models/gemini-2.0-flash-lite-preview-02-05',
    'models/gemini-pro',
    'models/gemini-1.5-pro-latest'
]

current_model_index = 0

def get_active_model():
    """Listeden sıradaki modeli getirir."""
    global current_model_index
    if current_model_index >= len(MODEL_LISTESI):
        print("❌ TÜM MODELLERİN KOTASI DOLDU! Yeni bir API Key veya yarına kadar beklemeniz gerekiyor.")
        return None
    
    model_name = MODEL_LISTESI[current_model_index]
    print(f"🔄 Model değiştiriliyor... Yeni Hedef: {model_name}")
    return genai.GenerativeModel(model_name)


model = get_active_model()

konular = [
    "Quantum Physics", "Machine Learning", "Bioinformatics", 
    "Economic Game Theory", "Computer Vision", "Renewable Energy",
    "Signal Processing", "Astrophysics", "Cyber Security", "Robotics",
    "Molecular Biology", "Digital History", "Climate Change Models",
    "Psychology of AI", "Nano Materials", "Urban Planning", "Genetics"
]

dosya_adi = "ai_data.csv"
ai_data = []
mevcut_sayi = 0
hedef_sayi = 3000 

# 1. KALDIĞIMIZ YERDEN DEVAM ETME
if os.path.exists(dosya_adi):
    try:
        df_eski = pd.read_csv(dosya_adi)
        ai_data = df_eski.to_dict('records')
        mevcut_sayi = len(ai_data)
        print(f"📂 Mevcut dosya bulundu: {mevcut_sayi} veri.")
        print(f"🚀 Kaldığımız yerden devam ediyoruz...")
    except:
        print("Dosya okunamadı, sıfırdan başlanıyor.")

print(f"HEDEF: {hedef_sayi}. Çıkış: CTRL+C")

try:
    while mevcut_sayi < hedef_sayi:
        try:
            if model is None:
                break

            konu = random.choice(konular)
            
            
            prompt = (f"Write 5 distinct and different academic abstracts (approx. 100 words each) "
                      f"about {konu}. Do not use titles. "
                      f"Separate each abstract ONLY with the string '|||'. Do not number them.")
            
            response = model.generate_content(prompt)
            
            if response.text:
                partiler = response.text.split('|||')
                
                for p in partiler:
                    temiz_p = p.replace("\n", " ").strip()
                    if len(temiz_p) > 50:
                        ai_data.append({"text": temiz_p, "label": "AI"})
                        mevcut_sayi += 1
                
                print(f"✅ {mevcut_sayi}/{hedef_sayi} (Model: {MODEL_LISTESI[current_model_index]})")

                # Her 50 veride bir KAYDET
                if mevcut_sayi % 50 == 0:
                    pd.DataFrame(ai_data).to_csv(dosya_adi, index=False)
                    print(f"💾 Otomatik kayıt...")
                
                time.sleep(3) 
                    
        except Exception as e:
            hata_mesaji = str(e)
            
            if "429" in hata_mesaji or "quota" in hata_mesaji.lower():
                print(f"⚠️ KOTA DOLDU ({MODEL_LISTESI[current_model_index]}). Sıradaki modele geçiliyor...")
                current_model_index += 1
                model = get_active_model()
                time.sleep(5)
            else:
                print(f"⚠️ Hata: {e}")
                time.sleep(10)

except KeyboardInterrupt:
    print("\n🛑 DURDURULDU! Kaydediliyor...")

finally:
    if len(ai_data) > 0:
        df_ai = pd.DataFrame(ai_data).head(hedef_sayi)
        df_ai.to_csv(dosya_adi, index=False)
        print(f"✅ SON DURUM: {len(df_ai)} veri kaydedildi.")