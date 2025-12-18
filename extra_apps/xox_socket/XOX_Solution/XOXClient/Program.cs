using System;
using System.Threading.Tasks;
using XOXCore; 
using System.Net.Sockets; 
using System.IO; 

namespace XOXClient
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("=======================");
            Console.WriteLine("XOX OYUNUNA HOŞGELDİNİZ");
            Console.WriteLine("=======================");
            Console.WriteLine("Oyun Modu Seçin:");
            Console.WriteLine("1: Yerel (2 Kişilik - Aynı PC)");
            Console.WriteLine("2: Yapay Zekaya Karşı (Kolay)");
            Console.WriteLine("3: Ağda Oyna (Network/Socket)");

            string choice = Console.ReadLine() ?? "1"; 

            switch (choice)
            {
                case "1":
                    StartLocalGame();
                    break;
                case "2":
                    StartAIGame(); 
                    break;
                case "3":
                    await ConnectAndPlay(); 
                    break;
                default:
                    Console.WriteLine("Geçersiz seçim.");
                    break;
            }
        }
        
        private static void StartLocalGame()
        {
            Console.WriteLine("\n--- Yerel Oyun Başladı ---");
            XOXGame game = new XOXGame();
            
            while (true)
            {
                DisplayBoard(game.GetBoardString());
                Console.WriteLine($"Oyuncu {game.GetCurrentPlayer()} sırası. Hamlenizi girin (Satır,Sütun Örn: 0,0):");
                string input = Console.ReadLine() ?? "";
                
                if (ParseMove(input, out int row, out int col))
                {
                    if (game.MakeMove(row, col, game.GetCurrentPlayer()))
                    {
                        if (game.CheckWin(game.GetCurrentPlayer()))
                        {
                            DisplayBoard(game.GetBoardString());
                            Console.WriteLine($"Tebrikler! Oyuncu {game.GetCurrentPlayer()} kazandı.");
                            break;
                        }
                        if (game.CheckDraw())
                        {
                            DisplayBoard(game.GetBoardString());
                            Console.WriteLine("Oyun Berabere!");
                            break;
                        }
                        game.SwitchTurn();
                    }
                    else
                    {
                        Console.WriteLine("Geçersiz hamle! Lütfen boş bir kare seçin.");
                    }
                }
                else
                {
                    Console.WriteLine("Geçersiz giriş formatı. Örn: 0,0 veya 1,2");
                }
            }
            Console.WriteLine("Çıkmak için bir tuşa basın...");
            Console.ReadKey();
        }

        private static void StartAIGame()
        {
            Console.WriteLine("\n--- Bilgisayara Karşı Mod Başladı (Sen X'sin) ---");
            XOXGame game = new XOXGame();
            
            while (true)
            {
                DisplayBoard(game.GetBoardString());
                
                if (game.GetCurrentPlayer() == 'X')
                {
                    Console.WriteLine("\nSıra Sende (X). Hamle yapın (Satır,Sütun örn: 1,1):");
                    string input = Console.ReadLine() ?? "";

                    if (ParseMove(input, out int r, out int c))
                    {
                        if (game.MakeMove(r, c, 'X'))
                        {
                            if (game.CheckWin('X'))
                            {
                                DisplayBoard(game.GetBoardString());
                                Console.WriteLine("Tebrikler! KAZANDINIZ!");
                                break;
                            }
                            if (game.CheckDraw())
                            {
                                DisplayBoard(game.GetBoardString());
                                Console.WriteLine("Oyun Berabere!");
                                break;
                            }
                            game.SwitchTurn(); 
                        }
                        else
                        {
                            Console.WriteLine("Bu kare dolu! Başka bir yer seçin.");
                        }
                    }
                    else
                    {
                        Console.WriteLine("Geçersiz format! Lütfen '0,0' gibi girin.");
                    }
                }
                else
                {
                    Console.WriteLine("\nBilgisayar (O) düşünüyor...");
                    System.Threading.Thread.Sleep(1000); 

                    var (bestRow, bestCol) = AIMinimax.FindBestMove(game);
                    game.MakeMove(bestRow, bestCol, 'O');

                    if (game.CheckWin('O'))
                    {
                        DisplayBoard(game.GetBoardString());
                        Console.WriteLine("Bilgisayar Kazandı! Bir dahaki sefere...");
                        break;
                    }
                    if (game.CheckDraw())
                    {
                        DisplayBoard(game.GetBoardString());
                        Console.WriteLine("Oyun Berabere!");
                        break;
                    }
                    game.SwitchTurn(); 
                }
            }
            Console.WriteLine("Çıkmak için bir tuşa basın...");
            Console.ReadKey();
        }

        public static async Task ConnectAndPlay()
        {
            Console.Write("Sunucu IP Adresi (Boş geçersen 127.0.0.1): ");
            string ip = Console.ReadLine();
            if (string.IsNullOrWhiteSpace(ip)) ip = "127.0.0.1";
            
            int port = 15000; 

            try
            {
                using (TcpClient client = new TcpClient())
                {
                    Console.WriteLine($"Sunucuya bağlanılıyor ({ip}:{port})...");
                    await client.ConnectAsync(ip, port);
                    Console.WriteLine("Bağlandı! Oyunun başlaması bekleniyor...");

                    var reader = new StreamReader(client.GetStream());
                    var writer = new StreamWriter(client.GetStream()) { AutoFlush = true };

                    bool gameRunning = true;

                    while (gameRunning)
                    {
                        string line = await reader.ReadLineAsync();
                        if (line == null) break;

                        // KRİTİK DÜZELTME: Sadece ilk '|' işaretinden böl!
                        string[] parts = line.Split('|', 2);
                        
                        string command = parts[0];
                        string content = parts.Length > 1 ? parts[1] : "";

                        if (command == "TAHTA")
                        {
                            Console.Clear();
                            Console.WriteLine(content.Replace("@", Environment.NewLine));
                        }
                        else if (command == "BILGI")
                        {
                            Console.WriteLine($"[SUNUCU]: {content}");
                        }
                        else if (command == "SORGU")
                        {
                            Console.WriteLine($" {content}");
                            Console.Write("> ");
                            string move = Console.ReadLine() ?? "";
                            await writer.WriteLineAsync($"HAMLE|{move}");
                        }
                        else if (command == "BITTI")
                        {
                            Console.WriteLine($"\n🏁 OYUN BİTTİ: {content}");
                            gameRunning = false;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Hata: {ex.Message}");
                Console.WriteLine("Lütfen önce XOXServer uygulamasını başlattığınızdan emin olun.");
            }
            
            Console.WriteLine("Çıkmak için bir tuşa bas.");
            Console.ReadKey();
        }

        private static bool ParseMove(string input, out int row, out int col)
        {
            row = -1; col = -1;
            
            if (string.IsNullOrWhiteSpace(input)) return false;

            string[] parts = input.Split(',');
            if (parts.Length != 2) return false;

            if (int.TryParse(parts[0].Trim(), out int r) && int.TryParse(parts[1].Trim(), out int c))
            {
                row = r; 
                col = c;
                return (row >= 0 && row <= 2 && col >= 0 && col <= 2);
            }
            return false;
        }

        private static void DisplayBoard(string boardString)
        {
            Console.WriteLine("\n--- Mevcut Tahta ---");
            Console.WriteLine(boardString);
            Console.WriteLine("--------------------");
        }
    }
}