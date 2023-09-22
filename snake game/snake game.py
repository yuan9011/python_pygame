import pygame
import sys
import random
from pygame.math import Vector2

# --------------------------------------------------
# 遊戲畫面長寬
# 遊戲畫面幀數
WIDTH = 400
HEIGHT = 500
FPS = 60

# --------------------------------------------------
class SNAKE:
  def __init__(self):
    
    # 圖片位置(向量)
    self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
    
    # 圖片移動方向
    self.direction = Vector2(0, 0)
    
    # 是否增加圖片(否)
    self.new_block = False
    
    # 載入圖片
    # 調整圖片大小
    self.head_up = pygame.image.load('graphics/head_up.png').convert_alpha()
    self.head_down = pygame.image.load('graphics/head_down.png').convert_alpha()
    self.head_right = pygame.image.load('graphics/head_right.png').convert_alpha()
    self.head_left = pygame.image.load('graphics/head_left.png').convert_alpha()
    
    self.tail_up = pygame.image.load('graphics/tail_up.png').convert_alpha()
    self.tail_down = pygame.image.load('graphics/tail_down.png').convert_alpha()
    self.tail_right = pygame.image.load('graphics/tail_right.png').convert_alpha()
    self.tail_left = pygame.image.load('graphics/tail_left.png').convert_alpha()
    
    self.body_vertical = pygame.image.load('graphics/body_vertical.png').convert_alpha()
    self.body_horizontal = pygame.image.load('graphics/body_horizontal.png').convert_alpha()
    
    self.body_tr = pygame.image.load('graphics/body_tr.png').convert_alpha()
    self.body_tl = pygame.image.load('graphics/body_tl.png').convert_alpha()
    self.body_br = pygame.image.load('graphics/body_br.png').convert_alpha()
    self.body_bl = pygame.image.load('graphics/body_bl.png').convert_alpha()
    
    self.head_up = pygame.transform.scale(self.head_up, (30, 30))
    self.head_down = pygame.transform.scale(self.head_down, (30, 30))
    self.head_right = pygame.transform.scale(self.head_right, (30, 30))
    self.head_left = pygame.transform.scale(self.head_left, (30, 30))
    
    self.tail_up = pygame.transform.scale(self.tail_up, (30, 30))
    self.tail_down = pygame.transform.scale(self.tail_down, (30, 30))
    self.tail_right = pygame.transform.scale(self.tail_right, (30, 30))
    self.tail_left = pygame.transform.scale(self.tail_left, (30, 30))
    
    self.body_vertical = pygame.transform.scale(self.body_vertical, (30, 30))
    self.body_horizontal = pygame.transform.scale(self.body_horizontal, (30, 30))
    
    self.body_tr = pygame.transform.scale(self.body_tr, (30, 30))
    self.body_tl = pygame.transform.scale(self.body_tl, (30, 30))
    self.body_br = pygame.transform.scale(self.body_br, (30, 30))
    self.body_bl = pygame.transform.scale(self.body_bl, (30, 30))
    
    # 載入音樂
    # 調整音樂音量
    self.crunch_sound = pygame.mixer.Sound('sound/crunch.wav')
    self.crunch_sound.set_volume(0.1)
    
  def draw_snake(self):
    self.update_head_graphics()
    self.update_tail_graphics()
    
    for index, block in enumerate(self.body):
      
      # 蛇位置
      x_pos = int(block.x * cell_size)
      y_pos = int(block.y * cell_size)
      
      # 蛇(矩形)
      block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
    
      # 畫出蛇頭
      if index == 0:
        screen.blit(self.head, block_rect)
      
      # 畫出蛇尾
      elif index == len(self.body) - 1:
        screen.blit(self.tail, block_rect)
      
      else:
        previous_block = self.body[index + 1] - block
        next_block = self.body[index - 1] - block
        
        if previous_block.x == next_block.x:
          screen.blit(self.body_vertical, block_rect)
          
        elif previous_block.y == next_block.y:
          screen.blit(self.body_horizontal, block_rect)
        
        else:
          
          if previous_block.x == -1 and next_block.y == -1 \
            or previous_block.y == -1 and next_block.x == -1:
              screen.blit(self.body_tl, block_rect)
              
          elif previous_block.x == 1 and next_block.y == -1 \
            or previous_block.y == -1 and next_block.x == 1:
              screen.blit(self.body_tr, block_rect)
              
          elif previous_block.x == -1 and next_block.y == 1 \
            or previous_block.y == 1 and next_block.x == -1:
              screen.blit(self.body_bl, block_rect)
              
          elif previous_block.x == 1 and next_block.y == 1 \
            or previous_block.y == 1 and next_block.x == 1:
              screen.blit(self.body_br, block_rect)
      
  def update_head_graphics(self):
    
    # 蛇移動方向
    head_relation = self.body[1] - self.body[0]
    
    # 判斷蛇移動方向
    if head_relation == Vector2(1, 0):
      self.head = self.head_left
      
    elif head_relation == Vector2(-1, 0):
      self.head = self.head_right
      
    elif head_relation == Vector2(0, 1):
      self.head = self.head_up
      
    elif head_relation == Vector2(0, -1):
      self.head = self.head_down
      
  def update_tail_graphics(self):
    
    # 蛇移動方向
    tail_relation = self.body[-2] - self.body[-1]
    
    # 判斷蛇移動方向
    if tail_relation == Vector2(1, 0):
      self.tail = self.tail_left
      
    elif tail_relation == Vector2(-1, 0):
      self.tail = self.tail_right
      
    elif tail_relation == Vector2(0, 1):
      self.tail = self.tail_up
      
    elif tail_relation == Vector2(0, -1):
      self.tail = self.tail_down
  
  def move_snake(self):
    
    if self.new_block:
      body_copy = self.body[:]
      body_copy.insert(0, body_copy[0] + self.direction)
      self.body = body_copy[:]
      self.new_block = False
      
    else:
      body_copy = self.body[: -1]
      body_copy.insert(0, body_copy[0] + self.direction)
      self.body = body_copy[:]
    
  def add_block(self):
    
    # 是否增加圖片(是)
    self.new_block = True

  def play_crunch_sound(self):
    self.crunch_sound.play()

  def reset(self):
    
    # 圖片位置(向量)
    self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
    
    # 圖片移動方向
    self.direction = Vector2(0, 0)


