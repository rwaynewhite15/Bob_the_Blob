# blob.py

import pygame
import random

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # Color for yellow blobs
BLACK = (0, 0, 0)      # Color for text

def generate_initial_blobs(blobs, num_blobs, screen_width, screen_height):
    for _ in range(num_blobs):
        while True:
            blob_size = random.randint(10, 40)
            blob_x = random.randint(0, screen_width - blob_size)
            blob_y = random.randint(0, screen_height - blob_size)
            color = random.choice([RED, GREEN, YELLOW])
            velocity_x = random.uniform(-2, 2)
            velocity_y = random.uniform(-2, 2)
            
            if not any(
                ((blob_x - other_blob["x"]) ** 2 + (blob_y - other_blob["y"]) ** 2) ** 0.5 < (blob_size + other_blob["size"])
                for other_blob in blobs
            ):
                blobs.append({
                    "x": blob_x, "y": blob_y, "size": blob_size,
                    "color": color, "velocity_x": velocity_x, "velocity_y": velocity_y
                })
                break

def generate_additional_blobs(blobs, bob, num_blobs, screen_width, screen_height):
    for _ in range(num_blobs):
        placed = False
        for _ in range(100):  # Try up to 100 times to place a new blob
            blob_size = random.randint(1, bob.size + 50)
            blob_x = random.randint(0, screen_width - blob_size)
            blob_y = random.randint(0, screen_height - blob_size)
            color = random.choice([RED, GREEN, YELLOW])  # Include yellow blobs
            velocity_x = random.uniform(-2, 2)
            velocity_y = random.uniform(-2, 2)
            
            if can_fit_blob(blob_x, blob_y, blob_size, blobs, bob, screen_width, screen_height):
                blobs.append({
                    "x": blob_x, "y": blob_y, "size": blob_size,
                    "color": color, "velocity_x": velocity_x, "velocity_y": velocity_y
                })
                placed = True
                break
        
        if not placed:
            print("Could not place additional blobs. Skipping...")
            break

def can_fit_blob(blob_x, blob_y, blob_size, blobs, bob, screen_width, screen_height):
    if (blob_x < 0 or blob_x + blob_size > screen_width or
        blob_y < 0 or blob_y + blob_size > screen_height):
        return False
    
    distance_to_bob = ((bob.x - blob_x) ** 2 + (bob.y - blob_y) ** 2) ** 0.5
    if distance_to_bob < bob.size + blob_size:
        return False
    
    if any(
        ((blob_x - other_blob["x"]) ** 2 + (blob_y - other_blob["y"]) ** 2) ** 0.5 < (blob_size + other_blob["size"])
        for other_blob in blobs
    ):
        return False
    
    return True

def update_blobs(blobs, bob, score, screen_width, screen_height):
    new_score = score
    for blob in blobs[:]:
        # Update blob position
        blob["x"] += blob["velocity_x"]
        blob["y"] += blob["velocity_y"]

        # Bounce off walls
        if blob["x"] <= 0 or blob["x"] + blob["size"] >= screen_width:
            blob["velocity_x"] *= -1
        if blob["y"] <= 0 or blob["y"] + blob["size"] >= screen_height:
            blob["velocity_y"] *= -1
        
        # Check collision with Bob
        distance = ((bob.x - blob["x"]) ** 2 + (bob.y - blob["y"]) ** 2) ** 0.5
        if distance < bob.size + blob["size"]:
            if bob.size > blob["size"]:
                if blob["color"] == GREEN:
                    bob.size += blob["size"] // 2  # Bob grows with green blobs
                elif blob["color"] == RED:
                    bob.size = max(10, bob.size - blob["size"] // 2)  # Bob shrinks with red blobs
                elif blob["color"] == YELLOW:
                    # Randomly grow or shrink Bob with yellow blobs
                    if random.choice([True, False]):
                        bob.size += blob["size"] // 2
                    else:
                        bob.size = max(10, bob.size - blob["size"] // 2)
                blobs.remove(blob)  # Remove the blob
                new_score += 1  # Increase score
                generate_additional_blobs(blobs, bob, 2, screen_width, screen_height)  # Generate new blobs
            else:
                return new_score, True  # Game over
    if not blobs:
        return new_score, True  # Game over if no blobs are left
    return new_score, False  # Game continues

def draw_blobs(screen, blobs, bob):
    font = pygame.font.Font(None, 24)  # Font size for blob sizes
    for blob in blobs:
        pygame.draw.circle(screen, blob["color"], (int(blob["x"]), int(blob["y"])), blob["size"])
        
        # Render the size of the blob
        size_text = font.render(f"{blob['size']}", True, BLACK)
        text_rect = size_text.get_rect(center=(blob["x"], blob["y"]))
        screen.blit(size_text, text_rect)
