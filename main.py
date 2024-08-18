import pygame
import blob
import bob
import highscore

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load the background music and popping sound effect
pygame.mixer.music.load("sound/theme.mp3")
pop_sound = pygame.mixer.Sound("sound/pop.mp3")

# Set the volume
pygame.mixer.music.set_volume(0.5)  # Background music volume
pop_sound.set_volume(0.7)  # Popping sound effect volume

# Play the background music on loop
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Screen dimensions
screen_width = 1500
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bob the Blob")

# Load high score
high_score_filename = "high_score.txt"
high_score, longest_time = highscore.load_high_score(high_score_filename)

 # format time
def format_time(time_in_seconds):
    minutes = int(time_in_seconds // 60)
    seconds = int(time_in_seconds % 60)
    formatted_time = f"{minutes}:{seconds:02d}"
    return formatted_time

def game_loop():
    # Create game objects
    blobs_list = []
    blob.generate_initial_blobs(blobs_list, 10, screen_width, screen_height)
    player_bob = bob.Bob(screen_width // 2, screen_height // 2, 20, 10)
    score = 0
    game_over = False
    last_blob_time = start_time = pygame.time.get_ticks() 
     # Hide the cursor
    pygame.mouse.set_visible(False)

    # Main game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                player_bob.use_mouse = False  # Disable mouse control if any key is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                player_bob.use_mouse = True # Enable mouse control if mouse is clicked


        keys = pygame.key.get_pressed()
        if player_bob.use_mouse:
            player_bob.move_with_mouse()
        else:
            player_bob.move(keys, screen_width, screen_height)

        # Update blobs and check for game over
        score, game_over = blob.update_blobs(blobs_list, player_bob, score, screen_width, screen_height)

        # Add new blob every 2 seconds if all blobs are larger than Bob
        current_time = pygame.time.get_ticks()
        if current_time - last_blob_time > 2000:
            if all(blob["size"] >= player_bob.size for blob in blobs_list):
                blob.generate_additional_blobs(blobs_list, player_bob, 1, screen_width, screen_height)
                last_blob_time = current_time

        # Calculate elapsed game time
        elapsed_time = (current_time - start_time) / 1000  # Convert to seconds

        # Draw everything
        screen.fill((0, 0, 0))  # Clear the screen
        blob.draw_blobs(screen, blobs_list, player_bob)
        player_bob.draw(screen)
        # Draw Bob's size
        font = pygame.font.Font(None, 24)
        bob_size_text = font.render(f"{player_bob.size}", True, (0, 0, 0))
        bob_size_rect = bob_size_text.get_rect(center=(player_bob.x, player_bob.y))
        screen.blit(bob_size_text, bob_size_rect)

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

        # Display game timer in the top-left corner, below Bob's size
        timer_text = font.render(f"Time: {format_time(elapsed_time)}", True, (255, 255, 255))
        screen.blit(timer_text, (10, 90))

        # Display Bob's size in the bottom corner
        bob_size_text = font.render(f"Size: {player_bob.size}", True, (255, 255, 255))
        screen.blit(bob_size_text, (10, 750))

        pygame.display.flip()

        delay = max(1, 30 - score // 5)
        pygame.time.delay(delay)
        print(f'delay:{delay}')  # Frame rate

    # Game over screen
    display_game_over(score, elapsed_time)

def display_game_over(score, elapsed_time):
    global high_score
    global longest_time
    new_record = False
    if score > high_score:
        high_score = score
        new_record = True
    if elapsed_time > longest_time:
        longest_time = elapsed_time
        new_record = True
    if new_record:
        highscore.save_high_score(high_score_filename, high_score, longest_time)

    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    time_over_text = font.render(f"Time: {format_time(elapsed_time)}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    longest_time_text = font.render(f"Longest Time: {format_time(longest_time)}", True, (255, 255, 255))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2 - 350))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - score_text.get_height() // 2 - 200))
    screen.blit(time_over_text, (screen_width // 2 - time_over_text.get_width() // 2, screen_height // 2 - time_over_text.get_height() // 2 - 125))
    screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height // 2 + 50))
    screen.blit(longest_time_text, (screen_width // 2 - longest_time_text.get_width() // 2, screen_height // 2 - longest_time_text.get_height() // 2 + 150))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 300))
    
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r or event.key == pygame.K_RETURN:
                    game_loop()  # Restart the game
                    waiting_for_input = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    game_loop()  # Restart the game
                    waiting_for_input = False

if __name__ == "__main__":
    game_loop()
