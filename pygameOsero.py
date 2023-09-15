import pygame
import sys
import time

# ゲームボードの初期化
# 8×8の正方形を作る

OthelloBoard = 8
board = [[0] * OthelloBoard for _ in range(OthelloBoard)]

# 初期配置
# 白（2）と黒（1）のオセロを置く…何もない（0）
board[3][3] = board[4][4] = 1
# board[3][4] = 2
board[3][4] = board[4][3] = 2
board[2][4] = 3
board[4][2] = 3
board[3][5] = 3
board[5][3] = 3

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
RED = (255, 100, 100)
GREEN = (50, 200, 50)
YELLOW = (50, 200, 200)
# そこを起点に周りをすべて表す 0をx 1をy座標とする。上から時計回り
LOOKAROUND = [[0, -1], [1, -1], [1, 0],
              [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]

clock = pygame.time.Clock()
loopCounter = 0
player_turn = 1
enemy_turn = 2
skipFlg = False
font = pygame.font.Font('D:\お遊び\Othello\Othello\Font/ipaexm.ttf', 15)

# メインループ
while True:
    for event in pygame.event.get():
        # ゲーム終了
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 石を置く
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 座標の取り出し
            x, y = pygame.mouse.get_pos()
            # 座標からどこの枠をクリックしたのか割り出し
            col = x // (width // OthelloBoard)
            row = y // (height // OthelloBoard)
            # もし、石が置ける場所なら～のif文
            if board[row][col] == 3:
                skipFlg = True
                # 石を置く
                board[row][col] = player_turn
                # 石をひっくり返す
                for point in range(8):
                    try:
                        AroundPoint = board[row + LOOKAROUND[point]
                                            [0]][col + LOOKAROUND[point][1]]
                        if AroundPoint == enemy_turn:
                            lc = 2
                            while AroundPoint == enemy_turn:
                                # ループする数だけ直線方向に進んでいく
                                xmove = LOOKAROUND[point][1] * lc
                                ymove = LOOKAROUND[point][0] * lc
                                if row + ymove < 0 or col + xmove < 0:
                                    break
                                AroundPoint = board[row + ymove][col + xmove]
                                lc += 1
                            # 抜けた先が自分の石である = ひっくり返す処理が必要になる
                            if AroundPoint == player_turn:
                                lc = 1
                                # 初期位置に戻る
                                AroundPoint = board[row + LOOKAROUND[point]
                                                    [0]][col + LOOKAROUND[point][1]]
                                # 今度は敵の石をひっくり返して行く
                                while AroundPoint == enemy_turn:
                                    # ループする数だけ直線方向に進んでいく
                                    board[row + (LOOKAROUND[point][0] * lc)][col + (
                                        LOOKAROUND[point][1] * lc)] = player_turn
                                    lc += 1
                                    # 現在地の更新
                                    AroundPoint = board[row + (LOOKAROUND[point][0] * lc)][col + (
                                        LOOKAROUND[point][1] * lc)]
                    except:
                        pass

                # プレイヤーを切り替える
                player_turn = 3 - player_turn
                enemy_turn = 3 - player_turn
                # 置ける場所を割り出す
                for row2 in range(8):
                    for col2 in range(8):
                        # 置ける場所をなくす
                        if board[row2][col2] == 3:
                            board[row2][col2] = 0
                        # 石が置いていない場所ならおけるか検知する
                        if board[row2][col2] == 0:
                            for point in range(8):
                                try:
                                    AroundPoint = board[row2 + LOOKAROUND[point]
                                                        [0]][col2 + LOOKAROUND[point][1]]
                                    # 周りに相手の石がある場合、石をおける可能性がある
                                    if AroundPoint == enemy_turn:
                                        try:
                                            lc = 1
                                            while AroundPoint == enemy_turn:
                                                # ループする数だけ直線方向に進んでいく
                                                xmove = LOOKAROUND[point][1] * lc
                                                ymove = LOOKAROUND[point][0] * lc
                                                if row2 + ymove < 0 or col2 + xmove < 0:
                                                    break
                                                AroundPoint = board[row2 + (LOOKAROUND[point][0] * lc)][col2 + (
                                                    LOOKAROUND[point][1] * lc)]
                                                lc += 1
                                            # 抜け出した箇所に自分の石があればおける
                                            if AroundPoint == player_turn:
                                                board[row2][col2] = 3
                                                skipFlg = False
                                        except:
                                            # 端の場合、index outエラーをするため
                                            pass
                                except:
                                    # 端の場合、index outエラーをするため
                                    pass
                if skipFlg:
                    player_turn = 3 - player_turn
                    enemy_turn = 3 - player_turn

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
    cnt3 = 0
    for row in range(8):
        for col in range(8):
            if board[row][col] == 1:
                pygame.draw.circle(screen, BLACK, (col * cell_size + cell_size //
                                   2, row * cell_size + cell_size // 2), cell_size // 2 - 5)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, WHITE, (col * cell_size + cell_size //
                                   2, row * cell_size + cell_size // 2), cell_size // 2 - 5)
            elif board[row][col] == 3:
                screen.fill(RED,
                            (col * cell_size + 2.5,
                             row * cell_size + 2.5,
                             47.5,
                             47.5)
                            )

    # 石が置けない場合にスクリーンに文字を出す。
    if skipFlg:
        skipFlg = False
        # 置ける場所がないため、ターンが継続します。
        # fillはX座標, Y座標, Width, Height
        screen.fill(RED, (50, 150, 300, 100))
        # 描画する文字列の設定
        text = font.render("置ける場所がないため、ターンが継続します。", True, (255, 255, 255))
        # 文字列の表示位置
        screen.blit(text, [20, 150])
        pygame.display.flip()
        time.sleep(3)

    loopCounter += 1

    clock.tick(10)
    pygame.display.flip()
