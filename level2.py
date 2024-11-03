# level2.py
import pygame
import random
import math
import sys
import numpy as np

def run():
    # Screen settings
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    GAME_DURATION = 60  # Level duration in milliseconds (1 minute)
    CAPTURE_RADIUS = 55

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Explore the New Moon - Level 2")

    # Load images and fonts once for efficiency
    background_img = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
    telescope_img = pygame.transform.scale(pygame.image.load("telescope.png"), (80, 80))
    meteor_asteroid_img = pygame.transform.scale(pygame.image.load("meteor_asteroid.png"), (50, 50))
    meteor_asteroid_img = pygame.transform.rotate(meteor_asteroid_img, 45)
    meteor_comet_img = pygame.transform.scale(pygame.image.load("meteor_comet.png"), (50, 50))
    meteor_comet_img = pygame.transform.rotate(meteor_comet_img, -45)
    moon_img = pygame.transform.scale(pygame.image.load("moon.png"), (100, 100))
    explosion_img = pygame.transform.scale(pygame.image.load("explosion.png"), (50, 50))
    font = pygame.font.Font(None, 36)

    # Q-learning parameters
    q_table = np.zeros((20, 2))  # Q-table with 20 states and 2 actions
    alpha = 0.7  # learning rate
    gamma = 0.9  # discount factor
    epsilon = 0.9  # exploration rate
    meteor_speed_range = [1.5, 3]
    meteor_spawn_interval = 1200
    current_state = 0
    capture_streak = 0

    # Show a message on the screen for the intro
    def show_intro(messages):
        for message in messages:
            screen.fill((0, 0, 0))
            text = font.render(message, True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))
            pygame.display.flip()

            # Handle events and delay
            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start_time < 2000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    # Display result screen with final score
    def show_result_screen(score):
        screen.fill((0, 0, 0))
        text = font.render(f"Level score: {score}", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.flip()

        # Wait for 1 second while processing events
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False  # Exit the waiting loop on key press

    # Moon phase effect that adjusts meteor visibility
    def adjust_visibility(alpha_value):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(alpha_value)))
        screen.blit(overlay, (0, 0))

    # Q-learning update function
    def update_q_table(state, action, reward, next_state):
        best_future_q = np.max(q_table[next_state])
        q_table[state, action] += alpha * (reward + gamma * best_future_q - q_table[state, action])

    # Run the main game loop

    # Display intro messages
    show_intro([
        "November 4, 5 - Taurids Meteor Shower",
        "Collect the meteoroids with your telescope",
        "When the moon is bright, visibility will be reduced"
    ])

    telescope_x, telescope_y = WIDTH // 2, HEIGHT - 100
    meteors = []
    explosions = []
    meteor_timer = 0
    moon_brightness = 0  # Initial moon brightness
    moon_phase_direction = 1  # Direction for moon phase (1: brightening, -1: dimming)
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    score = 0
    capture_streak = 0

    class Meteor:
        def __init__(self):
            self.x = random.randint(100, WIDTH - 100)
            self.y = 0
            self.speed = random.uniform(*meteor_speed_range)
            self.type = random.choice(["asteroid", "comet"])
            self.image = meteor_asteroid_img if self.type == "asteroid" else meteor_comet_img

        def move(self):
            self.y += self.speed

        def draw(self):
            # Adjust brightness of meteors based on moon phase
            meteor_image = self.image.copy()
            meteor_image.set_alpha(255 - moon_brightness)
            screen.blit(meteor_image, (int(self.x), int(self.y)))

    class Explosion:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.start_time = pygame.time.get_ticks()

        def draw(self):
            screen.blit(explosion_img, (self.x, self.y))

    running = True
    while running:
        elapsed_time = pygame.time.get_ticks() - start_time
        time_left = max(0, GAME_DURATION - elapsed_time)

        # Check game end condition
        if time_left <= 0:
            show_result_screen(score)
            pygame.quit()
            return 'next', score  # Return level status and score

        # Gradual moon phase adjustment for visibility
        moon_brightness += moon_phase_direction * 0.1
        if moon_brightness >= 150:
            moon_phase_direction = -1  # Switch to dimming
            moon_brightness = 150
        elif moon_brightness <= 0:
            moon_phase_direction = 1  # Switch to brightening
            moon_brightness = 0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and telescope_x > 0:
            telescope_x -= 15
        if keys[pygame.K_RIGHT] and telescope_x < WIDTH - telescope_img.get_width():
            telescope_x += 15

        # Meteor spawning
        meteor_timer += clock.get_time()
        if meteor_timer >= meteor_spawn_interval:
            meteor_timer = 0
            if len(meteors) < 7:
                meteors.append(Meteor())

        # Meteor movement and capturing
        for meteor in meteors[:]:
            meteor.move()
            if meteor.y > HEIGHT:
                meteors.remove(meteor)
                explosions.append(Explosion(meteor.x, HEIGHT - 50))
                capture_streak = max(0, capture_streak - 1)  # Reset streak on miss

            distance = math.hypot(meteor.x - telescope_x, meteor.y - telescope_y)
            if distance < CAPTURE_RADIUS:
                score += 10  # Increase score by 10
                meteors.remove(meteor)
                capture_streak += 1

                # Adjust difficulty based on capture streak
                current_state = min(19, score // 50)  # State based on score every 50 points
                if np.random.rand() < epsilon:  # Exploration
                    action = random.choice([0, 1])
                else:  # Exploitation
                    action = np.argmax(q_table[current_state])

                # Adjust difficulty based on action
                if action == 0 and capture_streak > 3:  # Increase difficulty
                    meteor_speed_range[1] = min(10, meteor_speed_range[1] + 0.5)
                    meteor_spawn_interval = max(500, meteor_spawn_interval - 50)
                elif action == 1 and capture_streak < 1:  # Decrease difficulty
                    meteor_speed_range[1] = max(1.5, meteor_speed_range[1] - 0.5)
                    meteor_spawn_interval = min(2000, meteor_spawn_interval + 50)

                # Update Q-table
                reward = 1 if capture_streak > 3 else -1
                next_state = min(19, score // 50)
                update_q_table(current_state, action, reward, next_state)
                current_state = next_state

                # Decrease epsilon to reduce exploration over time
                epsilon = max(0.1, epsilon * 0.995)

        # Draw everything
        screen.blit(background_img, (0, 0))
        for meteor in meteors:
            meteor.draw()
        screen.blit(telescope_img, (telescope_x, telescope_y))

        # Draw moon with inverse brightness effect
        moon_surface = moon_img.copy()
        moon_surface.set_alpha(moon_brightness)
        screen.blit(moon_surface, (WIDTH - 110, 10))

        # Apply moonlight overlay for visibility challenge
        adjust_visibility(moon_brightness)

        # Display score and timer
        time_text = font.render(f"Time Left: {time_left // 1000}s", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))
        screen.blit(score_text, (WIDTH - 150, 10))

        # Draw explosions
        for explosion in explosions[:]:
            explosion.draw()
            if pygame.time.get_ticks() - explosion.start_time > 500:
                explosions.remove(explosion)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    return 'next', score  # Return level status and score

if __name__ == "__main__":
    result, score = run()
    print("Level 2 result:", result)
    print("Level 2 score:", score)
