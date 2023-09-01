# Import the pygame module
import pygame
import sys
import random

from pygame.sprite import AbstractGroup

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
    KEYDOWN,
    RLEACCEL,
    QUIT,
)

ScrX, ScrY = 1280, 720

screen = pygame.display.set_mode((ScrX, ScrY))

white = (255, 255, 255)
sky = (135, 206, 235)

font = pygame.font.Font('Assets\Fonts\Font.FON', 256)
centerX, centerY = 1280/2, 720/2
pygame.display.set_caption('GameRunner')

lightgreen = (144, 238, 144)

text = True

background_surface = pygame.surface.Surface((1280, 480))
background_surface.fill(sky)
floor_surface = pygame.surface.Surface((1280, 240))
floor_surface.fill(lightgreen)

def text(text, x, y):
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x, y))

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(ScrX + 20, ScrY + 100),
                random.randint(0, ScrX),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
        
class Player(pygame.sprite.Sprite):
    def __init__(self, centerX, centerY):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Assets/Graphics/play_btn.jpg").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
    
    def update(self, pressed_keys):
        if pressed_keys:
            background_surface.fill(sky)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ScrX:
            self.rect.right = ScrX
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= ScrY:
            self.rect.bottom = ScrY

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(ScrX + 50, ScrX + 100),
                480
            )
        )
        self.speed = 1


    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

FPS = 60

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1500)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player(centerX, centerY)
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
clouds = pygame.sprite.Group()


def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                #QUIT STATEMENTS
                if event.key == K_ESCAPE:
                    run = False


            #QUIT
            if event.type == pygame.QUIT:
                run = False
            
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            
        screen.blit(background_surface, (0, 0))

        drawTitle = True

        screen.blit(floor_surface, (0, 480))

        screen.blit(player.surf, player.rect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            run = False

        if drawTitle == True:
            text('GameRunner', centerX, centerY - 100)


        pressed_keys = pygame.key.get_pressed() 

        if pressed_keys == True:
            background_surface.fill(sky)

        player.update(pressed_keys)

        enemies.update()

        pygame.display.update()

    pygame.quit()
    sys.exit()

main()

if __name__ == '__main__':
    main()
