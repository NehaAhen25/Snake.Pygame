import os
import pygame
from pygame.locals import *
import random
import time

# Constants
SIZE = 40
BACKGROUND_COLOR = (100, 255, 190)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        apple_img_path = os.path.join(os.path.dirname(__file__), "resources", "apple.jpg")
        self.apple = pygame.image.load(apple_img_path).convert()
        self.x = 120 
        self.y = 120 



    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        
        self.x =random.randint(0, 10 ) * SIZE
        self.y =random.randint(0, 8) * SIZE
        
            
class snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen= parent_screen
        block_img_path = os.path.join(os.path.dirname(__file__), "resources", "block.jpg")
        self.block = pygame.image.load(block_img_path).convert()
        snakeface_img_path = os.path.join(os.path.dirname(__file__), "resources", "snakeface.png")
        self.snakeface = pygame.image.load(snakeface_img_path).convert()
        self.x = [40]*length
        self.y = [40]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
         self.direction = 'right'


    def move_up(self):
         self.direction = 'up'


    def move_down(self):
         self.direction = 'down'


    def walk(self):
        for i in range(self.length-1,0,-1):
            # len,0,-1:::::     4,3,2,1,0,-1
            # len-0 first block move h, 0-1 reverse order me 2nd block
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        
        if self.direction == 'left':
            self.x[0] -= SIZE

        if self.direction == 'right':
            self.x[0] += SIZE

        if self.direction == 'up':  
            self.y[0] -= SIZE

        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            if i == 0:
                self.parent_screen.blit(self.snakeface, (self.x[i], self.y[i]))
            else:
                self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    


class Game:
    def __init__(self):
       pygame.init()
       pygame.mixer.init()

       self.play_background_music()
       self.surface = pygame.display.set_mode((1000, 500))

       
    #    self.surface.fill((100, 255, 190))
       self.snake = snake(self.surface, 1)
       self.snake.draw()
       self.apple = Apple(self.surface)
       self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    
    def play_background_music(self):
        music_path = os.path.join(os.path.dirname(__file__), "resources", "bg_music_1.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # Loop indefinitely
    
    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"resource/{sound}.mp3")

    def render_background(self):
        background_path = os.path.join(os.path.dirname(__file__), "resources", "background.jpg")
        background = pygame.image.load(background_path)
        self.surface.blit(background, (0, 0))

    def is_collision(self, x1, y1, x2, y2):
        return x1 >= x2 and x1 < x2 + SIZE and y1 >= y2 and y1 < y2 + SIZE

    def check_boundary_collision(self):
        head_x = self.snake.x[0]
        head_y = self.snake.y[0]
        return head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT


    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        # apple collision
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound_path = os.path.join(os.path.dirname(__file__), "resources", "ding.mp3")
            music=pygame.mixer.Sound(sound_path)
            # pygame.mixer.Sound.set_volume(music, 0.5)
            pygame.mixer.Sound.play(music)
            self.snake.increase_length()
            self.apple.move()


            # snake coilision
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]): 
                sound_path = os.path.join(os.path.dirname(__file__), "resources", "crush.wav")
                music=pygame.mixer.Sound(sound_path)
                # pygame.mixer.Sound.set_volume(music, 0.5)
                pygame.mixer.Sound.play(music)
                raise Exception("Game_Over")
        # boundary collision
        if self.check_boundary_collision():
            sound_path = os.path.join(os.path.dirname(__file__), "resources", "crush.wav")
            music=pygame.mixer.Sound(sound_path)
            # pygame.mixer.Sound.set_volume(music, 0.5)
            pygame.mixer.Sound.play(music)
            raise Exception("Game_Over")

            
    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.snake.length}', True, (90, 50, 250))
        self.surface.blit(score, (800, 10))

    def display_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is Over! Your score is {self.snake.length}", True, (90, 50, 250)) 
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Press Enter to play again or Escape to exit", True, (90, 50, 250))
        self.surface.blit(line2, (200, 350))

        pygame.display.flip()

        pygame.mixer.music.pause()    
    
        # Check for collision with apple
        # if self.snake.x[0] == self.apple.x and self.snake.y[0] == self.apple.y:
        #     self.snake.length += 1
        #     self.snake.x.append(-1)
    def reset(self):
        self.snake = snake(self.surface, 1)
        self.apple = Apple(self.surface)
        
        
            
    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
            # //startloop
                if event.type == KEYDOWN:
                # if loop
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:

                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                # if end elif start
                elif event.type == QUIT:
                    running = False
                # elif end
            # for loop end

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.display_game_over()
                pause = True
                self.reset()

            # self.play()
            time.sleep(0.5)
        # while loop     end





if __name__ == "__main__":
    game = Game()
    game.run()



    
    

#     # loading image in bg using image.load with robust path
#     # import os
#     # block_img_path = os.path.join(os.path.dirname(__file__), "resources", "block.jpg")
#     # block = pygame.image.load(block_img_path).convert()

#     # block_x = 100
#     # block_y = 100
#     # draw_block()

#    # time.sleep(10)
#     # running = True
#     # while running:
#     #     for event in pygame.event.get():
#     #         if event.type == KEYDOWN:
#     #             if event.key == K_ESCAPE:
#     #                 running = False
#     #             elif event.key == K_UP:
#     #                 block_y -= 10
#     #                 draw_block()
#     #             elif event.key == K_DOWN:
#     #                 block_y += 10
#     #                 draw_block()
#     #             elif event.key == K_LEFT:
#     #                 block_x -= 10
#     #                 draw_block()
#     #             elif event.key == K_RIGHT:
#     #                 block_x += 10
#     #                 draw_block()
#     #         elif event.type == QUIT:
#     #             running = False