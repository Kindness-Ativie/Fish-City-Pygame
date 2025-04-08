import pygame
from pygame import Rect
from random import randrange, choice

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1200
screen_height = 750

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Fish City')

# classes
class Enemy:
    def __init__(self, image, height, speed):
        self.image = image
        self.height = height
        self.speed = speed
        self.pos = image.get_rect().move(0, height)

    def move(self):
        self.pos = self.pos.move(self.speed, 1)
        if self.pos.right > screen_width - 20:
            self.pos.left = 0

    def collide(self, player_r):
        if player_r.colliderect(self.pos):
            return True


# player
player = pygame.image.load('assets/images/clown-fish.png')
pygame.display.set_icon(player)  # sets game window icon using player variable
dead_player = pygame.image.load('assets/images/fish-bone.png')
dead_player_rect = dead_player.get_rect()
dead_player_rect.x = 2000
dead_player_rect.y = 2000
player_left = pygame.transform.flip(player, True, False)
player_right = pygame.transform.flip(player, False, False)
player_rect = player.get_rect()
player_rect.x = screen_width / 2  # starting x
player_rect.y = screen_height - 70  # starting y
player_speed = 10

danger_zone = Rect(0, screen_height - 150, screen_width, 200)
player_alive = True

# bullet set up
bullet_img = pygame.image.load('assets/images/paintball.png')
bullet = pygame.transform.rotate(bullet_img, 90)
bullet_rect = bullet.get_rect()
bullet_rect.x = 0
bullet_rect.y = screen_height - 70
bullet_x_change = 0
bullet_y_change = 60
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))


# star and lightning set up
lightning_img = pygame.image.load('assets/images/lightning_strike.png')
star_image = pygame.image.load('assets/images/pixel_star.png')
star_img = choice([star_image, lightning_img])
star_rect = star_img.get_rect()

star_state = "fire"
star_y_change = 25


def star_fall(x, y):
    global star_state
    star_state = "fire"
    screen.blit(star_img, (x + 16, y + 10))


# levels and scores
level = 1
points = 0
more_enemies = 5
top_enemy_speed = 5

# enemy set up
enemy1_image = pygame.image.load('assets/images/donut.png')
enemy2_image = pygame.image.load('assets/images/red_monster.png')
enemy3_image = pygame.image.load('assets/images/slime.png')
enemy4_image = pygame.image.load('assets/images/technology.png')
enemy5_image = pygame.image.load('assets/images/squid_alien.png')
enemy6_image = pygame.image.load('assets/images/one_eyed_purple.png')
enemy7_image = pygame.image.load('assets/images/angry_ufo.png')
enemy8_image = pygame.image.load('assets/images/red_monster.png')
enemy9_image = pygame.image.load('assets/images/starship.png')
all_enemy_images = [enemy1_image, enemy2_image, enemy3_image, enemy4_image, enemy5_image]
upper_level_aliens = [enemy6_image, enemy7_image, enemy8_image, enemy9_image]
upper_level_idx = 0

enemies = []
num_of_each_enemy = 5
for num in range(num_of_each_enemy):
    enemy_img = choice(all_enemy_images)
    opponent_1 = Enemy(enemy_img, randrange(0, 5) * randrange(50, 100), randrange(1, top_enemy_speed) * randrange(13, 25))
    enemies.append(opponent_1)


# ----------------------- FUNCTIONS -------------------------
# scales and blits your bg! Enter true if it's already scaled!
def static_background(image_path, scaled=False):
    screen_surface = pygame.image.load(image_path)
    if scaled is False:
        scaled_surface = pygame.transform.scale(screen_surface, (screen_width, screen_height))
        screen.blit(scaled_surface, (0, 0))
    else:
        screen.blit(screen_surface, (0, 0))


# uses center
def text_on_screen_center(text: str, font_path, font_size, color, surface, x_pos, y_pos):
    display_font = pygame.font.Font(font_path, font_size)
    text_render = display_font.render(text, 1, color)
    text_rect = text_render.get_rect(center=(x_pos, y_pos))
    surface.blit(text_render, text_rect)


# uses top left vs center
def text_on_screen(text: str, font_path, font_size, color, surface, x_pos, y_pos):
    display_font = pygame.font.Font(font_path, font_size)
    text_render = display_font.render(text, 1, color)
    text_rect = text_render.get_rect()
    text_rect.topleft = (x_pos, y_pos)
    surface.blit(text_render, text_rect)


game_running = True
while game_running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
    static_background('assets/images/neon_city.jpg')
    text_on_screen(f'POINTS: {points}', 'assets/fonts/poxel-font.ttf', 30, 'white', screen, 50, 20)
    text_on_screen(f'LEVEL {level}', 'assets/fonts/poxel-font.ttf', 30, 'white', screen, screen_width - 300, 20)
    text_on_screen_center(f'FISH CITY', 'assets/fonts/Pixel-Regular.ttf', 30, 'white', screen, screen_width / 2, 50)

    # checks collision
    for op in enemies:
        idx = enemies.index(op)
        op.move()
        screen.blit(op.image, op.pos)
        if op.collide(bullet_rect):
            star_rect.x = bullet_rect.x
            star_fall(star_rect.x, star_rect.y)
            points += 10
            enemies.remove(op)

            # tracks levels
            enemy_tracker = len(enemies)
            if enemy_tracker == 0:
                level += 1
                if upper_level_idx < len(upper_level_aliens):
                    all_enemy_images.append(upper_level_aliens[upper_level_idx])
                    upper_level_idx += 1
                more_enemies += 5
                for num in range(more_enemies):
                    new_enemy_img = choice(all_enemy_images)
                    new_enemy = Enemy(new_enemy_img, randrange(0, 5) * randrange(50, 100), randrange(1, top_enemy_speed) * randrange(13, 25))
                    enemies.append(new_enemy)

        if op.collide(danger_zone):
            player_alive = False

    if player_alive:
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_LEFT]:
            player = player_left
            player_rect.x -= player_speed

        if key_press[pygame.K_RIGHT]:
            player = player_right
            player_rect.x += player_speed

        if key_press[pygame.K_SPACE]:
            if bullet_state == "ready":
                bullet_rect.x = player_rect.x
                fire_bullet(bullet_rect.x, bullet_rect.y)

        # Bullet Movement
        if bullet_rect.y <= 0:
            bullet_rect.y = screen_height - 70
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bullet_rect.x, bullet_rect.y)
            bullet_rect.y -= bullet_y_change

        # star_movement
        if star_rect.y <= 0:
            star_rect.y = screen_height - 70
            star_state = "ready"
        if star_state == "fire":
            star_fall(star_rect.x, star_rect.y)
            star_rect.y -= star_y_change

        screen.blit(player, player_rect)

    else:
        text_on_screen_center(f'GAME OVER', 'assets/fonts/poxel-font.ttf', 60, 'white', screen, screen_width / 2, screen_height / 2)
        dead_player_rect = player_rect
        screen.blit(player, (2000, 2000))
        screen.blit(dead_player, dead_player_rect)

    pygame.display.flip()

pygame.quit()

