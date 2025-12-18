namespace XOXCore
{
    public class XOXGame
    {
        private char[,] board = new char[3, 3];
        private char currentPlayer = 'X';

        public XOXGame()
        {
            for (int i = 0; i < 3; i++)
                for (int j = 0; j < 3; j++)
                    board[i, j] = ' ';
        }

        public char GetCurrentPlayer()
        {
            return currentPlayer;
        }

        public void SwitchTurn()
        {
            currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
        }

        public bool MakeMove(int row, int col, char player)
        {
            if (row < 0 || row > 2 || col < 0 || col > 2 || board[row, col] != ' ' || player != currentPlayer)
            {
                return false;
            }
            board[row, col] = player;
            return true;
        }

        public bool CheckWin(char player)
        {
            for (int i = 0; i < 3; i++)
            {
                if ((board[i, 0] == player && board[i, 1] == player && board[i, 2] == player) ||
                    (board[0, i] == player && board[1, i] == player && board[2, i] == player))
                {
                    return true;
                }
            }
            if ((board[0, 0] == player && board[1, 1] == player && board[2, 2] == player) ||
                (board[0, 2] == player && board[1, 1] == player && board[2, 0] == player))
            {
                return true;
            }
            return false;
        }

        public bool CheckDraw()
        {
            for (int i = 0; i < 3; i++)
                for (int j = 0; j < 3; j++)
                    if (board[i, j] == ' ')
                        return false; 
            
            return !CheckWin('X') && !CheckWin('O');
        }

        public char[,] GetBoardMatrix()
        {
            return (char[,])board.Clone();
        }

public string GetBoardString()
{
    var sb = new System.Text.StringBuilder();
    
    // Üst kısım: Sütun Numaraları (0 1 2)
    sb.AppendLine("     0   1   2"); 
    sb.AppendLine("   +---+---+---+");

    for (int i = 0; i < 3; i++)
    {
        // Sol kısım: Satır Numarası (0 1 2)
        sb.Append($" {i} |"); 
        
        for (int j = 0; j < 3; j++)
        {
            sb.Append($" {board[i, j]} ");
            sb.Append("|");
        }
        sb.AppendLine();
        sb.AppendLine("   +---+---+---+");
    }
    return sb.ToString();
}
    }
}