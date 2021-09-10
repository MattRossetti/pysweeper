import pygame
import random
import os
pygame.font.init()

# Global vars for square parameteres
SQUARES_LENGTH = 25
SQUARES_MIN = 5
SQUARES_MAX = 99

# Global Vars for Background Creation
BORDER = 10  # Border Thickness
GRID = 3  # Grid Thickness
TEXT_AREA_HEIGHT = 40

# PyGame global Vars
FPS = 60
GAME_FONT = pygame.font.SysFont('calibri', 20, bold = True)
SQUARE_FONT = pygame.font.SysFont('calibri', SQUARES_LENGTH, bold = True)
BUTTON_FONT = pygame.font.SysFont('calibri', 50, bold = True)


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = ('#FF0000')
L_GREY = ('#C5C5C5')
M_GREY = ('#808080')
D_GREY = ('#696969')
COLOR_ARR = ['#1395D6','#14A946', '#CD2020', '#251066', '#661026', '#501066', ' #665010', '#000000']

#images
FLAG_IMAGE = pygame.image.load(os.path.join('Assets', 'flag.png'))
FLAG = pygame.transform.scale(FLAG_IMAGE, (20, 20))

class Square:

    def __init__(self, square, square_id, coords, clicked, checkered, is_bomb, is_flag, neighbor_bombs):
        self.square = square
        self.square_id = square_id
        self.coords = coords
        self.clicked = clicked
        self.checkered = checkered
        self.is_bomb = is_bomb
        self.is_flag = is_flag
        self.neighbor_bombs = neighbor_bombs

def draw_background(screen, game_lens, square_cnts, game_area_coords):
    screen.fill(BLACK)

    # draw text area (ta)
    ta_x = BORDER
    ta_y = BORDER
    ta_width = game_lens[0]
    ta_height = TEXT_AREA_HEIGHT
    text_area = pygame.Rect(ta_x, ta_y, ta_width, ta_height)
    pygame.draw.rect(screen, WHITE, text_area)

    #draw game area
    ga_x = game_area_coords[0]
    ga_y = game_area_coords[1]
    game_area = pygame.Rect(ga_x, ga_y, game_lens[0], game_lens[1])
    pygame.draw.rect(screen, WHITE, game_area)

    # draw game grid
    x_shift = 0
    v_x1 = ga_x + SQUARES_LENGTH + GRID / 2
    v_x2 = ga_x + SQUARES_LENGTH + GRID / 2
    v_y1 = ga_y
    v_y2 = ga_y + game_lens[1]
    for i in range(square_cnts[0]):
        v_xy1 = (v_x1 + x_shift, v_y1)
        v_xy2 = (v_x2 + x_shift, v_y2)
        pygame.draw.line(screen, BLACK, (v_xy1), (v_xy2), GRID)
        x_shift += SQUARES_LENGTH + GRID

    y_shift = 0
    h_x1 = ga_x
    h_x2 = ga_x + game_lens[0]
    h_y1 = ga_y + SQUARES_LENGTH + GRID / 2
    h_y2 = ga_y + SQUARES_LENGTH + GRID / 2
    for j in range(square_cnts[1]):
        h_xy1 = (h_x1, h_y1 + y_shift)
        h_xy2 = (h_x2, h_y2 + y_shift)
        pygame.draw.line(screen, BLACK, (h_xy1), (h_xy2), GRID)
        y_shift += SQUARES_LENGTH + GRID


def create_squares(squares_cnts, game_area_coords):
    squares = []
    square_id = 0
    checkered = True
    for i in range(squares_cnts[0]):
        if is_even(i): checkered = True
        else: checkered = False
        for j in range(squares_cnts[1]):
            sq_x = game_area_coords[0] + (SQUARES_LENGTH + GRID) * i
            sq_y = game_area_coords[1] + (SQUARES_LENGTH + GRID) * j
            square = pygame.Rect(sq_x, sq_y, SQUARES_LENGTH, SQUARES_LENGTH)
            squares.append(Square(square, square_id, (i, j), False, checkered, False, False, 0))
            checkered = not checkered
            square_id += 1
    return squares


