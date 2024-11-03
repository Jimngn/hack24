# main.py
import pygame
import sys
import level1  # Import level1 module
import level2  # Import level2 module
import level3  # Import level3 module
import level4  # Import level4 module
from flask import Flask
app = Flask(__name__)


def show_landing_page():
    # Initialize Pygame
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("November Astronomical Events")
    font_title = pygame.font.Font(None, 74)
    font_button = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()

    # Render texts
    title_text = font_title.render("November Astronomical Events", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))

    # Button properties
    button_text = font_button.render("Start", True, (0, 0, 0))
    button_rect = pygame.Rect(0, 0, 200, 80)
    button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    button_color = (255, 255, 255)

    # Display the landing page
    while True:
        screen.fill((0, 0, 0))  # Black background
        screen.blit(title_text, title_rect)

        # Draw button
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return  # Start the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    return  # Start the game

        clock.tick(30)

def show_congratulations_screen(total_score):
    pygame.init()  # Re-initialize Pygame
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Completed")
    font_large = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    # Render texts
    congrats_text = font_large.render("Congratulations!", True, (255, 255, 255))
    levels_complete_text = font_large.render("You've completed all levels!", True, (255, 255, 255))
    total_score_text = font_small.render(f"Total Score: {total_score}", True, (255, 255, 255))
    continue_text = font_small.render("Press ESC to exit", True, (255, 255, 255))

    # Text positions
    congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    levels_complete_rect = levels_complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    total_score_rect = total_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    # Display the screen
    while True:
        screen.fill((0, 0, 0))  # Black background
        screen.blit(congrats_text, congrats_rect)
        screen.blit(levels_complete_text, levels_complete_rect)
        screen.blit(total_score_text, total_score_rect)
        screen.blit(continue_text, continue_rect)
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        clock.tick(30)

def main():
    show_landing_page()  # Show the landing page first

    total_score = 0  # Initialize total score

    while True:
        # Start Level 1
        print("Starting Level 1...")
        level_status, score = level1.run()
        total_score += score  # Add Level 1 score to total score

        # Check if Level 1 was completed or needs restart
        if level_status == "next":
            print("Level 1 completed! Starting Level 2...")
            level_status, score = level2.run()  # Run Level 2 if Level 1 is completed
            total_score += score  # Add Level 2 score to total score

            # Check if Level 2 was completed successfully
            if level_status == "next":
                print("Level 2 completed! Starting Level 3...")
                level_status, score = level3.run()  # Run Level 3 if Level 2 is completed
                total_score += score  # Add Level 3 score to total score

                # Check if Level 3 was completed successfully
                if level_status == "next":
                    print("Level 3 completed! Starting Level 4...")
                    level_status, score = level4.run()  # Run Level 4 if Level 3 is completed
                    total_score += score  # Add Level 4 score to total score

                    # Check if Level 4 was completed successfully
                    if level_status == "next":
                        print("Congratulations! You've completed all levels!")
                        show_congratulations_screen(total_score)
                        break  # Exit loop if all levels are completed successfully
                else:
                    print("You lost in Level 3. Restarting from Level 1...")
            else:
                print("You lost in Level 2. Restarting from Level 1...")
        else:
            print("You lost in Level 1. Restarting from Level 1...")

if __name__ == "__main__":
    main()
