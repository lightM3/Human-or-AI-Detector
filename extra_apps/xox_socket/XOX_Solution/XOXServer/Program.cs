using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;
using XOXCore;

namespace XOXServer
{
    class Program
    {
        private static TcpListener listener = null!;
        private static List<TcpClient> clients = new List<TcpClient>();
        private static XOXGame game = new XOXGame();

        static async Task Main(string[] args)
        {
            listener = new TcpListener(IPAddress.Any, 15000);
            listener.Start();
            Console.WriteLine("Sunucu 15000 portunda çalışıyor...");

            while (clients.Count < 2)
            {
                TcpClient client = await listener.AcceptTcpClientAsync();
                clients.Add(client);
                string symbol = clients.Count == 1 ? "X" : "O";
                Console.WriteLine($"Oyuncu {symbol} bağlandı.");
                
                await SendLine(client, $"BILGI|Rolün: {symbol}. Rakip bekleniyor...");
            }

            Console.WriteLine("Oyun Başlıyor!");
            await BroadcastGameStateMachine();
        }
        private static async Task BroadcastGameStateMachine()
        {
string boardStr = game.GetBoardString().Replace("\r", "").Replace("\n", "@");
            foreach (var c in clients)
            {
                await SendLine(c, $"TAHTA|{boardStr}");
            }

            if (game.CheckWin('X')) { await Broadcast("BITTI|X Kazandı!"); return; }
            if (game.CheckWin('O')) { await Broadcast("BITTI|O Kazandı!"); return; }
            if (game.CheckDraw())   { await Broadcast("BITTI|Berabere!"); return; }

            char turn = game.GetCurrentPlayer();
            TcpClient currentClient = (turn == 'X') ? clients[0] : clients[1];
            TcpClient waitingClient = (turn == 'X') ? clients[1] : clients[0];

            await SendLine(currentClient, "SORGU|Sıra sende. Hamle gir (Örn: 1,1):");
            await SendLine(waitingClient, $"BILGI|Sıra {turn} oyuncusunda. Bekleniyor...");

            await HandleMove(currentClient, turn);
        }

        private static async Task HandleMove(TcpClient client, char playerSymbol)
        {
            try
            {
                string msg = await ReadLine(client);
                if (msg.StartsWith("HAMLE|"))
                {
                    string coords = msg.Split('|')[1];
                    if (ParseMove(coords, out int r, out int c))
                    {
                        if (game.MakeMove(r, c, playerSymbol))
                        {
                            game.SwitchTurn();
                            await BroadcastGameStateMachine();
                        }
                        else
                        {
                            await SendLine(client, "BILGI|Hatalı hamle (Dolu yer).");
                            await BroadcastGameStateMachine();
                        }
                    }
                    else
                    {
                        await SendLine(client, "BILGI|Hatalı format.");
                        await BroadcastGameStateMachine();
                    }
                }
            }
            catch
            {
                Console.WriteLine("Bir oyuncu düştü.");
            }
        }

        
        private static async Task SendLine(TcpClient client, string message)
        {
            try
            {
                var writer = new StreamWriter(client.GetStream()) { AutoFlush = true };
                await writer.WriteLineAsync(message);
            }
            catch { }
        }

        private static async Task<string> ReadLine(TcpClient client)
        {
            var reader = new StreamReader(client.GetStream());
            return await reader.ReadLineAsync() ?? "";
        }

        private static async Task Broadcast(string message)
        {
            foreach (var c in clients) await SendLine(c, message);
        }

        private static bool ParseMove(string input, out int row, out int col)
        {
            row = -1; col = -1;
            var parts = input.Split(',');
            if (parts.Length == 2 && int.TryParse(parts[0], out int r) && int.TryParse(parts[1], out int c))
            {
                row = r; col = c;
                return true;
            }
            return false;
        }
    }
}