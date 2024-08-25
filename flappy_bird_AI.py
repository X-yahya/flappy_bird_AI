import pygame 
import neat
import time 
import os 
import random 


WIN_WIDTH = 500  
WIN_HEIGHT = 800

bird_imgs = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", f"bird{i}.png"))) for i in range(1, 4)]
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "pipe.png")))
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "base.png")))
bg_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bg.png")))


#print (bird_imgs) 

class Bird : 

    IMGS = bird_imgs 
    MAX_ROTATION = 25
    ROT_VEL = 20 
    ANIMATION_TIME = 5

    def __init__(self,x,y):
        self.x=x 
        self.y=y
        self.tilt = 0 
        self.tick_count = 0 
        self.vel = 0 
        self.height = self.y
        self.img_count = 0 
        self.img = self.IMGS[0]

    def jump(self) : 
        self.vel = -10.5
        self.tick_count = 0  
        self.height = self.y

    def move(self) : 
        self.tick_count +=1
        d = self.vel*self.tick_count+1.5*self.tick_count**2  #how much moving up/down 
                    #   
        d = min(d, 16)
        if d < 0:
            d -= 2
        self.y += d
        if d < 0 or self.y < self.height + 50:
            self.tilt = min(self.tilt + self.ROT_VEL, self.MAX_ROTATION)
        else:
            self.tilt = max(self.tilt - self.ROT_VEL, -90)

    def draw(self , win) : 
        self.img_count += 1
        img_index = (self.img_count // self.ANIMATION_TIME) % len(self.IMGS)
        self.img = self.IMGS[img_index]
        if self.img_count >= self.ANIMATION_TIME * len(self.IMGS):
            self.img_count = 0

        if self.tilt <= -80 :
            self.img = self.IMGS[1] 
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img , self.tilt)
        new_rect  = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)
    def get_mask(self): 
        return pygame.mask.from_surface(self.img)
    
class Pipe : 
    GAP = 200 
    VEL = 5

    def __init__(self,x):
        self.x = x 
        self.height = 0
        #self.gap = 200
        self.top = 0 
        self.bottom = 0 
        self.PIPE_TOP = pygame.transform.flip(pipe_img , False , False)
        self.PIPE_BOTTOM = pipe_img
        self.passed = False
        self.set_height()
        
    def set_height(self):
        self.height= random.randrange(50,450)
        self.top=self.height-self.PIPE_TOP.get_height()
        self.botton = self.height+self.GAP
    def move(self):
        self.x -=self.VEL
    def draw(self,win):
        win.blit(self.PIPE_TOP , (self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))
    def collide(self,bird,win):
        bird_mask = bird.get_mask()
        
        top_mask =  pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
    
        top_offset = (self.x-bird.x,self.top-round(bird.y))
        bottom_offset = (self.x-bird.x,self.bottom-round(bird.y))
        b_point = bird_mask.overlap(bottom_mask,bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if t_point or b_point : 
            return True
        return False

class base :
    VEL = 5 
    WIDTH = base_img.get_width()
    IMG = base_img 

    def __init__(self,y):
        self.y = y 
        self.x1 = 0 
        self.x2 = self.WIDTH
        
    def move(self) : 
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0 : 
            self.x1 = self.x2 + self.WIDTH
        if self.x2+self.WIDTH <0 :
            self.x2 = self.x1 + self.WIDTH
    def draw(self , win): 
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))
def draw_window(win , bird): 
    win.blit(bg_img,(0,0))
    bird.draw(win)
    pygame.display.update()


def main() :
    bird = Bird(200,200)
    run =  True
    win = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                run = False 
        bird.move()
        draw_window(win , bird) 
    pygame.quit()
    quit()

main()