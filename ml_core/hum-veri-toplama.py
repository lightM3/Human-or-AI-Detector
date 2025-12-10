import arxiv
import pandas as pd

def get_human_data(count=3000):
    client = arxiv.Client()
    
    search = arxiv.Search(
        query = "cs.AI: Yapay Zeka OR cs.CV: Bilgisayarlı Görü OR math.CO: Matematik (Kombinatorik) OR q-bio.PE: Biyoloji (Popülasyon ve Evrim) OR econ.GN: Ekonomi OR stat.ML: İstatistik OR eess.SP: Elektrik Mühendisliği (Sinyal İşleme)",
        max_results = count,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )

    data = []
    print(f"{count} adet makale farklı konulardan çekiliyor...")
    
    for result in client.results(search):
        # Özet metnini al ve satır sonlarını temizle
        text = result.summary.replace("\n", " ") 
        data.append({
            "text": text,
            "label": "Human" # İnsan yazımı olarak etiketle
        })
        
    return pd.DataFrame(data)

# Fonksiyonu çalıştır ve kaydet
if __name__ == "__main__":
    df_human = get_human_data(3000)
    # Veriyi CSV olarak kaydet
    df_human.to_csv("human_data.csv", index=False)
    print("İşlem tamam! 'human_data_cesitli.csv' dosyası oluşturuldu.")