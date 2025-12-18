using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json; 
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using AıOrHuman.Models;
using System;

namespace AıOrHuman.Controllers

{
    public class HomeController : Controller
    {
        private readonly HttpClient _httpClient;

        public HomeController(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Analyze([FromBody] TahminIstegi istek)
        {
            if (string.IsNullOrEmpty(istek.Text)) return Json(new { error = "Metin boş olamaz." });

            string flaskUrl = "http://127.0.0.1:5000/predict"; 

            var jsonContent = new StringContent(
                JsonConvert.SerializeObject(new { text = istek.Text }), 
                Encoding.UTF8, "application/json");

            try 
            {
                var response = await _httpClient.PostAsync(flaskUrl, jsonContent);

                if (response.IsSuccessStatusCode)
                {
                    var responseString = await response.Content.ReadAsStringAsync();
                    
                    // Python'dan gelen karmaşık JSON'u çözüyoruz
                    var flaskData = JsonConvert.DeserializeObject<FlaskResponse>(responseString);
                    

               

                    double score1 = 0, score2 = 0, score3 = 0;

                    if(flaskData.models_comparison.ContainsKey("Naive Bayes"))
                        score1 = flaskData.models_comparison["Naive Bayes"].ai_prob / 100.0;

                    if(flaskData.models_comparison.ContainsKey("Logistic Regression"))
                        score2 = flaskData.models_comparison["Logistic Regression"].ai_prob / 100.0;
                    
                    if(flaskData.models_comparison.ContainsKey("Random Forest"))
                        score3 = flaskData.models_comparison["Random Forest"].ai_prob / 100.0;

                    // Frontend'e temiz, basit veri gönderiyoruz
                    return Json(new {
                        model1_score = score1, // Naive Bayes
                        model2_score = score2, // Logistic Regression (Frontend'de başlığı güncelle!)
                        model3_score = score3, // Random Forest
                        final_decision = flaskData.main_prediction // "AI" veya "Human"
                    });
                }
                else
                {
                    return Json(new { error = "API Hatası: " + response.StatusCode });
                }
            }
            catch (Exception ex)
            {
                return Json(new { error = "Bağlantı Hatası: " + ex.Message });
            }
        }
    }
}