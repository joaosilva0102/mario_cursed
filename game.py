import pygame
import os
pygame.font.init()
pygame.init()

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1280

GROUND_WIDTH = SCREEN_WIDTH / 2
GROUND_HEIGHT = 120

PLAYER = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "player", "mario1.png")), (120, 120)),
          pygame.transform.scale(pygame.image.load(os.path.join("imgs", "player", "mario2.png")), (120, 120)),
          pygame.transform.scale(pygame.image.load(os.path.join("imgs", "player", "mario3.png")), (120, 120))]

GROUND = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "ground", "ground.png")), (GROUND_WIDTH + 10, GROUND_HEIGHT))
BG = 0

class Player: 
    IMG = PLAYER
    FLIP_IMG = list(map(lambda x: pygame.transform.flip(x, True, False), IMG))
    SPRINT_VEL = 15
    WALK_VEL = 10
    MAX_HEALTH = 100
    
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.health = self.MAX_HEALTH
        self.jump_count = 11
        self.is_jump = False
        self.vel = self.WALK_VEL
        self.walk_count = 0
        self.left = False
        self.right = False
        self.img = self.IMG[0]
        
    def move_forward(self):
        self.xpos += self.vel
        self.right = True
        self.left = False
        self.moving = True
        
    def move_backward(self):
        self.xpos -= self.vel
        self.right = False
        self.left = True
        self.moving = True
  
    def sprint(self):
        self.vel = self.SPRINT_VEL
     
    def walk(self):
        self.vel = self.WALK_VEL
        
    def jump(self):
        if self.is_jump:
            self.img = self.IMG[2]
            if self.jump_count >= -11:
                if self.jump_count > 0:
                    self.ypos -= (self.jump_count ** 2) * 0.5
                else:
                    self.ypos += (abs(self.jump_count) ** 2) * 0.5
                self.jump_count -= 1
            else:
                self.jump_count = 11
                self.is_jump = False
    
    def draw(self, screen):
        rate = 6

        if self.vel == self.WALK_VEL:
            rate = 12

        if self.walk_count + 1 >= rate:
            self.walk_count = 0
            
        if self.left and not self.is_jump and self.moving:
            self.img = self.FLIP_IMG[self.walk_count // (rate // 3)]
            screen.blit(self.img, (self.xpos, self.ypos))
            self.walk_count += 1
            
        elif self.right and not self.is_jump and self.moving:
            self.img = self.IMG[self.walk_count // (rate // 3)]
            screen.blit(self.img, (self.xpos, self.ypos))
            self.walk_count += 1
            
        else:
            if self.right:
                if self.is_jump:
                    self.img = self.IMG[2]
                else:
                    self.img = self.IMG[0]
            else:
                if self.is_jump:
                    self.img = self.FLIP_IMG[2]
                else:
                    self.img = self.FLIP_IMG[0]

            screen.blit(self.img, (self.xpos, self.ypos))
            self.walk_count = 0
        
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
    
    def draw(self, screen):
        screen.blit(self.IMG, (self.xpos0, self.ypos))
        screen.blit(self.IMG, (self.xpos1, self.ypos))
        screen.blit(self.IMG, (self.xpos2, self.ypos))
        
    def move(self, player):
        self.xpos0 -= player.vel
        self.xpos1 -= player.vel
        self.xpos2 -= player.vel
        
        if self.xpos0 <= -self.IMG.get_width():
            self.xpos0 = SCREEN_WIDTH
        
        if self.xpos1 <= -self.IMG.get_width():
            self.xpos1 = SCREEN_WIDTH
        
        if self.xpos2 <= -self.IMG.get_width():
            self.xpos2 = SCREEN_WIDTH

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
    count = 0
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
            player.moving = True    
            if player.xpos <= SCREEN_WIDTH / 2 - 80:
                player.move_forward()
            if player.xpos >= SCREEN_WIDTH / 2 - 80:
                player.right = True
                ground.move(player)

        if key[pygame.K_a]:     
            if player.xpos > -40:
                player.move_backward()
                
        if key[pygame.K_LSHIFT]:
            player.sprint()    
        else:
            player.walk()
            
        if not key[pygame.K_d] and not key[pygame.K_a]:
            player.moving = False
            
                
        if key[pygame.K_SPACE] or key[pygame.K_w]:
            player.is_jump = True
            
                        
        player.jump()
        draw_window(screen, player, ground)
        
    
    pygame.quit()
main()