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

def spawn_platform():
    # create platform above the visible area
    px = random.randint(0, WIDTH - 150)
    platforms.append(pygame.Rect(px, -20, 150, 15))

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

def draw_minion(rect):
    # Draw minion yellow body (large round shape)
    body_height = rect.height
    head_height = rect.height * 0.6
    
    # Head (top, rounder)
    head_rect = pygame.Rect(rect.left + 5, rect.top + 5, rect.width - 10, int(head_height))
    pygame.draw.ellipse(screen, (255, 255, 0), head_rect)
    
    # Torso (bottom, slightly wider)
    torso_rect = pygame.Rect(rect.left + 2, rect.top + int(head_height), rect.width - 4, rect.height - int(head_height))
    pygame.draw.rect(screen, (255, 255, 0), torso_rect)
    
    # Neon cyan overalls with tech look
    overall_height = rect.height - int(head_height) - 5
    overalls_rect = pygame.Rect(rect.left + 5, rect.top + int(head_height), rect.width - 10, overall_height)
    pygame.draw.rect(screen, (0, 150, 255), overalls_rect)  # Brighter cyan
    
    # Tech circuit lines on overalls
    pygame.draw.line(screen, (0, 255, 255), (rect.centerx - 8, rect.top + int(head_height) + 5), 
                     (rect.centerx - 8, rect.bottom - 2), 2)
    pygame.draw.line(screen, (0, 255, 255), (rect.centerx + 8, rect.top + int(head_height) + 5), 
                     (rect.centerx + 8, rect.bottom - 2), 2)
    pygame.draw.line(screen, (0, 255, 255), (rect.left + 8, rect.top + int(head_height) + 8), 
                     (rect.right - 8, rect.top + int(head_height) + 8), 1)
    
    # Tech pocket with glowing border
    pocket_rect = pygame.Rect(rect.centerx - 6, rect.top + int(head_height) + 12, 12, 10)
    pygame.draw.rect(screen, (0, 200, 255), pocket_rect)
    pygame.draw.rect(screen, (0, 255, 255), pocket_rect, 2)  # Glowing cyan border
    
    # Yellow arms with metal bands
    arm_y = rect.top + int(head_height) - 5
    # Left arm
    pygame.draw.line(screen, (255, 255, 0), (rect.left + 5, arm_y), (rect.left - 5, arm_y), 5)
    pygame.draw.circle(screen, (50, 50, 50), (rect.left - 8, arm_y), 4)  # Metal glove
    pygame.draw.circle(screen, (150, 150, 150), (rect.left - 8, arm_y), 2)  # Metal shine
    # Right arm
    pygame.draw.line(screen, (255, 255, 0), (rect.right - 5, arm_y), (rect.right + 5, arm_y), 5)
    pygame.draw.circle(screen, (50, 50, 50), (rect.right + 8, arm_y), 4)  # Metal glove
    pygame.draw.circle(screen, (150, 150, 150), (rect.right + 8, arm_y), 2)  # Metal shine
    
    # Metal feet
    pygame.draw.ellipse(screen, (100, 100, 100), pygame.Rect(rect.centerx - 12, rect.bottom - 4, 9, 4))
    pygame.draw.ellipse(screen, (100, 100, 100), pygame.Rect(rect.centerx + 3, rect.bottom - 4, 9, 4))
    
    # High-tech goggles with glowing cyan lenses
    goggle_y = rect.top + int(head_height) * 0.5
    goggle_size = 11
    
    # Left goggle
    pygame.draw.circle(screen, (50, 50, 50), (rect.centerx - 13, int(goggle_y)), goggle_size)  # Metal frame
    pygame.draw.circle(screen, (0, 200, 255), (rect.centerx - 13, int(goggle_y)), goggle_size - 2)  # Cyan lens
    pygame.draw.circle(screen, (0, 255, 255), (rect.centerx - 13, int(goggle_y)), goggle_size - 4)  # Glowing cyan
    pygame.draw.circle(screen, (0, 0, 0), (rect.centerx - 13, int(goggle_y)), 3)  # Pupil
    pygame.draw.circle(screen, (0, 255, 255), (rect.centerx - 15, int(goggle_y) - 2), 1)  # Tech shine
    
    # Right goggle
    pygame.draw.circle(screen, (50, 50, 50), (rect.centerx + 13, int(goggle_y)), goggle_size)
    pygame.draw.circle(screen, (0, 200, 255), (rect.centerx + 13, int(goggle_y)), goggle_size - 2)
    pygame.draw.circle(screen, (0, 255, 255), (rect.centerx + 13, int(goggle_y)), goggle_size - 4)
    pygame.draw.circle(screen, (0, 0, 0), (rect.centerx + 13, int(goggle_y)), 3)
    pygame.draw.circle(screen, (0, 255, 255), (rect.centerx + 15, int(goggle_y) - 2), 1)
    
    # Metal goggle connector bar with tech details
    pygame.draw.line(screen, (100, 100, 100), (rect.centerx - 3, int(goggle_y)), (rect.centerx + 3, int(goggle_y)), 3)
    pygame.draw.circle(screen, (0, 255, 255), (rect.centerx, int(goggle_y)), 2)  # Center tech node
    
    # Tech mouth (digital display style)
    mouth_y = int(goggle_y) + 13
    pygame.draw.line(screen, (0, 255, 255), (rect.centerx - 7, mouth_y), (rect.centerx + 7, mouth_y), 2)
    pygame.draw.line(screen, (0, 255, 255), (rect.centerx - 7, mouth_y + 2), (rect.centerx + 7, mouth_y + 2), 1)

def check_platform_collision(player, jump_vel):
    for platform in platforms:
        if (player.bottom >= platform.top and 
            player.bottom <= platform.top + 20 and
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

    # Gravity and jumping
    if not check_platform_collision(player, jump_velocity):
        # start falling if not already
        is_jumping = True
        jump_velocity += gravity
        player.y += jump_velocity
    else:
        # standing on a platform
        is_jumping = False
        jump_velocity = 0

    # Check if player fell off screen
    if player.top > HEIGHT:
        print(f"Game Over! Final Score: {score}")
        pygame.quit()
        sys.exit()

    # Spawn enemies
    spawn_timer += 1
    if spawn_timer > 30:
        spawn_enemy()
        spawn_timer = 0

    # vertical scroll: create more platforms as player ascends
    if player.y < HEIGHT // 4:
        shift = HEIGHT // 4 - player.y
        player.y += shift
        # move all platforms and enemies down
        for plat in platforms:
            plat.y += shift
        for enemy in enemies:
            enemy.y += shift
        # remove platforms that fell off bottom (except ground)
        platforms = [p for p in platforms if p.top < HEIGHT]
        if platforms and platforms[0].height != HEIGHT:  # ensure ground stays
            platforms.insert(0, pygame.Rect(0, HEIGHT - 20, WIDTH, 20))
        # spawn a new platform near the top
        px = random.randint(0, WIDTH - 150)
        platforms.append(pygame.Rect(px, -20, 150, 15))

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
    draw_minion(player)

    # Draw enemies
    for enemy in enemies:
        draw_banana_monster(enemy, NEON_RED)

    # Draw score
    score_text = font.render(f"Score: {score}", True, NEON_BLUE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()