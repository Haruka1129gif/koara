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
        if (x, y) in [(0, 0), (0, len(board[0]) - 1), (len(board) - 1, 0), (len(board[0]) - 1, len(board) - 1)]:
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

# プレイヤーの番を進める関数
def play_turn(board, stone, player_ai):
    """
    現在のプレイヤーの番を実行し、置けない場合はスキップします。
    """
    valid_moves = get_valid_moves(board, stone)
    if not valid_moves:
        # 手がない場合はスキップ
        print(f"{player_ai.face()} は置ける場所がないためスキップします。")
        return False  # 番をスキップした場合は False を返す

    # AIが手を選ぶ
    x, y = player_ai.place(board, stone)
    if (x, y) is None or (x, y) not in valid_moves:
        print(f"{player_ai.face()} は置けない場所 {(x, y)} を選びました。反則負けです。")
        return True  # 不正手の場合はゲーム終了
    # 手を適用する
    board = apply_move(board, stone, x, y)
    print(f"{player_ai.face()} は {(x, y)} に置きました。")
    return True  # 正常に手を進めた場合は True を返す

# メインのゲームループ
def run_othello(black_ai, white_ai):
    """
    オセロゲームを実行します。
    """
    current_board = [row[:] for row in board]  # 初期の盤面をコピー
    current_turn = BLACK  # 黒から開始
    players = {BLACK: black_ai, WHITE: white_ai}

    while True:
        # 現在のプレイヤーを取得
        current_player = players[current_turn]

        # プレイヤーの番を実行
        moved = play_turn(current_board, current_turn, current_player)

        if moved is None:  # 不正手があればゲーム終了
            print(f"{current_player.face()} の反則によりゲーム終了です。")
            break

        # 手が打てた場合は次のプレイヤーへ
        if moved:
            current_turn = 3 - current_turn  # 黒⇔白を切り替え

        # 両者が置けない場合はゲーム終了
        if not get_valid_moves(current_board, BLACK) and not get_valid_moves(current_board, WHITE):
            print("どちらも置ける場所がありません。ゲーム終了です。")
            break

    # 最終結果を表示
    black_count = sum(row.count(BLACK) for row in current_board)
    white_count = sum(row.count(WHITE) for row in current_board)
    print(f"ゲーム終了: 黒 {black_count}, 白 {white_count}")
    if black_count > white_count:
        print(f"黒 {black_ai.face()} の勝利です！")
    elif black_count < white_count:
        print(f"白 {white_ai.face()} の勝利です！")
    else:
        print("引き分けです！")

# ゲーム実行
run_othello(koaraAI(), koaraAI())
