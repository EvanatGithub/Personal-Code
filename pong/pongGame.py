# Pong Version 3
#You should use the event attributes of the event type listed in the event module to test whether an event is a KEYDOWN event. 
#event.type == KEYDOWN
#In order to check two keys simultaneously, you will need the following function in pygame.key module
#list_of_keys = pygame.key.get_pressed()
#keys. For example, if we wish to check if a key has been pressed then we would write the following statement: 
#To allow your game to respond to a key that is HELD down, insert this statement somewhere in the __init__ method of the Game class: pygame.key.set_repeat(20, 20)
#When moving a paddle, you will need to know the y coordinates of the top and bottom of the paddle's Rect so that you don't move it out of the window. Every Rect has a set of attributes listed in the documentation for the Rect type. For example, if you had a variable called paddle that was bound to one of the paddle's Rect, you could compute the y coordinate of the top of the rectangle, using the attribute reference expression: paddle.top
import pygame,time
from uagame import Window
from pygame.locals import *

# Main Algorithm
def main():
    # create the window
    title = 'Pong'
    width = 500
    height = 400
    window = Window(title,width,height)
    window.set_auto_update(False)
    # create the Game object
    game = Game(window)
    # play the game
    game.play()
    # close the window
    window.close()
# USER DEFINED CLASS
class Game:
    def __init__(self, window):
        self.window = window
        self.close_clicked = False
        self.continue_game = True
        self.pause_time = 0.01 
             
        color = pygame.Color('white')
        center_dot = [250,250]
        radius = 6
        velocity_dot = [6,1]
        surface = window.get_surface()
        self.dot = Dot(surface,color,center_dot,radius,velocity_dot)
        pygame.key.set_repeat(20, 20)
        #paddle properties
        self.x1 = 50
        self.y = 150
        self.x2 = 450
        self.location1=[self.x1, self.y]
        self.location2=[self.x2, self.y]
        self.width = 5
        self.height = 100
        size=(5, self.height) 
        self.rect1=pygame.Rect(self.location1,size)
        self.rect2=pygame.Rect(self.location2,size)        
        #score
        self.score_1 = 0
        self.score_2 = 0
        
    
    def play(self):
        while not self.close_clicked:
            self.draw()
            self.handle_event()
            if self.continue_game:
                self.update()
                self.decide_continue()
            time.sleep(self.pause_time) 
            
    def handle_event(self):
         # Loop forever
       
      # Handle events
        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        if event.type == KEYDOWN and self.continue_game:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w] and self.rect1.top > 0 : self.rect1.move_ip(0, -5)
            if pressed[pygame.K_s] and self.rect1.bottom + self.height < 400: self.rect1.move_ip(0,  5)
            if pressed[pygame.K_UP] and self.rect2.top > 0: self.rect2.move_ip(0, -5)
            if pressed[pygame.K_DOWN] and self.rect2.bottom + self.height< 400: self.rect2.move_ip(0, 5)  
            self.update()
            
        
    def draw(self):
        self.window.clear()
        pygame.draw.rect(self.window.get_surface(),pygame.Color('white'),self.rect1)
        pygame.draw.rect(self.window.get_surface(),pygame.Color('white'),self.rect2)
        self.dot.draw()
        self.draw_score()
        self.window.update()  
    def draw_score(self):
        score_string_1 = str(self.score_1)
        score_string_2 = str(self.score_2)
        font_size = 70
        self.window.set_font_size(font_size)
        self.window.set_font_color('white')
        x = 0
        y = 0
        self.window.draw_string(score_string_1,x,y) 
        y = 0
        x = 440
        self.window.draw_string(score_string_2,x,y) 
        if self.dot.center[0] <= self.dot.radius:
            self.score_1 = self.score_1 + 1
        if self.dot.center[0] + self.dot.radius >= 498:
            self.score_2 = self.score_2 + 1        
            
    def update(self):
        self.dot.move()
        #bounce code left paddle
        r1=pygame.draw.rect(self.window.get_surface(),pygame.Color('white'),self.rect1)
        r2=pygame.draw.rect(self.window.get_surface(),pygame.Color('white'),self.rect2)
        
        if r1.collidepoint(self.dot.center) and self.dot.velocity[0]<0:
            self.dot.bounce()
        #bounce code right paddle
        if r2.collidepoint(self.dot.center) and self.dot.velocity[0]>0:
            self.dot.bounce()                
    def decide_continue(self):
        if self.score_1 == 11:
            self.continue_game = False
        if self.score_2 == 11:
            self.continue_game = False        
        
    
class Dot:
    def __init__(self,surface,color,center,radius,velocity):  
        self.surface = surface
        self.color = color
        self.center = center
        self.radius = radius
        self.velocity = velocity
    def draw(self):
        pygame.draw.circle(self.surface,self.color,self.center,self.radius)
    def move(self):
        size = self.surface.get_size()
        #keep ball within window
        for coord in range(0,2):
            self.center[coord] = (self.center[coord]+self.velocity[coord])%size[coord]
            if self.center[coord] < self.radius :
                self.velocity[coord] = -self.velocity[coord]
            if self.center[coord] + self.radius > size[coord]:
                self.velocity[coord] = -self.velocity[coord]   
        
    def bounce(self):
        self.velocity[0] = - self.velocity[0]
        
                

        
        
main()


