import pygame
import os
from os import listdir
from os.path import join, isfile
pygame.font.init()
pygame.init()

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1280

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GROUND_WIDTH = SCREEN_WIDTH / 2
GROUND_HEIGHT = 120

#PLAYER = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "player", "mario1.png")), (120, 120)),
#          pygame.transform.scale(pygame.image.load(os.path.join("imgs", "player", "mario2.png")), (120, 120)),
#          pygame.transform.scale(pygame.image.load(os.path.join("imgs", "player", "mario3.png")), (120, 120))]

GROUND = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "ground", "ground.png")), (GROUND_WIDTH + 10, GROUND_HEIGHT))
BG = 0

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction = False):
    path = join("imgs", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        
        
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
            
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
            
    return all_sprites
    
class Player(pygame.sprite.Sprite): 
    SPRITES = load_sprite_sheets("characters", "player", 64, 64, True)
    SPRINT_VEL = 15
    WALK_VEL = 10
    MAX_HEALTH = 100
    ANIMATION_DELAY = 5
    GRAVITY = 1
    
    def __init__(self, xpos, ypos, width, height):
        super().__init__()
        self.rect = pygame.Rect(xpos, ypos, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.fall_count = 0
        self.animation_count = 0
        self.health = self.MAX_HEALTH
        self.jump_count = 11
        self.walk_count = 0
        self.direction = "right"
        self.sprint_mult = 1
        
    def move_forward(self, vel):
        self.x_vel = vel * self.sprint_mult
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

        
    def move_backward(self,vel):
        self.x_vel = -vel * self.sprint_mult
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
    def loop(self):
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.update_sprite(30)
    
    def update_sprite(self, fps):
        if self.rect.y >= SCREEN_HEIGHT - 240:
            self.rect.y = SCREEN_HEIGHT - 240
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        sprite_sheet = "idle"
        if self.x_vel != 0:
            sprite_sheet = "walk"
    
        sprite_sheet_name = sprite_sheet + "_" + self.direction
            
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
    
    def sprint(self, vel):
        self.sprint_mult = vel
     
    def walk(self):
        self.sprint_mult = 1  

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0
    
    def draw(self):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))
        
# class Enemie:
    
def draw_background():    
    return 0

class Ground():
    IMG = GROUND
    
    def __init__(self):
        self.xpos0 = 0
        self.xpos1 = self.IMG.get_width() 
        self.xpos2 = 2*self.IMG.get_width() 
        self.ypos = SCREEN_HEIGHT - 120
        self.top = SCREEN_HEIGHT - 120
        
    def move(self, player):
        self.xpos0 -= player.x_vel
        self.xpos1 -= player.x_vel
        self.xpos2 -= player.x_vel
        
        if self.xpos0 <= -self.IMG.get_width():
            self.xpos0 = SCREEN_WIDTH
        
        if self.xpos1 <= -self.IMG.get_width():
            self.xpos1 = SCREEN_WIDTH
        
        if self.xpos2 <= -self.IMG.get_width():
            self.xpos2 = SCREEN_WIDTH
    
    def draw(self):
        screen.blit(self.IMG, (self.xpos0, self.ypos))
        screen.blit(self.IMG, (self.xpos1, self.ypos))
        screen.blit(self.IMG, (self.xpos2, self.ypos))

def draw_window(player, ground):
    screen.fill((255,255,255))
    player.draw()
    ground.draw()
    pygame.display.update()
    
    
    
def handle_moves(player, ground):
    key = pygame.key.get_pressed()
    if key[pygame.K_d]:
        if player.rect.x <= SCREEN_WIDTH / 2 - 80:
            player.move_forward(5)
        if player.rect.x >= SCREEN_WIDTH / 2 - 80:
            ground.move(player)

    if key[pygame.K_a]:     
        if player.rect.x > -40:
            player.move_backward(5)
            
    if key[pygame.K_LSHIFT]:
        player.sprint(2)    
    else:
        player.walk()
        
            
    if key[pygame.K_SPACE] or key[pygame.K_w]:
        player.jump()

                  
def main():
    clock = pygame.time.Clock()
    player = Player(100, SCREEN_HEIGHT - 240, 64, 64) 
    ground = Ground()
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
                
        player.loop()
        handle_moves(player, ground)
        draw_window(player, ground)
        
    
    pygame.quit()
main()