def is_even(num):
    if (num % 2) == 0: return True
    else: return False


def draw_squares(screen, squares):
    lose = False
    for square in squares:
        if square.clicked == True:
            if square.is_bomb == False:
                color = L_GREY
                bomb_number = str(square.neighbor_bombs)
                text_color = COLOR_ARR[square.neighbor_bombs - 1]
            else:
                lose = True
                square.clicked = False

        elif square.checkered: color = M_GREY
        else: color = D_GREY
        pygame.draw.rect(screen, color, square.square)

        if square.clicked == True:
            if square.neighbor_bombs != 0 and square.is_bomb == False:
                square_text = SQUARE_FONT.render(f'{bomb_number}', 1, text_color)
                screen.blit(square_text, (square.square.left + GRID * 2, square.square.top + GRID* .5))
            else:
                neighbors = get_neighbors(square, squares)
                for neighbor in neighbors:
                    neighbor.clicked = True

        if square.is_flag == True and square.clicked == False:
            screen.blit(FLAG, (square.square.left + GRID, square.square.top + GRID* .5))
    
    if lose == True:
        lose_animation(screen, squares)
        return True
    
    return False


def draw_text(screen, bombs, game_lens):
    game_text = GAME_FONT.render(f'BOMBS: {bombs}', 1, BLACK)
    screen.blit(game_text, (20, 22))


