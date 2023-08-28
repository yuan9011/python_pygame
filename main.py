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

# 小飛船圖片 & 圖片背景透明化
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

rock_imgs = []

for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join('img', f'rock{i}.png')).convert())
    
expl_anim = {}

# 大爆炸
expl_anim['lg'] = []

# 小爆炸
expl_anim['sm'] = []

# 飛船爆炸
expl_anim['player'] = []

for i in range(9):
    expl_img = pygame.image.load(os.path.join('img', f'expl{i}.png')).convert()
    player_expl_img = pygame.image.load(os.path.join('img', f'player_expl{i}.png')).convert()
    
    # 圖片背景透明化
    expl_img.set_colorkey(BLACK)
    player_expl_img.set_colorkey(BLACK)
    
    # 調整圖片大小
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    
    expl_anim['player'].append(player_expl_img)
    
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join('img', 'shield.png')).convert()
power_imgs['gun'] = pygame.image.load(os.path.join('img', 'gun.png')).convert()
    
# 載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join('sound', 'shoot.wav'))
gun_sound = pygame.mixer.Sound(os.path.join('sound', 'pow1.wav'))
shield_sound = pygame.mixer.Sound(os.path.join('sound', 'pow0.wav'))
die_sound = pygame.mixer.Sound(os.path.join('sound', 'rumble.ogg'))

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

# 血條畫入畫面
def draw_lives(surf, lives, img, x, y):
    
    for i in range(lives):
        
        # 定位圖片
        img_rect = img.get_rect()
        img_rect.x = x + 32 * i
        img_rect.y = y
        
        # 畫出圖片
        surf.blit(img, img_rect)

# 創建石頭
def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

# 操控 sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        # 調整圖片大小
        self.image = pygame.transform.scale(player_img, (50, 38))
        
        # 圖片背景透明化
        self.image.set_colorkey(BLACK)
        
        # 定位圖片
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        
        # 以圖片中心點畫一個圓
        self.radius = 20
        
        # 圖片移動速度
        self.speedx = 8
        
        # 生命值(100)
        # 血條(3)
        self.health = 100
        self.lives = 3
        
        # 圖片隱藏
        # 圖片隱藏時間
        self.hidden = False
        self.hide_time = 0
        
        # 子彈等級
        # 子彈等級持續時間
        self.gun = 1
        self.gun_time = 0

    def update(self):
        
        # 現在時間
        now = pygame.time.get_ticks()
        
        # 判斷子彈等級 & 子彈等級持續時間是否大於 5000 毫秒
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now
        
        # 判斷圖片是否隱藏 & 隱藏時間是否大於 1000 毫秒
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            
            # 重新定位圖片
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            
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
        
        # 判斷圖片是否隱藏
        if not self.hidden:
            
            # 判斷子彈等級
            if self.gun == 1:
        
                # 創建子彈
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
                
            elif self.gun >= 2:
                
                # 創建子彈 * 2
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
                
        
    def hide(self):
        self.hidden = True
        
        # 圖片隱藏時間
        self.hide_time = pygame.time.get_ticks()
        
        # 圖片定位在畫面外
        self.rect.center = (WIDTH / 2, HEIGHT + 500)
        
    def gunup(self):
        
        # 子彈等級提升
        # 子彈等級提升時間
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()


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


# 爆炸 sprite
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        
        # 定位圖片
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        # 更新圖片張數
        self.frame = 0
        
        # 更新圖片時間(從初始化到現在經過時間(毫秒))
        self.last_update = pygame.time.get_ticks()
        
        # 更新圖片時間間隔(毫秒)
        self.frame_rate = 50
        
    def update(self):
        
        # 現在時間
        now = pygame.time.get_ticks()
        
        # 判斷(現在時間 - 最後一次圖片更新時間)是否大於更新圖片時間間隔
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            
            if self.frame == len(expl_anim[self.size]):
                
                # 刪除圖片
                self.kill()
                
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                
                # 定位圖片
                self.rect = self.image.get_rect()
                self.rect.center = center


# 寶物 sprite
class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        
        # 隨機選取掉寶種類
        self.type = random.choice(['shield', 'gun'])
        
        self.image = power_imgs[self.type]
        
        # 圖片背景透明化
        self.image.set_colorkey(BLACK)
        
        # 定位圖片
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        # 圖片掉落速度
        self.speedy = 3
        
    def update(self):
        self.rect.y += self.speedy
        
        # 判斷圖片是否超出畫面
        if self.rect.top > HEIGHT:
            
            # 刪除圖片
            self.kill()


# 群組 sprite
all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()

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
        
        # 大爆炸動畫
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        
        # 掉寶率為 10 %
        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        
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
        
        # 小爆炸動畫
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        
        if player.health <= 0:
            
            # 飛船爆炸動畫 & 音樂
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            
            player.lives -= 1
            
            # 刷新生命值
            player.health = 100
            
            player.hide()
    
    # 判斷血條是否歸零 & 飛船爆炸動畫是否存在
    if player.lives == 0 and not death_expl.alive():
        running = False
    
    # player & powers 碰撞處理
    hits = pygame.sprite.spritecollide(player, powers, True)
    
    # 判斷飛船 & 寶物是否碰撞
    for hit in hits:
        
        # 判斷寶物種類
        if hit.type == 'shield':
            player.health += 20
            
            # 判斷生命值是否大於 100
            if player.health > 100:
                player.health = 100
                
            gun_sound.play()
                
        elif hit.type == 'gun':
            player.gunup()
            shield_sound.play()
    
    # 畫面顯示
    screen.fill(BLACK)
    
    # 畫面背景
    screen.blit(background_img, (0, 0))
    
    all_sprites.draw(screen)
    
    # 顯示分數 & 生命條 & 血條
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    
    pygame.display.update()
    
pygame.quit()