class FRUIT:
  def __init__(self):
    
    # 定位圖片
    self.randomize()
    
    # 載入圖片
    # 調整圖片大小
    self.image = pygame.image.load('graphics/apple.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (30, 30))
    
  def draw_fruit(self):
    
    # 水果位置
    x_pos = int(self.pos.x * cell_size)
    y_pos = int(self.pos.y * cell_size)
    
    # 水果(矩形)
    fruit_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
    
    # 畫出水果
    screen.blit(self.image, fruit_rect)
    
  def randomize(self):
    
    # 定位圖片
    self.x = random.randint(0, cell_number - 1)
    self.y = random.randint(0, cell_number - 1)
    
    # 圖片位置(向量)
    self.pos = Vector2(self.x, self.y)


class MAIN:
  def __init__(self):
    
    # 創建水果
    # 創建蛇
    self.fruit = FRUIT()
    self.snake = SNAKE()
    
  def update(self):
    
    # 蛇移動
    self.snake.move_snake()
    
    # 判斷碰撞(蛇與水果)
    # 判斷蛇是否超出畫面
    self.check_collision()
    self.check_fail()
    
  def draw_elements(self):
    
    # 畫出水果
    # 畫出蛇
    # 畫出草
    # 畫出分數
    self.draw_grass()
    self.fruit.draw_fruit()
    self.snake.draw_snake()
    self.draw_score()
    
  def check_collision(self):
    
    # 判斷碰撞(蛇與水果)
    if self.fruit.pos == self.snake.body[0]:
      
      # 播放音樂
      self.snake.play_crunch_sound()
      
      # 重新定位水果
      self.fruit.randomize()
      
      # 蛇身體增加
      self.snake.add_block()
      
      for block in self.snake.body[1:]:
        
        # 判斷水果位置是否蛇身體重疊
        if block == self.fruit.pos:
          self.fruit.randomize()
      
  def check_fail(self):
    
    # 判斷蛇是否超出畫面
    if not 0 <= self.snake.body[0].x < cell_number or \
      not 0 <= self.snake.body[0].y < cell_number:
        
      # 結束遊戲
      self.game_over()
        
    for block in self.snake.body[1:]:
      
      # 判斷蛇是否碰觸自己本身
      if block == self.snake.body[0]:
        
        # 結束遊戲
        self.game_over()
        
  def game_over(self):
    self.snake.reset()

  def draw_grass(self):
    grass_color = (167, 209, 61)
    
    for row in range(cell_number):
      if row % 2 == 0:
        for col in range(cell_number):
          if col % 2 == 0:
            grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface=screen, 
                             color=grass_color, 
                             rect=grass_rect)
      else:
        for col in range(cell_number):
          if col % 2 != 0:
            grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface=screen, 
                             color=grass_color, 
                             rect=grass_rect)

  def draw_score(self):
    score_text = str(len(self.snake.body) - 3)
    
    # 渲染文字(反鋸齒antialias : 邊緣柔化)
    score_surface = game_font.render(score_text, True, (54, 74, 12))
    
    # 定位文字
    score_x = int(cell_size * cell_number - 60)
    score_y = int(cell_size * cell_number - 30)
    score_rect = score_surface.get_rect(center=(score_x, score_y))
    apple_rect = self.fruit.image.get_rect(midright=(score_rect.left, score_rect.centery))
    bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)
    
    # 畫出分數
    pygame.draw.rect(surface=screen, 
                     color=(167, 209, 61), 
                     rect=bg_rect)
    
    pygame.draw.rect(screen, (54, 74, 12), bg_rect, 2)
    screen.blit(score_surface, score_rect)
    screen.blit(self.fruit.image, apple_rect)

