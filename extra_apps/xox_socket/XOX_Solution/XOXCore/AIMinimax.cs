using System;

namespace XOXCore
{
    public static class AIMinimax
    {
        // Puanlama: AI kazanırsa 10, Oyuncu kazanırsa -10, Beraberlik 0
        private static int Evaluate(char[,] board)
        {
            // Satır/Sütun Kontrolü
            for (int i = 0; i < 3; i++)
            {
                if (board[i, 0] == board[i, 1] && board[i, 1] == board[i, 2])
                {
                    if (board[i, 0] == 'O') return 10;
                    if (board[i, 0] == 'X') return -10;
                }
                if (board[0, i] == board[1, i] && board[1, i] == board[2, i])
                {
                    if (board[0, i] == 'O') return 10;
                    if (board[0, i] == 'X') return -10;
                }
            }
            // Diyagonal Kontrolü
            if (board[0, 0] == board[1, 1] && board[1, 1] == board[2, 2])
            {
                if (board[0, 0] == 'O') return 10;
                if (board[0, 0] == 'X') return -10;
            }
            if (board[0, 2] == board[1, 1] && board[1, 1] == board[2, 0])
            {
                if (board[0, 2] == 'O') return 10;
                if (board[0, 2] == 'X') return -10;
            }
            return 0; // Kimse kazanmadı
        }

        // Tahtanın dolu olup olmadığını (Beraberlik) kontrol eder
        private static bool IsMovesLeft(char[,] board)
        {
            for (int i = 0; i < 3; i++)
                for (int j = 0; j < 3; j++)
                    if (board[i, j] == ' ')
                        return true;
            return false;
        }

        // Minimax Algoritmasının Temel Özyinelemeli Fonksiyonu
        public static int Minimax(char[,] board, int depth, bool isMaximizer)
        {
            int score = Evaluate(board);

            if (score == 10) return score - depth; // AI kazandı
            if (score == -10) return score + depth; // Oyuncu kaybetti
            if (IsMovesLeft(board) == false) return 0; // Beraberlik

            if (isMaximizer)
            {
                int best = -1000;
                for (int i = 0; i < 3; i++)
                {
                    for (int j = 0; j < 3; j++)
                    {
                        if (board[i, j] == ' ')
                        {
                            board[i, j] = 'O'; // Hamle yap
                            best = Math.Max(best, Minimax(board, depth + 1, !isMaximizer));
                            board[i, j] = ' '; // Hamleyi geri al
                        }
                    }
                }
                return best;
            }
            else
            {
                int best = 1000;
                for (int i = 0; i < 3; i++)
                {
                    for (int j = 0; j < 3; j++)
                    {
                        if (board[i, j] == ' ')
                        {
                            board[i, j] = 'X'; // Hamle yap
                            best = Math.Min(best, Minimax(board, depth + 1, !isMaximizer));
                            board[i, j] = ' '; // Hamleyi geri al
                        }
                    }
                }
                return best;
            }
        }

        // En iyi hamleyi döndüren ana fonksiyon
        public static (int row, int col) FindBestMove(XOXGame game)
        {
            char[,] board = game.GetBoardMatrix(); // XOXGame sınıfına bu metodu ekleyin
            int bestVal = -1000;
            int bestRow = -1;
            int bestCol = -1;

            for (int i = 0; i < 3; i++)
            {
                for (int j = 0; j < 3; j++)
                {
                    if (board[i, j] == ' ')
                    {
                        board[i, j] = 'O';
                        int moveVal = Minimax(board, 0, false);
                        board[i, j] = ' ';

                        if (moveVal > bestVal)
                        {
                            bestRow = i;
                            bestCol = j;
                            bestVal = moveVal;
                        }
                    }
                }
            }
            return (bestRow, bestCol);
        }
    }
}