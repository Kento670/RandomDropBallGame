import pygame
import random

class Ball:
   
    def __init__(self, screen_width, screen_height, image_path="images/chicken_jockey.png", 
                 width=40, height=60, color=(255, 0, 0)):
     
        self.width = width
        self.height = height
        self.color = color  
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.image = None
        try:
            
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        except pygame.error as e:
            print(f"Could not load chicken jockey image: {e}")
            self.image = None
        
     
        self.reset()
        
        
        self.base_speed = 3
        
       
        self.rotation = 0
        self.rotate_speed = 2
        
    def update(self, game_state):
   
        speed = game_state.calculate_speed(self.base_speed)
        
       
        self.y += speed
        
     
        self.rotation = (self.rotation + self.rotate_speed) % 360
        
    def draw(self, screen):
       
        if self.image:
      
            rotated_image = pygame.transform.rotate(self.image, self.rotation)
            rot_rect = rotated_image.get_rect(center=self.get_rect().center)
            screen.blit(rotated_image, rot_rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, self.get_rect())
        
    def get_rect(self):
        
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def reset(self):
       
        self.x = random.randint(0, self.screen_width - self.width)
        self.y = 0
        
    def is_off_screen(self):
       
        return self.y > self.screen_height
    
    