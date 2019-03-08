import pygame, time,random
from pygame.locals import *
from uagame import Window

# User-defined functions



def main():
   window = Window('Memory', 500, 400)
   window.set_auto_update(False)
   game = Game(window)
   game.play()
   window.close()   


# User-defined classes


class Game:
   # An object in this class represents a complete game.


   def __init__(self,window):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the window's pygame.Surface object
      self.window = window
      self.pause_time = 0.04 # smaller is faster game
      self.close_clicked = False
      self.continue_game = True
      
      surface = self.window.get_surface()
      self.surface = surface
      surface_size = surface.get_size()
         

      Tile.set_surface(self.surface)
      self.board = []
      self.images = [] 
      self.create_images()
      self.create_board()
      self.score = 0 
      self.exposed_tile = 0
      
      self.score = 0
      self.other_tile = None


   def create_images(self):
     # self.images = []
      for index in range(1,9):
         images = 'image' + str(index) + '.bmp'
         image = pygame.image.load(images) 
         self.images.append(image) 
      self.images = self.images + self.images
      random.shuffle(self.images)
      
   


      
   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.




      while not self.close_clicked: # until player clicks close box
         # play frame
         self.handle_event()
         self.draw()
         if self.continue_game:
            self.update()
            self.decide_continue()
            
       #  time.sleep(self.pause_time) # set game velocity by pausing




   def handle_event(self):
      # Handle each user event by changing the game state
      # appropriately.
      # - self is the Game whose events will be handled
      event = pygame.event.poll()
      if event.type == QUIT:
         self.close_clicked = True
      if event.type == MOUSEBUTTONUP and self.continue_game:
         self.handle_mouse_up(event)
        
      
         
       
   def select_tile(self,event):
      for row in self.board:
         for tile in row:
            if tile.select(event.pos):
               return tile 
   
   def handle_mouse_up(self,pos):
   # no tile has been select and both have None type 
      tile = self.select_tile(pos) 
                  # one tile selected 
      if tile is not None and tile is not self.other_tile:
         tile.exposed()
         if self.other_tile is None: 
            self.other_tile = tile
                        
                     #two tiles selected and match 
         elif tile == self.other_tile:
            tile.exposed()
            self.other_tile.exposed()
            self.exposed_tile = self.exposed_tile + 2
            self.other_tile = None
            
            
         #two tiles select and do not match, both not None
         else:
            tile.exposed()
            self.other_tile.exposed()
            self.draw()
            time.sleep(1)
            tile.hide()
            self.other_tile.hide()
            self.other_tile = None 
            
               
   def create_board(self):
      width = self.surface.get_width()//5 
      height = self.surface.get_height()//4 
      
      size = (width - Tile.border_width,height - Tile.border_width)
      for row_index in range(0,4):
         row = []
         for col_index in range (0,4):
            x = width * col_index 
            y = height *row_index 
            location = (x + Tile.border_width//2,y + Tile.border_width//2)
            image_index = row_index * 4 + col_index 
            image = self.images[image_index]
            tile = Tile(image,location,size,self.surface)
            row.append(tile)
         self.board.append(row)
         
   def draw_score(self):
         self.window.set_font_size(80)
         score = str(self.score)
         width = self.surface.get_width()
         height = self.surface.get_height()
         score_width = self.window.get_string_width(score)
         x = width - score_width
         y = 0 
         self.window.draw_string(score,x,y)   
   
   
      
   def draw(self):
      # Draw the tiles and scoreboard.
      # - self is the Memory game

 
      self.window.clear()
      for row in self.board:
         for tile in row:
            tile.draw()
      self.draw_score()
      self.window.update()
            
   def update(self):
      # Update the game objects.
      # - self is the Game to update
      self.score = pygame.time.get_ticks()//1000
      
      
   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check


      if self.exposed_tile == 16:
         self.continue_game = False 
         




class Tile:
   #class attributes 
   border_color = pygame.Color('black') 
   border_width = 8
   surface = None 
   hidden_tile = pygame.image.load('image0.bmp')
   exposed_tile = 0 


   @classmethod
   def set_surface(cls,surface):
      cls.surface = surface 

   def __init__(self,image,location,size,surface):
      self.image = image 
      self.location = location 
      self.size = size
      self.rect = pygame.Rect(self.location,self.size)
      self.expose = False 
      
   def __eq__(self,other_image):
      if self.image is not None and self.image == other_image :
         return True
      else:
         return False    
 
  
   def draw(self):
      if self.expose == True:
         pygame.draw.rect(self.surface,Tile.border_color,self.rect,Tile.border_width)
         image = pygame.transform.scale(self.image,self.size)
         self.surface.blit(image,self.location)
         
      else:
         pygame.draw.rect(self.surface,Tile.border_color,self.rect,Tile.border_width)
         image = pygame.transform.scale(Tile.hidden_tile,self.size)
         self.surface.blit(image,self.location) 




   def select(self,position):
      if self.rect.collidepoint(position) and self.expose == False :
         self.expose = True
         return True 
      else:
         return False 

   
   def exposed(self):
         self.expose = True 
         
         
   def hide(self):
         self.expose = False         
      
      
main()


