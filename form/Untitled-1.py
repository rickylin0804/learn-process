import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 設置遊戲窗口
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Plane")

# 加載圖像
plane_image = pygame.image.load(r"C:\\Users\\ricky\\OneDrive\\桌面\\資訊學習歷程\\assets\\plane.png")
bird_image = pygame.image.load(r"C:\\Users\\ricky\\OneDrive\\桌面\\資訊學習歷程\\assets\\bird.png")

# 調整圖像大小
plane_image = pygame.transform.scale(plane_image, (70, 50))
bird_image = pygame.transform.scale(bird_image, (50, 50))

# 飛機初始位置和速度
plane_x = screen_width // 2
plane_y = screen_height - plane_image.get_height() - 10
plane_speed = 10

# 鳥類列表（用於存儲多個鳥類）
birds = []
bird_speed_y = 5
bird_speed_x_range = (-3, 3)  # 水平速度範圍
bird_spawn_delay = 2000  # 每 2000 毫秒生成一隻鳥
last_bird_spawn_time = pygame.time.get_ticks()
difficulty_increase_interval = 5000  # 每 5000 毫秒增加一次難度
last_difficulty_increase_time = pygame.time.get_ticks()

# 遊戲的顏色
background_color = (135, 206, 235)  # 天藍色

# 計分
score = 0
font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def game_over():
    game_over_font = pygame.font.Font(None, 74)
    text = game_over_font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (200, 250))
    pygame.display.update()
    pygame.time.wait(2000)
    sys.exit()

# 主循環
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 檢查按鍵狀態
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and plane_x - plane_speed > 0:
        plane_x -= plane_speed
    if keys[pygame.K_RIGHT] and plane_x + plane_speed < screen_width - plane_image.get_width():
        plane_x += plane_speed

    # 每隔一段時間生成一隻鳥
    current_time = pygame.time.get_ticks()
    if current_time - last_bird_spawn_time > bird_spawn_delay:
        bird_x = random.randint(0, screen_width - bird_image.get_width())
        bird_y = -bird_image.get_height()
        bird_speed_x = random.randint(*bird_speed_x_range)
        birds.append([bird_x, bird_y, bird_speed_x])
        last_bird_spawn_time = current_time

    # 增加遊戲難度
    if current_time - last_difficulty_increase_time > difficulty_increase_interval:
        bird_spawn_delay = max(500, bird_spawn_delay - 200)  # 最小間隔 500 毫秒
        bird_speed_y += 1
        bird_speed_x_range = (bird_speed_x_range[0] - 1, bird_speed_x_range[1] + 1)
        last_difficulty_increase_time = current_time

    # 更新鳥類位置
    for i, (bird_x, bird_y, bird_speed_x) in enumerate(birds):
        bird_y += bird_speed_y
        bird_x += bird_speed_x
        if bird_x < 0 or bird_x > screen_width - bird_image.get_width():
            bird_speed_x = -bird_speed_x  # 碰到邊緣改變方向
        birds[i] = [bird_x, bird_y, bird_speed_x]
        if bird_y > screen_height:
            score += 1
            birds.pop(i)

    # 填充背景色
    screen.fill(background_color)

    # 繪製飛機
    screen.blit(plane_image, (plane_x, plane_y))

    # 繪製鳥類
    for bird_x, bird_y, bird_speed_x in birds:
        screen.blit(bird_image, (bird_x, bird_y))

    # 繪製計分
    draw_text(f"Score: {score}", font, (0, 0, 0), screen, 10, 10)

    # 碰撞檢測
    plane_rect = plane_image.get_rect(topleft=(plane_x, plane_y))
    for bird_x, bird_y, bird_speed_x in birds:
        bird_rect = bird_image.get_rect(topleft=(bird_x, bird_y))
        if plane_rect.colliderect(bird_rect):
            game_over()

    pygame.display.update()
    pygame.time.Clock().tick(30)  # 控制遊戲更新速率
