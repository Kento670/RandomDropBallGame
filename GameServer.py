import threading
import pygame
import socket
import sys
import random
import os
from game_state import GameState
import pygame.mixer

# Initialize global variables
posx = 300
posy = 200
game_state = GameState()
client_connected = False

border_width = 2
border_color = (139, 69, 19)

movement_keys_pressed = {'w': False, 'a': False, 's': False, 'd': False}

global running_game


def play_sound(sound_file):
    
    if os.path.exists(sound_file):
        sound = pygame.mixer.Sound(sound_file)
        sound.play()

def draw_text(screen, text, size, x, y, color=(255, 255, 255)):
    
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def draw_borders(screen, screen_width, screen_height):
    
    pygame.draw.rect(screen, border_color, (0, 0, screen_width, border_width))
    pygame.draw.rect(screen, border_color, (0, screen_height - border_width, screen_width, border_width))
    pygame.draw.rect(screen, border_color, (0, 0, border_width, screen_height))
    pygame.draw.rect(screen, border_color, (screen_width - border_width, 0, border_width, screen_height))

def draw_stats_background(screen, x, y, width, height, color):
   
    s = pygame.Surface((width, height), pygame.SRCALPHA)
   
    s.fill(color)
    
    screen.blit(s, (x, y))

def draw_minecraft_text(screen, text, size, x, y, color=(255, 255, 255)):
   
    # Check if the Minecraft font is already loaded
    if not hasattr(draw_minecraft_text, 'minecraft_font'):
        try:
            
            font_path = os.path.join("fonts", "Minecraft.ttf")
            draw_minecraft_text.minecraft_font = {}
            pygame.font.init()
        except Exception as e:
            print(f"Could not initialize font system: {e}")
            draw_minecraft_text.minecraft_font = None
    
   
    if draw_minecraft_text.minecraft_font is not None:
        if size not in draw_minecraft_text.minecraft_font:
            try:
                font_path = os.path.join("fonts", "Minecraft.ttf")
                draw_minecraft_text.minecraft_font[size] = pygame.font.Font(font_path, size)
            except Exception as e:
                print(f"Could not load Minecraft font at size {size}: {e}")
               
                draw_minecraft_text.minecraft_font[size] = pygame.font.SysFont(None, size)
        
        
        font = draw_minecraft_text.minecraft_font[size]
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)
    else:
        
        draw_text(screen, text, size, x, y, color)

def play_background_music(music_file):
    
    try:
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(0.4)  # Set volume to 40%
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            print(f"Playing background music: {music_file}")
        else:
            print(f"Music file not found: {music_file}")
    except pygame.error as e:
        print(f"Could not play background music: {e}")


