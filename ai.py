import math
def evaluate_board_with_middle(board, stone):
    """
    中割りを考慮した評価関数。
    石数を抑える戦略を取り入れ、相手に角を取らせるリスクを軽減する。
    """
    # 位置ごとの重み付け
    weight = [
        [10, -5, 5, 5, -5, 10],
        [-5, -5, 1, 1, -5, -5],
        [5, 1, 0, 0, 1, 5],
        [5, 1, 0, 0, 1, 5],
        [-5, -5, 1, 1, -5, -5],
        [10, -5, 5, 5, -5, 10]
    ]
    # 評価値を計算
    score = 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                score += weight[y][x]
            elif board[y][x] == 3 - stone:
                score -= weight[y][x]
    # 石数が多すぎる場合に評価を下げる
    stone_count = sum(row.count(stone) for row in board)
    score -= stone_count * 0.5  # 石を多く取りすぎるとペナルティ
    return score

def minimax_with_middle(board, stone, depth, maximizing_player, alpha=-math.inf, beta=math.inf):
    """
    中割りを考慮したミニマックス法。
    """
    valid_moves = get_valid_moves(board, stone)
    # 終端条件: 深さ0またはこれ以上石を置けない場合
    if depth == 0 or not valid_moves:
        return evaluate_board_with_middle(board, stone)
    if maximizing_player:
        max_eval = -math.inf
        for x, y in valid_moves:
            new_board = apply_move(board, stone, x, y)
            eval = minimax_with_middle(new_board, 3 - stone, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # βカット
        return max_eval
    else:
        min_eval = math.inf
        for x, y in valid_moves:
            new_board = apply_move(board, stone, x, y)
            eval = minimax_with_middle(new_board, 3 - stone, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # αカット
        return min_eval

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
            score = minimax_with_middle(temp_board, 3 - stone, depth=5, maximizing_player=False)
            # 中割りを考慮して最良手を選択
            if score > best_score:
                best_score = score
                best_move = (x, y)
        return best_move
