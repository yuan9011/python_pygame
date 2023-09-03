import pygame
import random
import os

# --------------------------------------------------
# 遊戲畫面長寬
# 遊戲畫面幀數
WIDTH = 500
HEIGHT = 600
FPS = 60

# --------------------------------------------------
# 顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# --------------------------------------------------
# 遊戲初始化
# 創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('太空生存戰')
clock = pygame.time.Clock()

# --------------------------------------------------
# 載入圖片
# 圖片背景透明化
# 調整圖片大小
background_img = pygame.image.load(os.path.join('img', 'background.png')).convert()
player_img = pygame.image.load(os.path.join('img', 'player.png')).convert()
bullet_img = pygame.image.load(os.path.join('img', 'bullet.png')).convert()

player_img.set_colorkey(BLACK)
bullet_img.set_colorkey(BLACK)

player_mini_img = pygame.transform.scale(player_img, (25, 19))

# 設定遊戲標題圖片
pygame.display.set_icon(player_mini_img)

rock_imgs = []

for i in range(7):
    rock_img = pygame.image.load(os.path.join('img', f'rock{i}.png')).convert()
    rock_img.set_colorkey(BLACK)
    rock_imgs.append(rock_img)
    
expl_anim = {}

# 大爆炸
# 小爆炸
# 飛船爆炸
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []

for i in range(9):
    expl_img = pygame.image.load(os.path.join('img', f'expl{i}.png')).convert()
    player_expl_img = pygame.image.load(os.path.join('img', f'player_expl{i}.png')).convert()
    
    expl_img.set_colorkey(BLACK)
    player_expl_img.set_colorkey(BLACK)
    
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    expl_anim['player'].append(player_expl_img)
    
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join('img', 'shield.png')).convert()
power_imgs['gun'] = pygame.image.load(os.path.join('img', 'gun.png')).convert()

# --------------------------------------------------
# 載入音樂
# 調整音樂音量
shoot_sound = pygame.mixer.Sound(os.path.join('sound', 'shoot.wav'))
gun_sound = pygame.mixer.Sound(os.path.join('sound', 'pow1.wav'))
shield_sound = pygame.mixer.Sound(os.path.join('sound', 'pow0.wav'))
die_sound = pygame.mixer.Sound(os.path.join('sound', 'rumble.ogg'))

shoot_sound.set_volume(0.1)
gun_sound.set_volume(0.1)
shield_sound.set_volume(0.1)
die_sound.set_volume(0.1)

expl_sounds = [
    pygame.mixer.Sound(os.path.join('sound', 'expl0.wav')),
    pygame.mixer.Sound(os.path.join('sound', 'expl1.wav'))
]

# 背景音樂
pygame.mixer.music.load(os.path.join('sound', 'background.ogg'))
pygame.mixer.music.set_volume(0.1)

# --------------------------------------------------
# 載入字體
font_name = os.path.join('font.ttf')

# --------------------------------------------------
# 文字寫入畫面
def draw_text(surf, text, size, x, y):
    
    # 創建文字物件
    font = pygame.font.Font(font_name, size)
    
    # 渲染文字(反鋸齒antialias : 邊緣柔化)
    text_surface = font.render(text, True, WHITE)
    
    # 定位文字
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    
    # 畫出文字
    surf.blit(text_surface, text_rect)
    
# 生命條畫入畫面
def draw_health(surf, hp, x, y):
    
    # 判斷生命是否小於 0
    if hp < 0:
        hp = 0
    
    # 生命條長寬
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    
    # 剩餘生命
    fill = (hp / 100) * BAR_LENGTH
    
    # 生命條(矩形)
    # 生命條外框(矩形)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    
    # 畫出生命條
    # 畫出生命條外框(外框粗細為 2)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# 血條畫入畫面(小飛機圖片)
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

# 初始畫面
def draw_init():
    
    # 畫面背景
    screen.blit(background_img, (0, 0))
    
    # 畫面文字
    draw_text(screen, '太空生存戰', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, '← → 移動飛船 空白鍵發射子彈', 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, '按任意鍵開始遊戲', 18, WIDTH / 2, HEIGHT * 3 / 4)
    
    # 更新內容顯示到畫面上
    pygame.display.update()
    
    waiting = True
    
    while waiting:
        
        # 一秒鐘迴圈執行次數
        clock.tick(FPS)
    
        # 取得輸入
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            
            # 判斷是否按下鍵盤鍵(按下並鬆開)
            elif event.type == pygame.KEYUP:
                waiting = False
                return False
        
