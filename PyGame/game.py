import pygame
import random


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/raketa.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/meteor.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(2, 3)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Mars(pygame.sprite.Sprite):
    def __init__(self):
        super(Mars, self).__init__()
        self.surf = pygame.image.load("images/mars.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()


class Hvezda(pygame.sprite.Sprite):
    def __init__(self):
        super(Hvezda, self).__init__()
        self.surf = pygame.image.load("images/hvezda.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()


pygame.mixer.init()

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDMARS = pygame.USEREVENT + 2
pygame.time.set_timer(ADDMARS, 10000)
ADDHVEZDA = pygame.USEREVENT + 3
pygame.time.set_timer(ADDHVEZDA, 100)

player = Player()

enemies = pygame.sprite.Group()
marses = pygame.sprite.Group()
hvezdy = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

pygame.mixer.music.load("sound/Sky_dodge_theme.ogg")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.4)

move_up_sound = pygame.mixer.Sound("sound/Jet_up.ogg")
move_down_sound = pygame.mixer.Sound("sound/Jet_down.ogg")
collision_sound = pygame.mixer.Sound("sound/Boom.ogg")

move_up_sound.set_volume(0.6)
move_down_sound.set_volume(0.6)
collision_sound.set_volume(1.0)

running = True
start_time = None
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDMARS:
            new_mars = Mars()
            marses.add(new_mars)
            all_sprites.add(new_mars)

        elif event.type == ADDHVEZDA:
            new_hvezda = Hvezda()
            hvezdy.add(new_hvezda)
            all_sprites.add(new_hvezda)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    marses.update()
    hvezdy.update()

    screen.fill((0, 0, 0))
    if start_time:
        time_since_enter = pygame.time.get_ticks() - start_time
        message = 'Score: ' + str(time_since_enter)
        screen.blit(pygame.font.SysFont("Sans", 20).render(message, True, (255, 255, 255)), (20, 20))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()

        move_up_sound.stop()
        move_down_sound.stop()
        pygame.mixer.music.stop()
        pygame.time.delay(50)
        collision_sound.play()
        pygame.time.delay(500)

        running = False

    pygame.display.flip()

    clock.tick(60)

pygame.mixer.music.stop()
pygame.mixer.quit()