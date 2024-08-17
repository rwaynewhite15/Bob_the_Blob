import pygame
import blob
import bob
import highscore

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1550
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bob the Blob")

# Load high score
high_score_filename = "high_score.txt"
high_score = highscore.load_high_score(high_score_filename)

def game_loop():
    # Create game objects
    blobs_list = []
    blob.generate_initial_blobs(blobs_list, 10, screen_width, screen_height)
    player_bob = bob.Bob(screen_width // 2, screen_height // 2, 20, 5)
    score = 0
    game_over = False
    
    # Main game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        keys = pygame.key.get_pressed()
        player_bob.move(keys, screen_width, screen_height)

        # Update blobs and check for game over
        score, game_over = blob.update_blobs(blobs_list, player_bob, score, screen_width, screen_height)

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
        screen.blit(score_text, (10, 10))

        # Display Bob's size in the top corner
        bob_size_text = font.render(f"Size: {player_bob.size}", True, (255, 255, 255))
        screen.blit(bob_size_text, (10, 850))

        pygame.display.flip()
        pygame.time.delay(30)  # Frame rate

    # Game over screen
    display_game_over(score)

def display_game_over(score):
    global high_score
    if score > high_score:
        high_score = score
        highscore.save_high_score(high_score_filename, high_score)

    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2 - 100))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - score_text.get_height() // 2))
    screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height // 2 + 50))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 150))
    
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()  # Restart the game
                    waiting_for_input = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

if __name__ == "__main__":
    game_loop()
