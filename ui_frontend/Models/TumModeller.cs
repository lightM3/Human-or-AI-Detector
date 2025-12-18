using System.Collections.Generic;


namespace AıOrHuman.Models 
{
    // Frontend'den gelen istek
    public class TahminIstegi
    {
        // 'string?' yaparak null olabilir dedik, uyarı gitti.
        public string? Text { get; set; } 
    }

    // Python Flask'tan gelen ana cevap
    public class FlaskResponse
    {
        public string? main_prediction { get; set; } 
        public Dictionary<string, ModelDetay>? models_comparison { get; set; }
    }

    // Model detayları
    public class ModelDetay
    {
        public string? prediction { get; set; }
        public double ai_prob { get; set; }
        public double human_prob { get; set; }
    }
    
    // Frontend'e geri göndereceğimiz sonuç (ViewModel)
    public class AnalyzeResultViewModel
    {
        public double Model1_Score { get; set; }
        public double Model2_Score { get; set; }
        public double Model3_Score { get; set; }
        public string Final_Decision { get; set; } = ""; // Başlangıç değeri atadık
    }
}