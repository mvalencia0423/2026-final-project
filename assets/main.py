import pygame
import random
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Dodge")

clock = pygame.time.Clock()

# Colors
BLACK = (10, 10, 10)
NEON_BLUE = (0, 255, 255)
NEON_RED = (255, 0, 100)
NEON_GREEN = (0, 255, 100)

# Player
player_size = 50
player = pygame.Rect(WIDTH//2, HEIGHT-70, player_size, player_size)
player_speed = 7
is_jumping = False
jump_velocity = 0
gravity = 0.6

# Platforms
platforms = [
    pygame.Rect(0, HEIGHT - 20, WIDTH, 20),  # Ground
    pygame.Rect(100, 450, 150, 15),
    pygame.Rect(400, 380, 150, 15),
    pygame.Rect(150, 300, 150, 15),
    pygame.Rect(500, 220, 150, 15),
]

# Enemy list
enemies = []
enemy_size = 40
enemy_speed = 5

# Score
score = 0
font = pygame.font.SysFont("Arial", 30)

def spawn_enemy():
    x = random.randint(0, WIDTH-enemy_size)
    y = -enemy_size
    enemies.append(pygame.Rect(x, y, enemy_size, enemy_size))

def draw_glow(rect, color):
    for i in range(10):
        glow_rect = rect.inflate(i*4, i*4)
        pygame.draw.rect(screen, color, glow_rect, 1)
    pygame.draw.rect(screen, color, rect)

def draw_banana_monster(rect, color):
    # Draw banana body (curved yellow shape)
    pygame.draw.ellipse(screen, (255, 255, 0), rect)
    
    # Draw eyes
    eye_offset = 8
    pygame.draw.circle(screen, BLACK, (rect.centerx - eye_offset, rect.centery - 3), 3)
    pygame.draw.circle(screen, BLACK, (rect.centerx + eye_offset, rect.centery - 3), 3)
    
    # Draw angry mouth
    pygame.draw.line(screen, BLACK, (rect.centerx - 6, rect.centery + 4), (rect.centerx + 6, rect.centery + 4), 2)
    
    # Draw glow effect
    for i in range(5):
        pygame.draw.circle(screen, color, (rect.centerx, rect.centery), rect.width//2 + i*2, 1)

def check_platform_collision(player, jump_vel):
    for platform in platforms:
        if (player.bottom >= platform.top and 
            player.bottom <= platform.bottom and
            player.centerx >= platform.left and 
            player.centerx <= platform.right and
            jump_vel >= 0):
            return True
    return False

spawn_timer = 0
running = True

while running:
    clock.tick(60)
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and check_platform_collision(player, jump_velocity):
                is_jumping = True
                jump_velocity = -15

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    # Jumping and gravity
    if is_jumping:
        jump_velocity += gravity
        player.y += jump_velocity

    # Check platform collision after movement
    if check_platform_collision(player, jump_velocity):
        is_jumping = False
        jump_velocity = 0

    # Spawn enemies
    spawn_timer += 1
    if spawn_timer > 30:
        spawn_enemy()
        spawn_timer = 0

    # Move enemies
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.top > HEIGHT:
            enemies.remove(enemy)
            score += 1

        if enemy.colliderect(player):
            print("Game Over! Final Score:", score)
            pygame.quit()
            sys.exit()

    # Draw platforms
    for platform in platforms:
        draw_glow(platform, NEON_GREEN)

    # Draw player
    draw_glow(player, NEON_BLUE)

    # Draw enemies
    for enemy in enemies:
        draw_banana_monster(enemy, NEON_RED)

    # Draw score
    score_text = font.render(f"Score: {score}", True, NEON_BLUE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()