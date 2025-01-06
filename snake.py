import pygame
import time
import random

pygame.init()

# Định nghĩa màu
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Kích thước màn hình
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by GitHub Copilot')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 5  # Tốc độ của rắn

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(blue)
            msg = font_style.render("Bạn đã thua! Nhấn Q để thoát hoặc C để chơi lại", True, red)
            dis.blit(msg, [dis_width / 6, dis_height / 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Xử lý di chuyển tự động khi giữ chuột phải
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[2]:  # Nếu chuột phải đang được giữ
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Tính toán hướng di chuyển theo trục X
            if mouse_x > x1 + snake_block and x1_change <= 0:
                x1_change = snake_block
                y1_change = 0
            elif mouse_x < x1 - snake_block and x1_change >= 0:
                x1_change = -snake_block
                y1_change = 0

            # Tính toán hướng di chuyển theo trục Y
            if mouse_y > y1 + snake_block and y1_change <= 0:
                y1_change = snake_block
                x1_change = 0
            elif mouse_y < y1 - snake_block and y1_change >= 0:
                y1_change = -snake_block
                x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        pygame.display.update()

        # Điều kiện ăn thức ăn
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()