def timer_text(screen, game_time, game_lens):
    if game_time == 0: time_to_print = GAME_FONT.render('TIMER: ' + str(0), 1, BLACK)
    else: time_to_print = GAME_FONT.render('TIMER: ' + str((pygame.time.get_ticks() - game_time) // 1000), 1, BLACK)
    screen.blit(time_to_print, (game_lens[0] - 100 ,22))


def handle_mouse(left, right, click_coords, squares):
    if left and not right:
        click = 'left'
    if not left and right:
        click = 'right'
    if left and right:
        click = 'both'
    for square in squares:
        if square.square.collidepoint(click_coords):
            return (click, square.square_id)
    return (click, -1)


def handle_click(clicked_square, squares, bombs):
    neighbor_bombs = squares[clicked_square[1]].neighbor_bombs
    neighbor_flags = 0
    win = False
    if clicked_square[0] == 'left':
        if squares[clicked_square[1]].is_flag == False:
            squares[clicked_square[1]].clicked = True
    if clicked_square[0] == 'right' and squares[clicked_square[1]].clicked == False:
        if squares[clicked_square[1]].is_flag == True:
            squares[clicked_square[1]].is_flag = False
            bombs += 1
        else:
            squares[clicked_square[1]].is_flag = True
            bombs -= 1        
    if clicked_square[0] == 'both':
        neighbors = get_neighbors(squares[clicked_square[1]], squares)
        for neighbor in neighbors:
            print('check', neighbor.square_id, neighbor.is_flag)
            if neighbor.is_flag: neighbor_flags += 1 
        if neighbor_bombs == neighbor_flags:
            for neighbor in neighbors:
                if neighbor.is_flag == False:
                    neighbor.clicked = True
    print(clicked_square, neighbor_bombs, neighbor_flags)
    print(bombs)
    if bombs == 0:
        print('win', bombs)
        win = win_check(squares)
        print(win)
    return (squares, bombs, win)

def win_check(squares):
    print()
    correct_bomb_cnt = 0 #delete later
    for square in squares:
        if square.is_flag and square.is_bomb:
            correct_bomb_cnt += 1
        elif not square.clicked:
            return False
    return True


def lose_animation(screen, squares):
    lose_time = pygame.time.get_ticks()
    all_bomb_squares = []
    handled = True
    for square in squares:
        if square.is_bomb: all_bomb_squares.append(square)
    random.shuffle(all_bomb_squares)
    count = 0
    while True:
        try:
            if current_ticks != pygame.time.get_ticks() and current_ticks != None:
                handled = False
        except UnboundLocalError:
            current_ticks = 0
            print(1)
            pass
        current_ticks = pygame.time.get_ticks()
        if (pygame.time.get_ticks() - lose_time) % 50 == 0 and handled == False:
            pygame.draw.rect(screen, RED, all_bomb_squares[count].square)
            pygame.display.update()
            count += 1
            handled = True
            print(count)

        if count >= len(all_bomb_squares):
            break

def new_game_start(start_screen, click_coords):
    # returns difficulty and tuple for custom game
    difficulty = ''
    start_screen.fill(BLACK)
    start_text1 = GAME_FONT.render('Welcome to PySweeper!', 1, WHITE)
    start_text2 = GAME_FONT.render('Please Select Difficulty', 1, WHITE)
    start_screen.blit(start_text1, (25, 15))
    start_screen.blit(start_text2, (25, 38))
    easy_border = pygame.Rect(23, 73, 254, 54)
    easy_button = pygame.Rect(25, 75, 250, 50)
    easy_text = BUTTON_FONT.render('EASY', 1, COLOR_ARR[1])
    pygame.draw.rect(start_screen, COLOR_ARR[1], easy_border)
    pygame.draw.rect(start_screen, L_GREY, easy_button)
    start_screen.blit(easy_text, (100, 78))
    medium_border = pygame.Rect(23, 148, 254, 54)
    medium_button = pygame.Rect(25, 150, 250, 50)
    medium_text = BUTTON_FONT.render('MEDIUM', 1, COLOR_ARR[0])
    pygame.draw.rect(start_screen, COLOR_ARR[0], medium_border)
    pygame.draw.rect(start_screen, M_GREY, medium_button)
    start_screen.blit(medium_text, (55, 153))
    hard_border = pygame.Rect(23, 223, 254, 54)
    hard_button = pygame.Rect(25, 225, 250, 50)
    hard_text = BUTTON_FONT.render('HARD', 1, COLOR_ARR[2])
    pygame.draw.rect(start_screen, COLOR_ARR[2], hard_border)
    pygame.draw.rect(start_screen, D_GREY, hard_button)
    start_screen.blit(hard_text, (95, 228))
    pygame.display.update()

    buttons = [easy_button, medium_button, hard_button]
    for i in range(len(buttons)):
        if buttons[i].collidepoint(click_coords):
            if i == 0: difficulty = 'Easy'
            elif i == 1: difficulty = 'Medium'
            elif i == 2: difficulty = 'Hard'

    return difficulty

def win_screen(start_screen, win_time, difficulty, click_coords):
    event = '-1'
    start_screen.fill(BLACK)
    win_text1 = GAME_FONT.render('Wow! you just won!', 1, WHITE)
    win_text2 = GAME_FONT.render(f'{difficulty} defeated!', 1, WHITE)
    win_text3 = GAME_FONT.render(f'Time: {win_time}!', 1, WHITE)
    start_screen.blit(win_text1, (25, 15))
    start_screen.blit(win_text2, (25, 38))
    start_screen.blit(win_text3, (25, 61))
    new_game_border = pygame.Rect(23, 148, 254, 54)
    new_game_button = pygame.Rect(25, 150, 250, 50)
    new_game_text = BUTTON_FONT.render('NEW GAME', 1, COLOR_ARR[0])
    pygame.draw.rect(start_screen, COLOR_ARR[0], new_game_border)
    pygame.draw.rect(start_screen, M_GREY, new_game_button)
    start_screen.blit(new_game_text, (29, 153))
    quit_border = pygame.Rect(23, 223, 254, 54)
    quit_button = pygame.Rect(25, 225, 250, 50)
    quit_text = BUTTON_FONT.render('QUIT', 1, COLOR_ARR[1])
    pygame.draw.rect(start_screen, COLOR_ARR[2], quit_border)
    pygame.draw.rect(start_screen, D_GREY, quit_button)
    start_screen.blit(quit_text, (100, 227))

    buttons = [new_game_button, quit_button]
    for i in range(len(buttons)):
        if buttons[i].collidepoint(click_coords):
            event = i

    pygame.display.update()
    return event

def lose_screen(start_screen, click_coords):
    event = '-1'
    start_screen.fill(BLACK)
    lose_text1 = GAME_FONT.render('Uh Oh!', 1, WHITE)
    lose_text2 = GAME_FONT.render(f'PySweeper has beat you!', 1, WHITE)
    lose_text3 = GAME_FONT.render(f'Try Better Next time!', 1, WHITE)
    start_screen.blit(lose_text1, (25, 15))
    start_screen.blit(lose_text2, (25, 38))
    start_screen.blit(lose_text3, (25, 61))
    new_game_border = pygame.Rect(23, 148, 254, 54)
    new_game_button = pygame.Rect(25, 150, 250, 50)
    new_game_text = BUTTON_FONT.render('NEW GAME', 1, COLOR_ARR[0])
    pygame.draw.rect(start_screen, COLOR_ARR[0], new_game_border)
    pygame.draw.rect(start_screen, M_GREY, new_game_button)
    start_screen.blit(new_game_text, (30, 153))
    quit_border = pygame.Rect(23, 223, 254, 54)
    quit_button = pygame.Rect(25, 225, 250, 50)
    quit_text = BUTTON_FONT.render('QUIT', 1, COLOR_ARR[1])
    pygame.draw.rect(start_screen, COLOR_ARR[2], quit_border)
    pygame.draw.rect(start_screen, D_GREY, quit_button)
    start_screen.blit(quit_text, (100, 227))

    buttons = [new_game_button, quit_button]
    for i in range(len(buttons)):
        if buttons[i].collidepoint(click_coords):
            event = i

    pygame.display.update()
    return event

    


def set_bomb_attributes(squares_cnts, clicked_square, squares, bombs):
    # defines is_bomb for each square randomble
    # excluding clicked square and neighbors
    eligible_bombs = []
    uneligible_bombs = [clicked_square[1]]
    first_click_neighbors = get_neighbors(squares[clicked_square[1]], squares)
    for neighbor in first_click_neighbors:
        uneligible_bombs.append(neighbor.square_id)
    for i in range(0, squares_cnts[0] * squares_cnts[1]):
        if i not in uneligible_bombs:
            eligible_bombs.append(i)
    bomb_ids = random.sample(eligible_bombs, bombs)
    for square in squares:
        if square.square_id in bomb_ids:
            square.is_bomb = True
            square.neighbor_bombs = 0
        
    # defines neighbor_bombs for each square
    for square in squares:
        neighbors = get_neighbors(square, squares)
        for neighbor in neighbors:
            if neighbor.is_bomb:
                square.neighbor_bombs += 1

    squares[clicked_square[1]].clicked = True
    return squares


def get_neighbors(square, squares):
    neighbor_squares = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            x, y = square.coords[0] + i, square.coords[1] + j
            for neighbor in squares:
                if neighbor.coords == (x, y) and (i, j) != (0, 0):
                    neighbor_squares.append(neighbor)
    return neighbor_squares


def main():
    
    pygame.display.set_caption('PySweeper')

    start_screen = pygame.display.set_mode((300, 300))

    left = False
    right = False
    both = False
    click_time = 0
    time_dif = 0
    click_coords = (0,0)
    click = False
    clicked_square = ('', -1)
    first_click = True
    game_timer = 0
    playing = False
    win = False
    lose = False


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left = True
                    click = True
                    click_coords = event.pos
                    click_time = pygame.time.get_ticks()
                if event.button == 3:
                    right = True
                    click = True
                    click_coords = event.pos
                    click_time = pygame.time.get_ticks()
        
        if playing == False and win == False and lose == False:
            if left == True:
                print(click_coords)
                left = click = False

            difficulty = new_game_start(start_screen, click_coords)
            if difficulty == '':
                pass
            else:
                game_timer = 0
                if difficulty == 'Easy':
                    bombs = 10
                    squares_cnt_x = 8
                    squares_cnt_y = 8
                elif difficulty == 'Medium':
                    bombs = 40
                    squares_cnt_x = 16
                    squares_cnt_y = 16
                elif difficulty == 'Hard':
                    bombs = 99
                    squares_cnt_x = 30
                    squares_cnt_y = 16
                else: print('error')

                print(bombs, squares_cnt_x, squares_cnt_y)
                squares_cnts = (squares_cnt_x, squares_cnt_y)
                if squares_cnt_x < SQUARES_MIN or squares_cnt_x > SQUARES_MAX:
                    print('squares_cnt_x value invalid')
                if squares_cnt_y < SQUARES_MIN or squares_cnt_y > SQUARES_MAX:
                    print('square_cnt_y value invalid')
                game_len_x = (squares_cnts[0] * SQUARES_LENGTH
                                + ((squares_cnts[0] - 1) * GRID)) 
                game_len_y = (squares_cnts[1] * SQUARES_LENGTH
                                + ((squares_cnts[1] - 1) * GRID))
                game_lens = (game_len_x, game_len_y)
                game_area_x = BORDER
                game_area_y = BORDER * 2 + TEXT_AREA_HEIGHT
                game_area_coords = (game_area_x, game_area_y)
                width = BORDER * 2 + game_len_x
                height = BORDER * 3 + TEXT_AREA_HEIGHT + game_len_y
                screen = pygame.display.set_mode((width, height))
                squares = create_squares(squares_cnts, game_area_coords) 
                playing = True 

                  



        elif playing == True and win == False:
            draw_background(screen, game_lens, squares_cnts, game_area_coords)
            draw_text(screen, bombs, game_lens)
            lose = draw_squares(screen, squares)
            if lose: click_coords = (0,0)                

            
            time_dif = pygame.time.get_ticks() - click_time
            if click and time_dif > 75:
                clicked_square = handle_mouse(left, right, click_coords, squares)
                left = right = click = False
                time_dif = 0

            if clicked_square[1] != -1:
                if clicked_square[0] == 'left' and first_click:
                    print(clicked_square)
                    squares = set_bomb_attributes(squares_cnts, clicked_square, squares, bombs)
                    first_click = False
                    game_timer = pygame.time.get_ticks()
                elif clicked_square[0] == 'right' and first_click:
                    pass
                elif clicked_square[0] == 'both' and first_click:
                    pass
                else:
                    click_return = handle_click(clicked_square, squares, bombs)
                    squares = click_return[0]
                    bombs = click_return[1]
                    win = click_return[2]
                    if win: click_coords = (0,0)
                clicked_square = ('', -1)

            timer_text(screen, game_timer, game_lens)

            pygame.display.update()

        if lose:
            playing = False
            start_screen = pygame.display.set_mode((300, 300))
            lose_event = lose_screen(start_screen,click_coords)
            if lose_event == 0:
                lose_event = -1
                lose = False
                click_coords = (0,0)
                first_click = True
            elif lose_event == 1:
                lose_event = -1
                pygame.quit()


        if win:
            playing = False
            win_time = game_timer // 1000
            start_screen = pygame.display.set_mode((300, 300))
            event = win_screen(start_screen, win_time, difficulty, click_coords)
            print(event)
            if event == 0:
                event = -1
                win = False
                click_coords = (0,0)
                first_click = True
            elif event == 1:
                event = -1
                pygame.quit()

    pygame.quit()

if __name__ == '__main__':
    main()