# --------------------------------------------------
# 遊戲初始化
# 創建視窗
pygame.init()
pygame.mixer.init()
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

# 載入字體
game_font = pygame.font.Font('font/PoetsenOne-Regular.ttf', 25)

# 創建計時器
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(event=SCREEN_UPDATE, 
                      millis=150)

main_game = MAIN()

# --------------------------------------------------
# 遊戲迴圈
while True:
  
  # 一秒鐘迴圈執行次數
  clock.tick(FPS)
  
  # 取得輸入
  for event in pygame.event.get():
      
      # 判斷是否關閉遊戲
      if event.type == pygame.QUIT:
          
          # 關閉遊戲
          pygame.quit()
          sys.exit()
      
      # 判斷事件
      if event.type == SCREEN_UPDATE:
        
        # 更新內容
        main_game.update()
        
      # 判斷是否按下鍵盤鍵
      if event.type == pygame.KEYDOWN:
        
        # 蛇移動方向改變(上下左右)
        if event.key == pygame.K_UP:
          if main_game.snake.direction.y != 1:
            main_game.snake.direction = Vector2(0, -1)
        
        if event.key == pygame.K_RIGHT:
          if main_game.snake.direction.x != -1:
            main_game.snake.direction = Vector2(1, 0)
          
        if event.key == pygame.K_DOWN:
          if main_game.snake.direction.y != -1:
            main_game.snake.direction = Vector2(0, 1)
          
        if event.key == pygame.K_LEFT:
          if main_game.snake.direction.x != 1:
            main_game.snake.direction = Vector2(-1, 0)
            
  # 畫面顯示顏色
  screen.fill((175, 215, 70))
  
  # 畫出內容
  main_game.draw_elements()
  
  # 更新內容顯示到畫面上
  pygame.display.update()