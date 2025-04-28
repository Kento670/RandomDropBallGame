# game_state.py
class GameState:
   
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    
    def __init__(self):
        self.current_state = self.MENU
        self.score = 0
        self.difficulty_level = 1
        
    def reset_game(self):
        
        self.score = 0
        self.difficulty_level = 1
        
    def increase_difficulty(self):
       
        self.difficulty_level += 1
        
    def calculate_speed(self, base_speed):
        
        return base_speed + (self.difficulty_level * 0.5)
    
    def set_state(self, state):
        
        self.current_state = state
        
    def get_state(self):
        
        return self.current_state