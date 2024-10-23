#line 15
'''class Monster(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):

        monster = pygame.image.load("monster.PNG").convert_alpha()
        monster = pygame.transform.scale(monster, (80, 80))
        monster_rect = monster.get_rect(center=(250, 250))

        self.rect=pygame.Rect(x,y,width,height)
        self.x_vel=0
        self.y_vel=0
        self.mask= None
        self.direction = "left"
        self.animation_count =0
    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y +=dy
    def move_left(self,vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction="left"
            self.animation_count=0
    def move_right(self,vel):
        self.x_vel =vel
        if self.direction != "right":
            self.direction="right"
            self.animation_count=0
    def loop(self,fps):
        self.move(self.x_vel,self.y_vel)

    def draw(self,window):
        pygame.draw.rect(window, self.monster, self.monster_rect)'''
