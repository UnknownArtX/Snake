import pygame
import sys
import random
import pygame_menu
import sqlite3
pygame.init()

#size_Display = [950, 900]
SIZE_BLOCK = 35
COUNT_BLOCK = 20
MARGIN = 1
HEADER_MARGIN = 70
size = (SIZE_BLOCK * COUNT_BLOCK + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCK, 
        SIZE_BLOCK * COUNT_BLOCK + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCK + HEADER_MARGIN)


FRAME_COLOR = (0, 255, 204)
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
SNAKE_COLOR = (1, 102, 0)
HEADER_COLOR = (0, 202, 153)
RED = (224, 0, 0)

courier = pygame.font.SysFont('Calibri', 36)
timer = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')

class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def is_inside(self):
        return 0<=self.x<=COUNT_BLOCK-1 and 0<=self.y<=COUNT_BLOCK-1
    
    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y

def start_the_game(): 
    user_name = user_input.get_value()

    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCK-1)
        y = random.randint(0, COUNT_BLOCK-1)
        Empty_Block = SnakeBlock(x, y)
        while Empty_Block in snake_blocks:
            Empty_Block.x = random.randint(0, COUNT_BLOCK-1)
            Empty_Block.y = random.randint(0, COUNT_BLOCK-1)
        return Empty_Block

    def draw_block(color, raw, column):
        pygame.draw.rect(screen, color, (SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column+1), 
                                        HEADER_MARGIN + SIZE_BLOCK + raw * SIZE_BLOCK + MARGIN * (raw+1), 
                                        SIZE_BLOCK, SIZE_BLOCK))   
    
    snake_blocks = [SnakeBlock(9,8), SnakeBlock(9,9), SnakeBlock(9,10)]
    apple = get_random_empty_block()
    d_raw = buf_raw = 0
    d_col = buf_col = 1
    total = 0
    speed = 2

    while True:
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                with sqlite3.connect('Player.db') as db:
                    cursor = db.cursor()
                    query = f""" INSERT INTO Players (name, Count) VALUES ('{user_name}, {total}') """
                    cursor.execute(query)
                    db.commit()
                print('Exit')
                sys.exit()
            elif Event.type == pygame.KEYDOWN:
                if Event.key == pygame.K_UP and buf_col != 0:
                    buf_raw = -1
                    buf_col = 0
                elif Event.key == pygame.K_DOWN and buf_col != 0:
                    buf_raw = 1
                    buf_col = 0
                elif Event.key == pygame.K_LEFT and buf_raw != 0:
                    buf_raw = 0
                    buf_col = -1
                elif Event.key == pygame.K_RIGHT and buf_raw != 0:
                    buf_raw = 0
                    buf_col = 1
                
        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        text_total = courier.render(f'Ваш счет: {total}', 0, WHITE)
        text_speed = courier.render(f'Ваша скорость: {speed}', 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK+200, SIZE_BLOCK))

        for raw in range(COUNT_BLOCK):
            for column in range(COUNT_BLOCK):
                if (raw+column)%2 == 0:
                    color = BLUE
                else:
                    color = WHITE
                draw_block(color, raw, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print('You lose')
            with sqlite3.connect('Player.db') as db:
                cursor = db.cursor()
                query = f""" INSERT INTO Players (name, Count) VALUES ('{user_name}', {total}) """
                cursor.execute(query)
                db.commit()
            db_select()
            break


        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if apple == head:
            total += 1
            speed = total//5 + 1
            snake_blocks.append(apple)
            apple = get_random_empty_block()

        d_raw = buf_raw
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_raw, head.y + d_col)

        if new_head in snake_blocks:
            print('You lose')
            with sqlite3.connect('Player.db') as db:
                cursor = db.cursor()
                query = f""" INSERT INTO Players (name, Count) VALUES ('{user_name}', {total}) """
                cursor.execute(query)
                db.commit()
            db_select()
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(2+speed)



name_generate = random.randint(0, 10000)
menu = pygame_menu.Menu('Snake', size[0], size[1], theme=pygame_menu.themes.THEME_BLUE)

user_input = menu.add.text_input('Ваше имя: ', default=f'Player{name_generate}')
menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)
menu.add.label('')
menu.add.label('')
def db_select():
    con = sqlite3.connect("Player.db")
    cursor = con.cursor()
    query = cursor.execute("""SELECT * FROM Players ORDER BY count DESC LIMIT 5""")
    response = query.fetchall()
    for index in response:
        menu.add.label(f'Игрок {index[1]} со счетом {index[2]}')
            
db_select()

menu.mainloop(screen)