def reveal(x, y, board, revealed, flags, screen):
    if not in_board(x,y,board) or revealed[x][y]:
        return True
    if board[x][y]:
        show_mines(x, y, board, screen, flags)
        return False
    global revealed_count
    revealed_count += 1
    count = count_mines(x, y, board)
    show_count(x, y, count, screen)
    revealed[x][y] = True
    if (x,y) in flags:
        flag.remove((x,y)) 
    if count == 0:
        for a in range(x-1,x+2):
            for b in range(y-1,y+2):
                reveal(a, b, board, revealed, flags, screen)
    return True

def in_board(x, y, board):
    return x < len(board) and x >= 0 and y < len(board[0]) and y >= 0

def count_mines(x, y, board):
    count = 0
    for a in range(x-1,x+2):
        for b in range(y-1,y+2):
            if in_board(a,b,board) and board[a][b]:
                count += 1
    return count

import pygame
import random
#board has num_mines many mines which are all hidden at the beginning
def init_board(n, m, num_mines, height = 1080, width = 720):

    def make_mines(n, m, num_mines):
        coordinates = [] 
        for i in range(n):
            for j in range(m):
                coordinates.append((i,j))
        board = [[0 for i in range(m)] for j in range(n)]
        for i in range(num_mines):
            index = random.randint(0,n*m-1-i)
            x, y = coordinates[index]
            board[x][y] = 1
            coordinates[index] = coordinates[len(coordinates)-1-i]
        return board
    board = make_mines(n, m, num_mines)

    def display_board(n, m, height, width):
        pygame.init()
        image = pygame.image.load("unrevealed.png")
        global length
        length = min(width//n, height//m)
        image = pygame.transform.scale(image, (length, length))
        screen = pygame.display.set_mode((n*length,m*length))
        pygame.display.set_icon(pygame.image.load("mine.png"))
        for i in range(n):
            for j in range(m):
                screen.blit(image, (i*length, j*length))
        return screen

    screen = display_board(n, m, width, height)
    revealed = [[0 for i in range(m)] for j in  range(n)]
    return (board, revealed, screen)

def show_count(x, y, count, screen):
    global length
    image = pygame.image.load(str(count) + ".png")
    image = pygame.transform.scale(image, (length, length))
    screen.blit(image,(x*length, y*length))

def show_mines(x, y, board, screen, flags):
    global length
    clicked_mine = pygame.transform.scale(pygame.image.load("clicked_mine.png"), (length, length))
    mine = pygame.transform.scale(pygame.image.load("mine.png"), (length, length))
    false_flag = pygame.transform.scale(pygame.image.load("false_flag.png"), (length,length))
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] and (i,j) not in flags:
                screen.blit(mine, (i*length, j*length))
            elif not board[i][j] and (i, j) in flags:
                screen.blit(false_flag, (i*length, j*length))
    screen.blit(clicked_mine, (x*length, y*length))

A = True
n = 40
m = 30
num_mines = (n*m)//8
revealed_count = 0
is_clicking = False
board, revealed, screen = init_board(n, m, num_mines)
flags = set()
unrevealed_image = pygame.transform.scale(pygame.image.load("unrevealed.png"), (length,length))
flag_image = false_flag = pygame.transform.scale(pygame.image.load("flag.png"), (length,length))
empty_image = pygame.transform.scale(pygame.image.load("0.png"), (length,length))
just_flagged = False
B = True
while A:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            A = False
            B = False
    if not is_clicking and pygame.mouse.get_pressed()[0]:
        is_clicking = True
        x, y = pygame.mouse.get_pos()
        x //= length
        y //= length
        if (x, y) in flags or revealed[x][y]:
            is_clicking = False
            continue
        screen.blit(empty_image,(x*length,y*length))
    if is_clicking and not pygame.mouse.get_pressed()[0]:
        is_clicking = False
        a, b = pygame.mouse.get_pos()
        a //= length
        b //= length
        if a == x and b == y:
            A = reveal(x, y, board, revealed, flags, screen)
        else:
            screen.blit(unrevealed_image,(x*length,y*length))
    if pygame.mouse.get_pressed()[2]:
        if not just_flagged:
            just_flagged = True
            x, y = pygame.mouse.get_pos()
            x //= length
            y //= length
            if revealed[x][y]:
                continue
            if (x,y) not in flags:
                flags.add((x,y))
                print(num_mines-len(flags))
                screen.blit(flag_image,(x*length,y*length))
            else:
                flags.remove((x,y))
                print(num_mines-len(flags))
                screen.blit(unrevealed_image,(x*length,y*length))
    else:
        just_flagged = False
    if revealed_count == n*m-num_mines:
        A = False
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] and (i, j) not in flags:
                    flags.add((i,j))
                    screen.blit(flag_image,(i*length,j*length))
    pygame.display.flip()
    
while B:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            B = False
pygame.quit()

