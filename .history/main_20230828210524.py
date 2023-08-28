# Import the pygame module
import pygame
import sys

# Initialize pygame
pygame.init()

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    MOUSEBUTTONDOWN,
    KEYDOWN,
    QUIT,
)

screen = pygame.display.set_mode((1280, 720))

white = (255, 255, 255)
sky = (135, 206, 235)
font = pygame.font.Font('Assets\Fonts\Font.FON', 128)
centerX, centerY = 1280/2, 720/2
pygame.display.set_caption('Game')

text = True

background_surface = pygame.surface.Surface((1280, 480))

def image(path, x, y):
    img = pygame.image.load(path).convert_alpha()
    screen.blit(img, (x, y))

def text(text, x, y):
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x, y))

FPS = 60

def draw_on_window():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                #QUIT STATEMENTS
                if event.key == K_ESCAPE:
                    run = False
            if event.type == MOUSEBUTTONDOWN:
                if centerX <= mouse[0] <= centerX-35 and centerY <= mouse[1] <= centerY: 
                    background_surface.fill(0, 0)
                    pygame.display.update()  

            #QUIT
            if event.type == pygame.QUIT:
                run = False
            else:
                background_surface.fill(sky)
                screen.blit(background_surface, (0, 0))
                image('Assets\Graphics\\floor.jpg', -10, 360)
                mouse = pygame.mouse.get_pos()
                text('UnderTale', centerX - 50, centerY - 100)
                image('Assets\Graphics\play_btn.jpg', centerX - 35, centerY)
                image('Assets\Graphics\help.jpg', 1190, 600)
                pygame.display.update()
    pygame.quit()
    sys.exit()

def main():
    draw_on_window()

if __name__ == '__main__':
    main()
