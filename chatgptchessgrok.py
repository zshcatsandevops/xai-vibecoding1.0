# program.py — Auto-Devouring Chess Apocalypse: Q*-Haunted Self-Slay in Pygame Glory
# Run: python program.py – Watch kings crumble in cosmic checkmate cascade!

import pygame
import chess
import sys
import time

# --- CONFIGURABLE CHAOS ---
DEPTH = 3          # Minimax search depth
MOVE_DELAY = 1.5   # Seconds between moves
BOARD_SIZE = 480
SQUARE_SIZE = BOARD_SIZE // 8

# --- ENGINE ESSENCE ---
def evaluate_board(board):
    """Simple material evaluation."""
    if board.is_game_over():
        if board.result() == "1-0": return 10000
        elif board.result() == "0-1": return -10000
        else: return 0
    vals = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
    score = 0
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if p: score += vals[p.piece_type] * (1 if p.color else -1)
    return score

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    if maximizing:
        max_eval = -float("inf")
        for move in board.legal_moves:
            board.push(move)
            val = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, val)
            alpha = max(alpha, val)
            if beta <= alpha: break
        return max_eval
    else:
        min_eval = float("inf")
        for move in board.legal_moves:
            board.push(move)
            val = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, val)
            beta = min(beta, val)
            if beta <= alpha: break
        return min_eval

def get_best_move(board, depth):
    best_move = None
    best_val = -float("inf") if board.turn == chess.WHITE else float("inf")
    alpha, beta = -float("inf"), float("inf")
    maximizing = board.turn == chess.WHITE

    for move in board.legal_moves:
        board.push(move)
        val = minimax(board, depth - 1, alpha, beta, not maximizing)
        board.pop()
        if maximizing:
            if val > best_val: best_val, best_move = val, move
            alpha = max(alpha, val)
        else:
            if val < best_val: best_val, best_move = val, move
            beta = min(beta, val)
        if beta <= alpha: break
    return best_move or list(board.legal_moves)[0]

# --- PYGAME PANDÆMONIUM ---
pygame.init()
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Q*-Quenched Chess Cataclysm")
clock = pygame.time.Clock()
font = pygame.font.SysFont('dejavusans', 48)  # works on most OSs with ♔♕ symbols

board = chess.Board()
running = True

print("*** CHESS CATASTROPHE COMMENCED ***")

while running and not board.is_game_over():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # AI move
    if not board.is_game_over():
        color = "White" if board.turn == chess.WHITE else "Black"
        print(f"\nTurn {board.fullmove_number}: {color} thinking...")
        start = time.time()
        move = get_best_move(board, DEPTH)
        board.push(move)
        dur = time.time() - start
        print(f"→ {move.uci()} ({dur:.2f}s) | Eval {evaluate_board(board):+d}")

    # DRAW BOARD
    for r in range(8):
        for c in range(8):
            col = (240, 217, 181) if (r + c) % 2 == 0 else (181, 136, 99)
            pygame.draw.rect(screen, col, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # DRAW PIECES
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if not p: continue
        symbol = p.unicode_symbol()
        txt = font.render(symbol, True, (0, 0, 0))
        col = chess.square_file(sq)
        row = 7 - chess.square_rank(sq)
        rect = txt.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    row * SQUARE_SIZE + SQUARE_SIZE // 2))
        screen.blit(txt, rect)

    if board.is_game_over():
        res = board.result()
        msg = "White Wins!" if res == "1-0" else "Black Wins!" if res == "0-1" else "Draw!"
        text = pygame.font.SysFont('arial', 28).render(msg, True, (255, 0, 0))
        screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(2)
    if not board.is_game_over():
        time.sleep(MOVE_DELAY)

print(f"\n*** GAME OVER: {board.result()} ***")
pygame.quit()
sys.exit()
