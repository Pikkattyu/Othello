import pygame
import sys

# ゲームボードの初期化
# 8×8の正方形を作る
board = [[0] * 8 for _ in range(8)]

# 初期配置
# 白（2）と黒（1）のオセロを置く…何もない（0）
board[3][3] = board[4][4] = 1
board[3][4] = board[4][3] = 2

# ゲーム初期化
pygame.init()
# 画面のサイズ
size = width, height = 400, 400
screen = pygame.display.set_mode(size)
# タイトル
pygame.display.set_caption("オセロゲーム")

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)

clock = pygame.time.Clock()
loopCounter = 0
player_turn = 1

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // (width // 8)
            row = y // (height // 8)
            if board[row][col] == 0:
                # 石を置く
                board[row][col] = player_turn
                # プレイヤーを切り替える
                player_turn = 3 - player_turn

    # ゲームボードを描画
    screen.fill(GREEN)

    # 枠を置く
    for row in range(8):
        pygame.draw.line(screen, BLACK, (0, width / 8 * row),
                         (400, width / 8 * row), 5)
    for col in range(8):
        pygame.draw.line(screen, BLACK, (width / 8 * col, 0),
                         (width / 8 * col, 400), 5)

    # オセロ石を置く
    cell_size = width // 8
    for row in range(8):
        for col in range(8):
            if board[row][col] == 1:
                pygame.draw.circle(screen, BLACK, (col * cell_size + cell_size //
                                   2, row * cell_size + cell_size // 2), cell_size // 2 - 5)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, WHITE, (col * cell_size + cell_size //
                                   2, row * cell_size + cell_size // 2), cell_size // 2 - 5)

    clock.tick(10)
    pygame.display.flip()
