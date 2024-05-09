import pygame 

from gui_settings import *



pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GUI TEST")
clock = pygame.time.Clock()


def main():

    #image_frames = [pygame.image.load(f'ai_frames/{i:02d}.png').convert_alpha() for i in range(90)]
    image_frames = [pygame.image.load(f'frames/{i:03d}.png').convert() for i in range(162)]
    frame_count = len(image_frames)
    frame_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        screen.fill((0, 0, 0))
        screen.blit(image_frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % frame_count

        pygame.display.update()
        clock.tick(30)

main()
        