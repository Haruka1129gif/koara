import math
# 評価関数
def evaluate_board(board, stone):
    weight = [
        [20, -3, 11, 11, -3, 20],
        [-3, -7, -4, -4, -7, -3],
        [11, -4,  2,  2, -4, 11],
        [11, -4,  2,  2, -4, 11],
        [-3, -7, -4, -4, -7, -3],
        [20, -3, 11, 11, -3, 20]
    ]
    score = 0
    opponent = 3 - stone
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                score += weight[y][x]
            elif board[y][x] == opponent:
                score -= weight[y][x]
    # 安定石の加点
    score += count_stable_stones(board, stone) * 10
    return score

# 安定石を数える関数
def count_stable_stones(board, stone):
    stable = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                if is_stable(board, stone, x, y, directions):
                    stable += 1
    return stable

# 石が安定しているか判定
def is_stable(board, stone, x, y, directions):
    for dx, dy in directions:
        nx, ny = x, y
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
            if board[ny][nx] != stone:
                return False
            nx += dx
            ny += dy
    return True

# FoxAI クラス
class FoxAI:
    def name(self):
        return "FoxAI"
    
    def face(self):
        return "🦊"
    
    def place(self, board, stone):
        valid_moves = get_valid_moves(board, stone)
        if not valid_moves:
            return None
        
        best_move = None
        best_score = -math.inf
        
        for x, y in valid_moves:
            temp_board = apply_move(board, stone, x, y)
            
            # 中割りをチェック
            if creates_disadvantageous_situation(temp_board, stone):
                continue
            
            # ミニマックス法で評価
            score = minimax(temp_board, 3 - stone, depth=5, maximizing_player=False)
            
            if score > best_score:
                best_score = score
                best_move = (x, y)
        
        return best_move

# 中割り回避ロジック
def creates_disadvantageous_situation(board, stone):
    opponent = 3 - stone
    valid_moves_opponent = get_valid_moves(board, opponent)
    
    # 相手が角を取れる手があれば回避
    for x, y in valid_moves_opponent:
        if (x, y) in [(0, 0), (0, len(board[0]) - 1), (len(board) - 1, 0), (len(board) - 1, len(board[0]) - 1)]:
            return True
    return False
