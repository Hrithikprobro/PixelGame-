import pygame
import sys
import random
import time

pygame.init()

# Constants
ScrX, ScrY = 1280, 720
FPS = 60
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
LIGHT_GREEN = (144, 238, 144)
FONT_PATH = 'Assets/Fonts/Font.FON'

# Initialize the screen
screen = pygame.display.set_mode((ScrX, ScrY))
pygame.display.set_caption('GameRunner')

# Fonts
menu_font = pygame.font.Font(FONT_PATH, 72)
small_font = pygame.font.Font(FONT_PATH, 36)

def get_font(size): 
    return pygame.font.Font("Assets/Fonts/Font.FON", size)


# Surfaces
background_surface = pygame.surface.Surface((ScrX, 480))
background_surface.fill(SKY_BLUE)
floor_surface = pygame.surface.Surface((ScrX, 240))
floor_surface.fill(LIGHT_GREEN)

# Abstract Button class
class Button:
    def __init__(self, image, pos, text, font, base_color, hovering_color):
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.button_text = text  # Store the text separately from self.text to avoid conflicts
        self.text = font.render(self.button_text, True, base_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.base_color = base_color
        self.hovering_color = hovering_color

    def change_color(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.text = small_font.render(self.button_text, True, self.hovering_color)
        else:
            self.text = small_font.render(self.button_text, True, self.base_color)

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)



# Function to display text
def display_text(text, x, y):
    text_surface = small_font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))

# Class for Cloud
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(ScrX + 20, ScrY + 100),
                random.randint(0, ScrX),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Class for Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Assets/Graphics/player.jpg").convert()
        self.rect = pygame.Rect(5, 5, 150, 198)

    def update(self, pressed_keys):
        if pressed_keys:
            background_surface.fill(SKY_BLUE)
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ScrX:
            self.rect.right = ScrX
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= ScrY:
            self.rect.bottom = ScrY

# Class for Enemy
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

# Function to display the main menu
def main_menu():
    global PLAY_BUTTON, QUIT_BUTTON
    while True:
        screen.fill(SKY_BLUE)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(
            image=pygame.image.load("Assets/Graphics/Play Rect.png"),
            pos=(640, 250),
            text="PLAY",  # Use the text attribute, not text_input
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        QUIT_BUTTON = Button(
            image=pygame.image.load("Assets/Graphics/Quit Rect.png"),
            pos=(640, 400),
            text="QUIT",  # Use the text attribute, not text_input
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.change_color(MENU_MOUSE_POS)
            button.update(screen)

        # Check for mouse button clicks
        if pygame.mouse.get_pressed()[0]:  # 0 represents the left mouse button
            if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                play()
            if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


        pygame.display.update()
        

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1500)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
clouds = pygame.sprite.Group()

# Function to play the game
# Function to play the game
def play():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            if event.type == pygame.QUIT:
                run = False

        screen.blit(background_surface, (0, 0))

        text_start_time = None
        text_duration = 5  # Adjust this to set the duration in seconds

        if text_start_time is None:
            text_start_time = time.time()

        current_time = time.time()
        if current_time - text_start_time <= text_duration:
            display_text("Your Text Here", 100, 100)
            text_start_time = None

        screen.blit(floor_surface, (0, 480))

        screen.blit(player.surf, player.rect)

        # Update the button in the game loop
        PLAY_BUTTON.change_color(pygame.mouse.get_pos())
        QUIT_BUTTON.change_color(pygame.mouse.get_pos())

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Add this part to render enemies
        for enemy in enemies:
            screen.blit(enemy.surf, enemy.rect)

        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            run = False

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys:
            background_surface.fill(SKY_BLUE)
            screen.blit(floor_surface, (0, 480))
            screen.blit(player.surf, player.rect)

        player.update(pressed_keys)

        enemies.update()

        # Update the buttons in the game loop
        PLAY_BUTTON.update(screen)
        QUIT_BUTTON.update(screen)

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_menu()
