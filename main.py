import pygame
import random
import os

FPS = 60
WIDTH = 500
HEIGHT = 600

# 顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 遊戲初始化 and 創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('第一個遊戲')
clock = pygame.time.Clock()

# 載入圖片
background_img = pygame.image.load(os.path.join('img', 'background.png')).convert()
player_img = pygame.image.load(os.path.join('img', 'player.png')).convert()
bullet_img = pygame.image.load(os.path.join('img', 'bullet.png')).convert()

rock_imgs = []

for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join('img', f'rock{i}.png')).convert())
    
# 載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join('sound', 'shoot.wav'))

expl_sounds = [
    pygame.mixer.Sound(os.path.join('sound', 'expl0.wav')),
    pygame.mixer.Sound(os.path.join('sound', 'expl1.wav'))
]

pygame.mixer.music.load(os.path.join('sound', 'background.ogg'))

# 調整背景音樂音量
pygame.mixer.music.set_volume(0.4)

# 載入字體
font_name = pygame.font.match_font('arial')

# 文字寫入畫面
def draw_text(surf, text, size, x, y):
    
    # 創建文字物件
    font = pygame.font.Font(font_name, size)
    
    # 渲染文字
    text_surface = font.render(text, True, WHITE)
    
    # 定位文字
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    
    # 畫出文字
    surf.blit(text_surface, text_rect)
    
# 生命條畫入畫面
def draw_health(surf, hp, x, y):
    if hp <= 0:
        hp = 0
    
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    
    # 剩餘生命
    fill = (hp / 100) * BAR_LENGTH
    
    # 生命條
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    
    # 生命條外框
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    
    # 畫出生命條
    pygame.draw.rect(surf, GREEN, fill_rect)
    
    # 畫出生命條外框
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# 創建石頭
def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

# 操控 sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        
        # 圖片背景透明化
        self.image.set_colorkey(BLACK)
        
        # 定位圖片
        self.rect = self.image.get_rect()
        
        # 以圖片中心點畫一個圓
        self.radius = 20
        
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        
        # 生命值
        self.health = 100

    def update(self):
        key_pressed = pygame.key.get_pressed()
        
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        
        # 判斷圖片是否超出畫面
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            
        if self.rect.left < 0:
            self.rect.left = 0
            
    def shoot(self):
        
        # 創建子彈
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()


# 石頭 sprite
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        
        # 圖片背景透明化
        self.image_ori.set_colorkey(BLACK)
        
        self.image = self.image_ori.copy()
        
        # 定位圖片
        self.rect = self.image.get_rect()
        
        # 以圖片中心點畫一個圓
        self.radius = int(self.rect.width * 0.85 / 2)
        
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 5)
        
        # 總轉動度數
        self.total_degree = 0
        
        self.rot_degree = random.randrange(-3, 3)
        
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree %= 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        
        # 轉動前圖片中心點
        center = self.rect.center
        
        # 重新定位轉動後圖片
        self.rect = self.image.get_rect()
        self.rect.center = center
    
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # 判斷圖片是否超出畫面
        if self.rect.y > HEIGHT \
            or self.rect.left > WIDTH \
            or self.rect.right < 0:
            
            # 重置圖片
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)


# 子彈 sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        
        # 圖片背景透明化
        self.image.set_colorkey(BLACK)
        
        # 定位圖片
        self.rect = self.image.get_rect()
        
        self.rect.centerx = x
        self.rect.y = y
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        
        # 判斷圖片是否超出畫面
        if self.rect.bottom < 0:
            
            # 刪除圖片
            self.kill()


all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for _ in range(8):
    
    # 創建石頭
    new_rock()
    
# 分數
score = 0

# 播放背景音樂(無限重複播放)
pygame.mixer.music.play(-1)

running = True

# 遊戲迴圈
while running:
    clock.tick(FPS)
    
    # 取得輸入
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        
        # 判斷是否按下鍵盤鍵
        elif event.type == pygame.KEYDOWN:
            
            # 按下空白鍵呼叫shoot
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # 更新遊戲
    all_sprites.update()
    
    # rocks & bullets 碰撞處理
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    
    # 判斷石頭 & 子彈是否碰撞
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        
        # 創建石頭
        new_rock()
    
    # player & rocks 碰撞處理
    # 加強碰撞判斷(矩形 -> 圓形)
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    
    # 判斷飛船 & 石頭是否碰撞
    for hit in hits:
        
        # 創建石頭
        new_rock()
        
        # 減少生命值
        player.health -= hit.radius
        
        if player.health <= 0:
            running = False
    
    # 畫面顯示
    screen.fill(BLACK)
    
    # 畫面背景
    screen.blit(background_img, (0, 0))
    
    all_sprites.draw(screen)
    
    # 顯示分數
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    
    # 顯示生命條
    draw_health(screen, player.health, 5, 15)
    
    pygame.display.update()
    
pygame.quit()