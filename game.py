import pygame
import os
pygame.font.init()
pygame.init()

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1280

GROUND_WIDTH = SCREEN_WIDTH / 2
GROUND_HEIGHT = 120

PLAYER = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "mario1.png")), (120, 120)),
          pygame.transform.scale(pygame.image.load(os.path.join("imgs", "mario2.png")), (120, 120)),
          pygame.transform.scale(pygame.image.load(os.path.join("imgs", "mario3.png")), (120, 120))]
GROUND = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "ground.png")), (GROUND_WIDTH, GROUND_HEIGHT))
BG = 0

class Player: 
    IMG = PLAYER
    FLIP_IMG = list(map(lambda x: pygame.transform.flip(x, True, False), IMG))
    MAX_VEL = 5
    MAX_JUMP = 5
    MAX_HEALTH = 100
    
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.height = ypos
        self.ground_level = ypos
        self.health = self.MAX_HEALTH
        self.img = self.IMG[0]
        self.jump_count = 10
        self.is_jump = False
        
    def move_forward(self):
        self.xpos += self.MAX_VEL
        self.img = self.IMG[0]
        
    def move_backward(self):
        self.xpos -= self.MAX_VEL
        self.img = self.FLIP_IMG[0]
     
    def set_height(self, height):
        self.height = height 
       
    def jump(self):
        if self.is_jump:
            if self.jump_count >= -10:
                self.ypos -= (self.jump_count * abs(self.jump_count)) * 0.4
                self.jump_count -= 1
            else: # This will execute if our jump is finished
                self.jump_count = 10
                self.is_jump = False
    
    def draw(self, screen):
        screen.blit(self.img, (self.xpos, self.ypos))

# class Enemie:
    
def draw_background():    
    return 0

class Ground():
    IMG = GROUND
    
    def __init__(self):
        self.xpos0 = 0
        self.xpos1 = self.IMG.get_width() 
        self.ypos = SCREEN_HEIGHT - 120
    
    def draw(self, screen):
        screen.blit(self.IMG, (self.xpos0, self.ypos))
        screen.blit(self.IMG, (self.xpos1, self.ypos))
    

def draw_window(screen, player, ground):
    screen.fill((255,255,255))
    player.draw(screen)
    ground.draw(screen)
    pygame.display.update()
    
    
    
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(100, SCREEN_HEIGHT - 240) 
    ground = Ground()
    
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            player.move_forward()
            
        if key[pygame.K_a]:
            player.move_backward()
            
        if key[pygame.K_SPACE]:
            player.is_jump = True
                    
        player.jump()
        draw_window(screen, player, ground)
        
    
    pygame.quit()
main()