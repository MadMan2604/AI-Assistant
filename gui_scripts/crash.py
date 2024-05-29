import pygame
import sys

# Initialize pygame
pygame.init()

# Define the window size
WINDOW_WIDTH, WINDOW_HEIGHT = 400, 300

# Create the main window
main_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Main Window")

# Function to duplicate the main window
def duplicate_window():
    # Create a new window with the same size as the main window
    new_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Duplicate Window")

    # Copy the contents of the main window onto the new window
    new_window.blit(main_window, (0, 0))

    # Update the display
    pygame.display.flip()

# Track the number of windows (including the main window)
num_windows = 1

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Close the main window
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Duplicate the main window when SPACE key is pressed
                if num_windows < 10:  # Limit the number of windows to 10
                    duplicate_window()
                    num_windows += 1

# Quit pygame
pygame.quit()