# --------------------------------------------------
# 操控 sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        # 調整圖片大小
        self.image = pygame.transform.scale(player_img, (50, 38))
        
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
        
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        
        if key_pressed[pygame.K_RIGHT]:
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
                # 播放子彈音樂
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
                
            elif self.gun >= 2:
                
                # 創建子彈 * 2
                # 播放子彈音樂
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                
                shoot_sound.play()
                 
    def hide(self):
        self.hidden = True
        
        # 紀錄圖片隱藏開始時間
        self.hide_time = pygame.time.get_ticks()
        
        # 圖片定位在畫面外
        self.rect.center = (WIDTH / 2, HEIGHT + 500)
        
    def gunup(self):
        
        # 子彈等級提升
        # 紀錄子彈等級提升開始時間
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()


# 石頭 sprite
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image = self.image_ori.copy()
        
        # 定位圖片
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        
        # 以圖片中心點畫一個圓
        self.radius = int(self.rect.width * 0.85 / 2)
        
        # 圖片移動速度
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 5)
        
        # 總轉動度數
        # 轉動度數
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
        
    def rotate(self):
        
        # 轉動度數
        # 轉動圖片
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
            
            # 重置圖片(位置 & 移動速度)
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)


# 子彈 sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        
        # 定位圖片
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        
        # 圖片移動速度
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
        # 紀錄更新圖片開始時間
        # 更新圖片時間間隔(毫秒)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        
        # 現在時間
        now = pygame.time.get_ticks()
        
        # 判斷(現在時間 - 最後一次圖片更新時間)是否大於更新圖片時間間隔
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            
            # 判斷圖片更新張數是否為最後一張
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
        self.type = random.choice(list(power_imgs.keys()))
        
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


# --------------------------------------------------
# 播放背景音樂(無限重複播放)
pygame.mixer.music.play(-1)

# --------------------------------------------------
# 遊戲迴圈
show_init = True
running = True

while running:
    
    # 顯示初始畫面
    if show_init:
        colse = draw_init()
        
        # 判斷是否關閉初始畫面
        if colse:
            break
        
        show_init = False
        
        # 群組 sprite
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()

        # 創建飛船
        player = Player()
        all_sprites.add(player)

        # 創建石頭 * 8
        for _ in range(8):
            new_rock()
            
        # 分數
        score = 0
    
    # 一秒鐘迴圈執行次數
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
    
    # rocks & bullets 碰撞處理(碰撞後刪除)
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    
    # 判斷石頭 & 子彈是否碰撞
    for hit in hits:
        
        # 隨機選取爆炸音樂
        # 調整音樂音量
        # 播放音樂
        expl_sound = random.choice(expl_sounds)
        expl_sound.set_volume(0.1)
        expl_sound.play()
        
        # 更新分數
        score += hit.radius
        
        # 大爆炸動畫
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        
        # 掉寶率為 10 %
        if random.random() > 0.9:
            
            # 創建寶物
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        
        # 重新創建石頭
        new_rock()
    
    # player & rocks 碰撞處理(rocks 碰撞後刪除)
    # 加強碰撞判斷(矩形 -> 圓形)
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    
    # 判斷飛船 & 石頭是否碰撞
    for hit in hits:
        
        # 重新創建石頭
        new_rock()
        
        # 減少生命值
        player.health -= hit.radius
        
        # 小爆炸動畫
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        
        # 判斷生命值是否小於等於 0
        if player.health <= 0:
            
            # 飛船爆炸動畫 & 音樂
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            
            # 減少血條
            player.lives -= 1
            
            # 刷新生命值
            player.health = 100
            
            # 隱藏飛船
            player.hide()
    
    # 判斷血條是否歸零 & 飛船爆炸動畫是否存在
    if player.lives == 0 and not death_expl.alive():
        
        # 顯示初始畫面
        show_init = True
    
    # player & powers 碰撞處理(powers 碰撞後刪除)
    hits = pygame.sprite.spritecollide(player, powers, True)
    
    # 判斷飛船 & 寶物是否碰撞
    for hit in hits:
        
        # 判斷寶物種類
        if hit.type == 'shield':
            
            # 增加生命值
            player.health += 20
            
            # 判斷生命值是否大於 100
            if player.health > 100:
                player.health = 100
                
            # 播放音樂
            shield_sound.play()
                
        elif hit.type == 'gun':
            
            # 子彈等級提升
            player.gunup()
            
            # 播放音樂
            gun_sound.play()
    
    # 畫面顯示
    # 畫面背景
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    
    # 畫出 sprites 群組
    all_sprites.draw(screen)
    
    # 顯示分數 & 生命條 & 血條
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    
    # 更新內容顯示到畫面上
    pygame.display.update()
    
pygame.quit()
