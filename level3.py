# level3.py
import pygame
import random
import sys

def run():
    # Constants
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    GRID_SIZE = 20
    MAZE_WIDTH, MAZE_HEIGHT = WINDOW_WIDTH // GRID_SIZE, WINDOW_HEIGHT // GRID_SIZE

    # Colors
    PATH_COLOR = (0, 0, 0)  # Black color for paths
    EXIT_COLOR = (0, 255, 0)  # Green color for exit

    # Initialize Pygame
    pygame.init()

    # Load images for textures and sprite
    log_texture = pygame.image.load("pixil-frame-0.png")  # Log texture for static background
    beaver_sprite = pygame.image.load("pixil-frame-1.png")  # Beaver sprite for the player

    # Set sprite size larger for better visibility
    sprite_width, sprite_height = 60, 60  # Larger than GRID_SIZE for clear visibility
    beaver_sprite = pygame.transform.scale(beaver_sprite, (sprite_width, sprite_height))

    # Scale log texture to fit the grid size
    log_texture = pygame.transform.scale(log_texture, (GRID_SIZE, GRID_SIZE))

    # Maze generation using recursive backtracking
    def generate_maze():
        # Initialize maze with walls (1s)
        maze = [[1 for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]

        # Recursive function to carve paths
        def carve_path(x, y):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)  # Randomize directions to create a unique maze each time
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                # Check if the next cell is within bounds and still a wall
                if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 1:
                    maze[y + dy][x + dx] = 0  # Carve a path between cells
                    maze[ny][nx] = 0
                    carve_path(nx, ny)  # Recur

        # Start carving from a random point in the maze
        start_x, start_y = random.randint(0, (MAZE_WIDTH - 1) // 2) * 2, random.randint(0, (MAZE_HEIGHT - 1) // 2) * 2
        maze[start_y][start_x] = 0
        carve_path(start_x, start_y)

        return maze

    # Function to draw the static log background
    def draw_background(screen):
        # Tile the log texture across the entire screen as the static background
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            for x in range(0, WINDOW_WIDTH, GRID_SIZE):
                screen.blit(log_texture, (x, y))

    # Function to draw the maze paths
    def draw_maze_paths(screen, maze):
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if maze[y][x] == 0:  # Draw paths over the log background
                    pygame.draw.rect(screen, PATH_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Function to draw the exit
    def draw_exit(screen, exit_pos):
        pygame.draw.rect(screen, EXIT_COLOR, (exit_pos[0] * GRID_SIZE, exit_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Display win message with final score
    def show_win_message(screen, score):
        font = pygame.font.Font(None, 72)
        text = font.render(f"Level score: {score}", True, EXIT_COLOR)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.fill((0, 0, 0))  # Clear screen
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Show the message for 2 seconds
        pygame.quit()
        return 'next', score  # Return 'next' and the final score

    def show_start_message(screen):
        font = pygame.font.Font(None, 48)
        text = font.render("Find the exit to the maze", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        
        # Get the start time
        start_time = pygame.time.get_ticks()

        # Display the message for 3 seconds
        while pygame.time.get_ticks() - start_time < 3000:
            screen.fill((0, 0, 0))  # Clear screen to black
            screen.blit(text, text_rect)
            pygame.display.flip()

            # Allow for exit events during the 3-second display
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        # Clear the screen after 3 seconds
        screen.fill((0, 0, 0))
        pygame.display.flip()

    # Main game function
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Beaver Maze Game - Level 3")
    clock = pygame.time.Clock()

    # Show start message
    show_start_message(screen)

    # Generate the maze
    maze = generate_maze()
    player_pos = [1, 1]  # Starting position for the player
    exit_pos = [MAZE_WIDTH - 2, MAZE_HEIGHT - 2]  # Exit position near the bottom-right corner

    # Initialize the score and timer
    score = 100
    start_time = pygame.time.get_ticks()  # Record the starting time
    movement_delay = 100  # Delay in milliseconds between moves
    last_move_time = pygame.time.get_ticks()  # Initialize last move time

    running = True
    while running:
        # Calculate the elapsed time in milliseconds
        elapsed_time = pygame.time.get_ticks() - start_time
        # Decrease score over time
        score = int(max(0, 1000 - elapsed_time * 0.1))  # Adjust the rate as needed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle player movement with collision detection and delay
        current_time = pygame.time.get_ticks()
        if current_time - last_move_time > movement_delay:
            keys = pygame.key.get_pressed()
            new_x, new_y = player_pos[0], player_pos[1]
            if keys[pygame.K_UP] and player_pos[1] > 0 and maze[player_pos[1] - 1][player_pos[0]] == 0:
                new_y -= 1
            elif keys[pygame.K_DOWN] and player_pos[1] < MAZE_HEIGHT - 1 and maze[player_pos[1] + 1][player_pos[0]] == 0:
                new_y += 1
            elif keys[pygame.K_LEFT] and player_pos[0] > 0 and maze[player_pos[1]][player_pos[0] - 1] == 0:
                new_x -= 1
            elif keys[pygame.K_RIGHT] and player_pos[0] < MAZE_WIDTH - 1 and maze[player_pos[1]][player_pos[0] + 1] == 0:
                new_x += 1

            # Update player position if the new position is valid
            if maze[new_y][new_x] == 0:
                player_pos = [new_x, new_y]
                last_move_time = current_time  # Update last move time

        # Check if player has reached the exit or score is zero
        if player_pos == exit_pos or score == 0:
            result, final_score = show_win_message(screen, score)
            return result, final_score  # Return status and final score

        # Draw the static log background
        draw_background(screen)

        # Draw the maze paths
        draw_maze_paths(screen, maze)

        # Draw the exit
        draw_exit(screen, exit_pos)

        # Draw the player (beaver sprite), centered in the grid cell
        screen.blit(beaver_sprite, 
                    (player_pos[0] * GRID_SIZE + (GRID_SIZE - sprite_width) // 2, 
                     player_pos[1] * GRID_SIZE + (GRID_SIZE - sprite_height) // 2))

        # Draw the score in the top-right corner
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Level score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WINDOW_WIDTH - 400, 10))

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Frame rate

    pygame.quit()
    return 'quit', score  # If the user quits, return status and score

if __name__ == "__main__":
    result, score = run()
    print("Level 3 result:", result)
    print("Level 3 score:", score)
