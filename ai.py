import math
BLACK = 1
WHITE = 2

# 初期の盤面
board = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

# 石を置く
def apply_move(board, stone, x, y):
    new_board = [row[:] for row in board]
    new_board[y][x] = stone
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        stones_to_flip = []
        while 0 <= nx < len(new_board[0]) and 0 <= ny < len(new_board) and new_board[ny][nx] == opponent:
            stones_to_flip.append((nx, ny))
            nx += dx
            ny += dy
        if stones_to_flip and 0 <= nx < len(new_board[0]) and 0 <= ny < len(new_board) and new_board[ny][nx] == stone:
            for flip_x, flip_y in stones_to_flip:
                new_board[flip_y][flip_x] = stone
    return new_board

# 有効な手を取得
def get_valid_moves(board, stone):
    valid_moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                valid_moves.append((x, y))
    return valid_moves

# 手を置けるかチェック
def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True
        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True
    return False

# 評価関数
def evaluate_board(board, stone):
    weight = [
    [20, -3, 11, 11, -3, 20],
    [-3, -7, -4, -4, -7, -3],
    [11, -4, 2, 2, -4, 11],
    [11, -4, 2, 2, -4, 11],
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
    score += count_stable_stones(board, stone) * 10
    return score

# 安定石を数える関数
def count_stable_stones(board, stone):
    stable = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone and is_stable(board, stone, x, y, directions):
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

# 中割り回避ロジック
def creates_disadvantageous_situation(board, stone):
    opponent = 3 - stone
    valid_moves_opponent = get_valid_moves(board, opponent)
    for x, y in valid_moves_opponent:
        if (x, y) in [(0, 0), (0, len(board[0]) - 1), (len(board) - 1, 0), (len(board) - 1, len(board[0]) - 1)]:
            return True
    return False

# ミニマックス法
def minimax(board, stone, depth, maximizing_player, alpha=-math.inf, beta=math.inf):
    valid_moves = get_valid_moves(board, stone)
    if depth == 0 or not valid_moves:
        return evaluate_board(board, stone)
    if maximizing_player:
        max_eval = -math.inf
        for x, y in valid_moves:
            new_board = apply_move(board, stone, x, y)
            eval = minimax(new_board, 3 - stone, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for x, y in valid_moves:
            new_board = apply_move(board, stone, x, y)
            eval = minimax(new_board, 3 - stone, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# FoxAI クラス
class koaraAI:
    def name(self):
        return "koaraAI"
    
    def face(self):
        return "🐨"
    
    def place(self, board, stone):
        valid_moves = get_valid_moves(board, stone)
        if not valid_moves:
            return None
        
        best_move = None
        best_score = -math.inf
        
        for x, y in valid_moves:
            temp_board = apply_move(board, stone, x, y)
            if creates_disadvantageous_situation(temp_board, stone):
                continue
            score = minimax(temp_board, 3 - stone, depth=5, maximizing_player=False)
            if score > best_score:
                best_score = score
                best_move = (x, y)
        
        return best_move
