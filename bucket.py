import pygame

class Bucket:
    
    def __init__(self, screen_width, screen_height, image_path="images/lava_bucket.png", 
                 width=80, height=80, color=(0, 51, 204), outline_color=(0, 0, 255)):
       
        self.width = width
        self.height = height
        self.color = color 
        self.outline_color = outline_color
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        
        self.image = None
        try:
           
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        except pygame.error as e:
            print(f"Could not load lava bucket image: {e}")
            self.image = None
        
        
        self.x = screen_width // 2 - width // 2
        self.y = screen_height - 100  
        
    def update(self, posx, posy):
       
        self.x = posx
        self.y = posy
            
    def draw(self, screen):
        
        if self.image:
           
            screen.blit(self.image, (self.x, self.y))
        else:
           
            bucket_rect = self.get_rect()
            pygame.draw.rect(screen, self.color, bucket_rect)
            pygame.draw.rect(screen, self.outline_color, bucket_rect, 2)  # 2px outline
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def collides_with(self, obj_rect):
        return self.get_rect().colliderect(obj_rect)