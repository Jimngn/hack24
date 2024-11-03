# level4.py
import pygame
import random
import sys
import math

def run():
    # Constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PLAYER_SIZE = 50
    BULLET_SIZE = 30
    INITIAL_BULLET_SPEED = 1  # Start with a slower initial speed for ease
    INITIAL_SPAWN_INTERVAL = 60  # Slower spawn interval to make it easier initially
    BULLET_LIFETIME = 5000  # Bullet lifetime in milliseconds (5 seconds)
    
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Level 4: Dodge the Alien Bullets")
    clock = pygame.time.Clock()
    
    # Load images
    player_image = pygame.transform.scale(pygame.image.load('alien.png'), (PLAYER_SIZE, PLAYER_SIZE))
    bullet_image = pygame.transform.scale(pygame.image.load('bullet.png'), (BULLET_SIZE, BULLET_SIZE))
    background_image = pygame.transform.scale(pygame.image.load('galaxy.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Reset initial state
    player_rect = player_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE - 10))
    player_speed = 10
    bullets = []
    bullet_spawn_timer = 0
    bullet_speed = INITIAL_BULLET_SPEED
    spawn_interval = INITIAL_SPAWN_INTERVAL
    score = 0
    
    # Function to show result screen
    def show_result_screen(message, final_score):
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        
        # Display the final score
        score_text = pygame.font.Font(None, 36).render(f"Final Score: {final_score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(score_text, score_rect)
        
        # Display "Press SPACE to continue"
        continue_text = pygame.font.Font(None, 36).render("Press SPACE to continue", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(continue_text, continue_rect)
    
        pygame.display.flip()
        
        # Wait for SPACE to continue
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False  # Exit the waiting loop
    
    # Main game loop
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # Draw the background image
    
        # Update score over time
        score += 0.5  # Increase score by 0.5 per frame for survival
    
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < SCREEN_HEIGHT:
            player_rect.y += player_speed
    
        # Rapid increase in difficulty based on score
        bullet_speed = INITIAL_BULLET_SPEED + (score // 400)  # Faster increase in bullet speed
        spawn_interval = max(10, INITIAL_SPAWN_INTERVAL - int(score // 300))  # Faster decrease in spawn interval
    
        # Bullet spawning aimed at the player's position
        if bullet_spawn_timer <= 0:
            spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
            if spawn_side == 'top':
                bullet_x = random.randint(0, SCREEN_WIDTH - BULLET_SIZE)
                bullet_y = 0
            elif spawn_side == 'bottom':
                bullet_x = random.randint(0, SCREEN_WIDTH - BULLET_SIZE)
                bullet_y = SCREEN_HEIGHT - BULLET_SIZE
            elif spawn_side == 'left':
                bullet_x = 0
                bullet_y = random.randint(0, SCREEN_HEIGHT - BULLET_SIZE)
            elif spawn_side == 'right':
                bullet_x = SCREEN_WIDTH - BULLET_SIZE
                bullet_y = random.randint(0, SCREEN_HEIGHT - BULLET_SIZE)
    
            bullet_rect = pygame.Rect(bullet_x, bullet_y, BULLET_SIZE, BULLET_SIZE)
            bullets.append((bullet_rect, pygame.time.get_ticks()))  # Store bullet with its spawn time
            bullet_spawn_timer = spawn_interval  # Reset bullet spawn timer
        else:
            bullet_spawn_timer -= 1
        
        # Bullet movement and collision detection
        for bullet, spawn_time in bullets[:]:
            bullet_center = bullet.center
            player_center = player_rect.center
            direction_x = player_center[0] - bullet_center[0]
            direction_y = player_center[1] - bullet_center[1]
            distance = math.hypot(direction_x, direction_y)
    
            if distance != 0:
                direction_x /= distance
                direction_y /= distance
            
            bullet.x += direction_x * bullet_speed
            bullet.y += direction_y * bullet_speed
            
            # Check for collisions  
            if bullet.colliderect(player_rect):
                final_score = int(score)  # Convert score to integer
                show_result_screen("You crashed!", final_score)
                pygame.quit()
                return 'next', final_score  # Return 'next' and the final score
    
            # Remove bullets that go off-screen or have existed for more than BULLET_LIFETIME
            if bullet.y > SCREEN_HEIGHT or bullet.y < 0 or bullet.x < 0 or bullet.x > SCREEN_WIDTH or \
                    pygame.time.get_ticks() - spawn_time > BULLET_LIFETIME:
                bullets.remove((bullet, spawn_time))
        
        # Draw player and bullets
        screen.blit(player_image, player_rect)
        for bullet, _ in bullets:
            screen.blit(bullet_image, bullet.topleft)
        
        # Display the score
        score_text = pygame.font.Font(None, 36).render(f"Level score: {int(score)}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)  # Set FPS for consistent gameplay

    pygame.quit()
    return 'next', int(score)  # Return 'next' and the final score

if __name__ == "__main__":
    result, score = run()
    print("Level 4 result:", result)
    print("Level 4 score:", score)