def GameThread():
    
    pygame.init()
    pygame.mixer.init()  # Initialize sound mixer
    
    screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Minecraft Chicken Jockey Catch")

    clock = pygame.time.Clock()
    
    play_background_music("music/Mall.mp3")

    # Get global variables
    global posx, posy, game_state, client_connected, running_game
    
    from ball import Ball
    from bucket import Bucket
    
    ball = Ball(screen_width, screen_height, "images/chicken_jockey.png", width=40, height=60)
    bucket = Bucket(screen_width, screen_height, "images/lava_bucket.png", width=80, height=80)
    
    # Load background image
    background = None
    try:
        background = pygame.image.load("images/minecraft_forest.png").convert()
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except pygame.error as e:
        print(f"Could not load background image: {e}")
    
    
    show_difficulty_message = False
    difficulty_message_timer = 0
    difficulty_message_duration = 180  # Show for 3 seconds
    
    # Set initial position
    posx = bucket.x
    posy = bucket.y
    
    # Add boundary checking to keep bucket within borders
    if bucket.x < border_width:
        bucket.x = border_width
        posx = border_width 
    elif bucket.x > screen_width - bucket.width - border_width:
        bucket.x = screen_width - bucket.width - border_width
        posx = screen_width - bucket.width - border_width 

    # Load sound effects
    catch_sound = "sounds/catch.wav"
    miss_sound = "sounds/miss.wav"    
    
    # Track previous state
    prev_state = game_state.get_state()
    
    # Main game loop
    running = True
    running_game = True
    while running and running_game:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        current_state = game_state.get_state()
        
        if current_state != prev_state:
            print(f"Game state changed: {prev_state} → {current_state}")
            
            # When entering PLAYING state, always reset
            if current_state == GameState.PLAYING:
                print("Resetting ball and bucket positions")
                ball.reset()
                bucket.x = screen_width // 2 - bucket.width // 2
                bucket.y = screen_height - 100
                posx = bucket.x
                posy = bucket.y
                
        
        # Menu state
        if current_state == GameState.MENU:
            
            try:
                if not hasattr(GameThread, 'menu_bg'):
                    GameThread.menu_bg = pygame.image.load("images/minecraft_kitten.png").convert()
                    GameThread.menu_bg = pygame.transform.scale(GameThread.menu_bg, (screen_width, screen_height))
                screen.blit(GameThread.menu_bg, (0, 0))
            except (pygame.error, AttributeError) as e:
                print(f"Menu background load error: {e}")
                screen.fill((14, 23, 48))
            
            
            draw_stats_background(screen, 0, 0, screen_width, screen_height, (0, 0, 0, 160))
            
            # Menu text
            draw_minecraft_text(screen, "CHICKEN JOCKEY CATCH", 36, screen_width // 2, screen_height // 4, (255, 215, 0))
            draw_minecraft_text(screen, "SPACE to start", 24, screen_width // 2, screen_height // 2, (255, 255, 255))
            draw_minecraft_text(screen, "ESC to quit", 24, screen_width // 2, screen_height // 2 + 50, (255, 255, 255))           
            
            status_text = "Client Connected" if client_connected else "Waiting for Client..."
            status_color = (0, 255, 0) if client_connected else (255, 165, 0)
            draw_minecraft_text(screen, status_text, 18, screen_width // 2, screen_height - 100, status_color)
            draw_minecraft_text(screen, "Have fun!", 16, screen_width // 2, screen_height - 50)
        
        # Playing state
        elif current_state == GameState.PLAYING:
            
            bucket.update(posx, posy)
            ball.update(game_state)

            
            if bucket.collides_with(ball.get_rect()):
                game_state.score += 1
                play_sound(catch_sound)
                
                # Increase difficulty
                if game_state.score % 5 == 0:
                    game_state.increase_difficulty()
                    show_difficulty_message = True
                    difficulty_message_timer = difficulty_message_duration
                
                # Reset ball after catch
                ball.reset()
            elif ball.is_off_screen():
                # Game over when ball is missed
                play_sound(miss_sound)
                game_state.set_state(GameState.GAME_OVER)
                ball.y = screen_height + 100  # Ensure ball is off-screen
            
            # Draw game 
            if background:
                screen.blit(background, (0, 0))
            else:
                screen.fill((115, 185, 255))

            draw_borders(screen, screen_width, screen_height)
            
            
            if show_difficulty_message:
                # Draw message background
                draw_stats_background(screen, screen_width // 2 - 200, 40, 400, 40, (0, 0, 0, 180))
                
                # Draw message text
                draw_minecraft_text(screen, "Difficulty increases every 5 balls!", 18, 
                                  screen_width // 2, 50, (255, 255, 0))
                
                # Decrement timer
                difficulty_message_timer -= 1
                if difficulty_message_timer <= 0:
                    show_difficulty_message = False
            
            # Draw game objects
            bucket.draw(screen)
            ball.draw(screen)
            
            # Draw UI elements
            draw_stats_background(screen, 10, 5, 130, 30, (0, 0, 0, 128))
            draw_minecraft_text(screen, f"Level: {game_state.difficulty_level}", 18, 70, 10, (255, 255, 255))
 
            draw_stats_background(screen, screen_width - 140, 5, 130, 30, (0, 0, 0, 128))
            draw_minecraft_text(screen, f"Score: {game_state.score}", 18, screen_width - 70, 10, (255, 255, 255))
        
        # Game over state
        elif current_state == GameState.GAME_OVER:
            # Game over screen
            screen.fill((89, 16, 16))
            draw_minecraft_text(screen, "GAME OVER", 48, screen_width // 2, screen_height // 4, (255, 255, 0))
            draw_minecraft_text(screen, f"SCORE: {game_state.score}", 32, screen_width // 2, screen_height // 2)
            draw_minecraft_text(screen, "Press SPACE to play again", 20, screen_width // 2, screen_height - 100)
            draw_minecraft_text(screen, "Press ESC to quit", 20, screen_width // 2, screen_height - 70)
        
        
        prev_state = current_state
        
        pygame.display.update()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

def ServerThread():
   
    global posx, posy, game_state, client_connected, movement_keys_pressed
    
    # Get server IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        host = s.getsockname()[0]
    except:
        host = "127.0.0.1"
    finally:
        s.close()
    
    print(f"Server IP: {host}")
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    print("Server enabled...")
    server_socket.listen(2)
    
    screen_width, screen_height = 600, 400
    bucket_width, bucket_height = 80, 80
    
    while True:
        try:
            conn, address = server_socket.accept()
            print("Connection from: " + str(address))
            client_connected = True
            
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                
                print(f"Command received: {data} | Current state: {game_state.get_state()}")

                 # Key states for movement
                if data.startswith('press_'):
                    key = data.split('_')[1]
                    if key in ['w', 'a', 's', 'd']:
                        movement_keys_pressed[key] = True
                elif data.startswith('release_'):
                    key = data.split('_')[1]
                    if key in ['w', 'a', 's', 'd']:
                        movement_keys_pressed[key] = False
                
                # PLAYING state movement on key states
                if game_state.get_state() == GameState.PLAYING:
                    move_speed = 10 * (1 + (game_state.difficulty_level * 0.1))
                    
                    if movement_keys_pressed['a']:
                        posx -= move_speed
                    if movement_keys_pressed['d']:
                        posx += move_speed
                    if movement_keys_pressed['w']:
                        posy -= move_speed
                    if movement_keys_pressed['s']:
                        posy += move_speed
                
                # Border constraints
                if posx < border_width:
                    posx = border_width
                if posx > screen_width - bucket_width - border_width:
                    posx = screen_width - bucket_width - border_width
                if posy < border_width:
                    posy = border_width
                if posy > screen_height - bucket_height - border_width:
                    posy = screen_height - bucket_height - border_width

                # Handle game control commands, space to start and esc to quit
                if data == 'space':
                    print(f"SPACE command received in state {game_state.get_state()}")
                    
                    if game_state.get_state() == GameState.MENU or game_state.get_state() == GameState.GAME_OVER:
                        game_state.set_state(GameState.PLAYING)
                        game_state.reset_game()
                        
                        posx = (screen_width - bucket_width) // 2
                        posy = screen_height - 100
                        print(f"Game started/restarted via client command")

                elif data == 'esc':
                    if game_state.get_state() == GameState.PLAYING:
                        game_state.set_state(GameState.MENU)
                        print("Returned to menu via client command")
                    elif game_state.get_state() == GameState.MENU or game_state.get_state() == GameState.GAME_OVER:
                        global running_game
                        running_game = False
            
            client_connected = False
            conn.close()
        except Exception as e:
            print(f"Server error: {e}")
            client_connected = False

if __name__ == "__main__":
    if not os.path.exists("sounds"):
        os.makedirs("sounds")
        print("Created sounds directory. Please add sound files.")
    
    # Start game threads
    t1 = threading.Thread(target=GameThread, args=[])
    t2 = threading.Thread(target=ServerThread, args=[])
    t1.start()
    t2.start()