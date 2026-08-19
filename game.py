import pygame
import sys
import os

def resource_path(relative_path):
    """Получить путь к файлу, корректно работающий в скомпилированном .exe"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
W, H = 800, 450
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Teto Mario")
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load(resource_path("kurymdik.mp3"))
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

player_img = pygame.image.load(resource_path("teto.png"))
player_img = pygame.transform.scale(player_img, (64, 64))

enemy_img = pygame.image.load(resource_path("miku.png"))
enemy_img = pygame.transform.scale(enemy_img, (64, 64))

bg_img = pygame.image.load(resource_path("bg.jpg"))
bg_img = pygame.transform.scale(bg_img, (W, H))

grass_img = pygame.image.load(resource_path("grass.jpg"))
grass_img = pygame.transform.scale(grass_img, (W, H))

p_w, p_h = 64, 64
p_x, p_y = 30, 300
speed = 5
vy = 0
g = 0.6
on_ground = False
lives = 3
score = 0
current_level = 1
invincible = False
invincible_timer = 0

cam_x = 0

# 5 УРОВНЕЙ
levels = {
    1: {
        "platforms": [(0, 400, 1200, 40), (300, 300, 150, 20), (600, 200, 150, 20), (900, 300, 150, 20)],
        "enemies": [{"x": 150, "y": 336, "w": 64, "h": 64, "dir": 1, "speed": 2},
                    {"x": 500, "y": 336, "w": 64, "h": 64, "dir": -1, "speed": 2},
                    {"x": 800, "y": 336, "w": 64, "h": 64, "dir": 1, "speed": 2}],
        "coins": [(350, 250), (400, 250), (650, 150), (700, 150), (950, 250)],
        "finish": (1100, 336, 40, 64)
    },
    2: {
        "platforms": [(0, 400, 1500, 40), (200, 300, 100, 20), (450, 200, 100, 20), (700, 300, 100, 20), (950, 200, 100, 20), (1200, 300, 100, 20)],
        "enemies": [{"x": 100, "y": 336, "w": 64, "h": 64, "dir": 1, "speed": 3},
                    {"x": 400, "y": 336, "w": 64, "h": 64, "dir": -1, "speed": 2},
                    {"x": 700, "y": 336, "w": 64, "h": 64, "dir": 1, "speed": 3},
                    {"x": 1000, "y": 336, "w": 64, "h": 64, "dir": -1, "speed": 2}],
        "coins": [(230, 250), (480, 150), (730, 250), (980, 150), (1230, 250)],
        "finish": (1400, 336, 40, 64)
    },
    3: {
        "platforms": [(0, 400, 1800, 40), (150, 320, 100, 20), (350, 240, 100, 20), (550, 160, 100, 20), (750, 240, 100, 20), (950, 320, 100, 20), (1150, 240, 100, 20), (1350, 160, 100, 20)],
        "enemies": [{"x": 80, "y": 336, "w": 64, "h": 64, "dir": 1, "speed": 3},
                    {"x": 300, "y": 336, "w": 64, "h": 64, "dir": -1, "speed": 3},
                    {"x": 600, "y": 336, "w": 64, "h": 64, "dir": 1, "speed": 2},
                    {"x": 900, "y": 336, "w": 64, "h": 64, "dir": -1, "speed": 3},
                    {"x": 1200, "y": 336, "w": 64, "h": 64, "dir": 1, "speed": 2}],
        "coins": [(180, 270), (380, 190), (580, 110), (780, 190), (980, 270), (1180, 190)],
        "finish": (1700, 336, 40, 64)
    },
    4: {
        "platforms": [(0, 400, 2000, 40), (250, 320, 100, 20), (450, 240, 100, 20), (650, 160, 100, 20), (850, 240, 100, 20), (1050, 320, 100, 20), (1250, 240, 100, 20), (1450, 160, 100, 20), (1650, 240, 100, 20)],
        "enemies": [{"x": 100, "y": 336, "w": 64, "h": 64, "dir": 1, "speed": 3},
                    {"x": 350, "y": 256, "w": 64, "h": 64, "dir": -1, "speed": 3},
                    {"x": 550, "y": 176, "w": 64, "h": 64, "dir": 1, "speed": 3},
                    {"x": 750, "y": 256, "w": 64, "h": 64, "dir": -1, "speed": 2},
                    {"x": 950, "y": 336, "w": 64, "h": 64, "dir": 1, "speed": 3},
                    {"x": 1150, "y": 256, "w": 64, "h": 64, "dir": -1, "speed": 3}],
        "coins": [(280, 270), (480, 190), (680, 110), (880, 190), (1080, 270), (1280, 190), (1480, 110)],
        "finish": (1900, 336, 40, 64)
    },
    5: {
        "platforms": [(0, 400, 2200, 40), (200, 340, 100, 20), (400, 280, 100, 20), (600, 220, 100, 20), (800, 160, 100, 20), (1000, 220, 100, 20), (1200, 280, 100, 20), (1400, 340, 100, 20), (1600, 280, 100, 20), (1800, 220, 100, 20), (2000, 160, 100, 20)],
        "enemies": [{"x": 100, "y": 336, "w": 64, "h": 64, "dir": 1, "speed": 4},
                    {"x": 300, "y": 276, "w": 64, "h": 64, "dir": -1, "speed": 4},
                    {"x": 500, "y": 216, "w": 64, "h": 64, "dir": 1, "speed": 3},
                    {"x": 700, "y": 156, "w": 64, "h": 64, "dir": -1, "speed": 4},
                    {"x": 900, "y": 216, "w": 64, "h": 64, "dir": 1, "speed": 3},
                    {"x": 1100, "y": 276, "w": 64, "h": 64, "dir": -1, "speed": 4},
                    {"x": 1300, "y": 336, "w": 64, "h": 64, "dir": 1, "speed": 3},
                    {"x": 1500, "y": 276, "w": 64, "h": 64, "dir": -1, "speed": 4}],
        "coins": [(230, 290), (430, 230), (630, 170), (830, 110), (1030, 170), (1230, 230), (1430, 290), (1630, 230), (1830, 170)],
        "finish": (2100, 336, 40, 64)
    }
}

def load_level(level_num):
    global platforms, enemies, coins, finish, level_width
    level = levels[level_num]
    platforms = level["platforms"]
    enemies = []
    for e in level["enemies"]:
        enemies.append({"rect": pygame.Rect(e["x"], e["y"], e["w"], e["h"]), "dir": e["dir"], "speed": e["speed"]})
    coins = [pygame.Rect(x, y, 16, 16) for x, y in level["coins"]]
    finish = pygame.Rect(level["finish"][0], level["finish"][1], level["finish"][2], level["finish"][3])
    level_width = max([p[0] + p[2] for p in platforms]) + 200

def reset_player():
    global p_x, p_y, vy, on_ground, invincible, invincible_timer
    p_x, p_y = 30, 300
    vy = 0
    on_ground = False
    invincible = True
    invincible_timer = pygame.time.get_ticks()

load_level(current_level)
font = pygame.font.SysFont("Arial", 40)
font_small = pygame.font.SysFont("Arial", 24)

MENU, PLAYING, GAME_OVER = 0, 1, 2
state = MENU
menu_start_time = pygame.time.get_ticks()

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if state == MENU and e.key == pygame.K_RETURN:
                state = PLAYING
                reset_player()
            if state == GAME_OVER and e.key == pygame.K_RETURN:
                state = MENU
                current_level = 1
                lives = 3
                score = 0
                load_level(current_level)
                reset_player()
                menu_start_time = pygame.time.get_ticks()

    if state == MENU:
        if pygame.time.get_ticks() - menu_start_time > 3000:
            state = PLAYING
            reset_player()

    if state == PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            p_x -= speed
        if keys[pygame.K_RIGHT]:
            p_x += speed
        if keys[pygame.K_UP] and on_ground:
            vy = -12
            on_ground = False

        vy += g
        p_y += vy

        on_ground = False
        player_rect = pygame.Rect(p_x, p_y, p_w, p_h)
        for plat in platforms:
            plat_rect = pygame.Rect(plat[0], plat[1], plat[2], plat[3])
            if player_rect.colliderect(plat_rect):
                if vy > 0 and player_rect.bottom - vy <= plat_rect.top + 10:
                    p_y = plat_rect.top - p_h
                    on_ground = True
                    vy = 0
                elif vy < 0 and player_rect.top - vy >= plat_rect.bottom - 10:
                    p_y = plat_rect.bottom
                    vy = 0

        if p_x < 0:
            p_x = 0
        if p_x + p_w > level_width:
            p_x = level_width - p_w
        if p_y > 600:
            if not invincible:
                lives -= 1
                reset_player()
                if lives <= 0:
                    state = GAME_OVER

        if invincible and pygame.time.get_ticks() - invincible_timer > 1000:
            invincible = False

        for enemy in enemies[:]:
            enemy["rect"].x += enemy["dir"] * enemy["speed"]
            if enemy["rect"].x < 50 or enemy["rect"].x > level_width - 100:
                enemy["dir"] *= -1
            if player_rect.colliderect(enemy["rect"]):
                if vy > 0 and player_rect.bottom - vy <= enemy["rect"].top + 10:
                    enemies.remove(enemy)
                    score += 100
                else:
                    if not invincible:
                        lives -= 1
                        reset_player()
                        if lives <= 0:
                            state = GAME_OVER

        for coin in coins[:]:
            if player_rect.colliderect(coin):
                coins.remove(coin)
                score += 50

        if player_rect.colliderect(finish):
            if current_level < 5:
                current_level += 1
                lives = 3
                load_level(current_level)
                reset_player()
            else:
                state = GAME_OVER

        cam_x = p_x - W // 2
        if cam_x < 0:
            cam_x = 0
        if cam_x > level_width - W:
            cam_x = level_width - W

    screen.blit(bg_img, (0, 0))
    screen.blit(grass_img, (0, 0))

    if state == MENU:
        title = font.render("TETO MARIO", True, (255, 255, 255))
        screen.blit(title, (W//2 - title.get_width()//2, 150))
        sub = font_small.render("Press ENTER or wait 3 seconds", True, (255, 255, 200))
        screen.blit(sub, (W//2 - sub.get_width()//2, 220))
        timer_text = font_small.render(f"Starting in {max(0, 3 - (pygame.time.get_ticks() - menu_start_time)//1000)}s", True, (255, 255, 200))
        screen.blit(timer_text, (W//2 - timer_text.get_width()//2, 270))
        
    elif state == PLAYING:
        for plat in platforms:
            x = plat[0] - cam_x
            if -plat[2] < x < W + 50:
                pygame.draw.rect(screen, (139, 69, 19), (x, plat[1], plat[2], plat[3]))

        for enemy in enemies:
            x = enemy["rect"].x - cam_x
            if -50 < x < W + 50:
                screen.blit(enemy_img, (x, enemy["rect"].y))

        for coin in coins:
            x = coin.x - cam_x
            if -50 < x < W + 50:
                pygame.draw.circle(screen, (255, 215, 0), (x + 8, coin.y + 8), 8)

        fx = finish.x - cam_x
        if -50 < fx < W + 50:
            pygame.draw.rect(screen, (0, 255, 0), (fx, finish.y, finish.w, finish.h))
            pygame.draw.rect(screen, (0, 200, 0), (fx + 5, finish.y + 10, finish.w - 10, finish.h - 20))

        screen.blit(player_img, (p_x - cam_x, p_y))

        text = font_small.render(f"Score: {score}  Lives: {lives}  Level: {current_level}/5", True, (255, 255, 255))
        screen.blit(text, (10, 10))

    elif state == GAME_OVER:
        s = pygame.Surface((W, H))
        s.set_alpha(180)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))
        if lives <= 0:
            go_text = font.render("GAME OVER", True, (255, 0, 0))
        else:
            go_text = font.render("YOU WIN!", True, (0, 255, 0))
        screen.blit(go_text, (W//2 - go_text.get_width()//2, 150))
        sub = font_small.render("Press ENTER to restart", True, (255, 255, 255))
        screen.blit(sub, (W//2 - sub.get_width()//2, 220))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()