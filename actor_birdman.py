from actor import Actor
import math

class Birdman(Actor):
    def __init__(self, app, stage):
        super().__init__(app, stage)
        self.cnt = 0
        self.angle = 0

        self.sprite_name = "bird"
        self.owner_app.GetRenderer().CreateSprite(self.sprite_name, "Asset/bird.png")
        
        # スプライトから当たり判定用のサイズ取得
        self.w, self.h = self.owner_app.GetRenderer().GetSpriteSize(self.sprite_name)
        self.radius = self.h / 2 # 微調整

        self.sprite_name_dead = "bird_dead"
        self.owner_app.GetRenderer().CreateSprite(self.sprite_name_dead, "Asset/bird_dead.png")

        self.pattern = 0

        # 行動パターンをリスト化
        self.Behavior = [
            self.Behavior_0, 
            self.Behavior_1, 
            self.Behavior_2, 
            self.Behavior_3, 
            self.Behavior_4]


        self.damage_sound = "gue_sound"
        self.owner_app.GetMixer().CreateSoundEffects(self.damage_sound, "Asset/gue.mp3")


    def __del__(self):
        pass

    def Init(self):
        return super().Init()
    
    # 弾幕を撃つ
    def ShootBullet(self):
        bullet_angle = 45
        for i in range(0, int(360/bullet_angle)):
            for bullet in  self.owner_stage.GetBullets():
                if(bullet.GetDisp() == False):
                    x = self.x + math.cos(math.radians(i*bullet_angle)) * 50
                    y = self.y + math.sin(math.radians(i*bullet_angle)) * 50
                    bullet.Append(x, y)
                    bullet.SetAngle(i*bullet_angle)
                    bullet.SetSpeed(5)
                    break
        

    # パターン別
    def Behavior_0(self):
        self.angle += 5
        self.y += math.sin(math.radians(self.angle)) * 6
        self.x -= 6

        if self.cnt % 60 == 0:
            self.ShootBullet()

    def Behavior_1(self):

        if self.cnt < 50:
            self.x -= 10
        elif self.cnt < 90:
            pass
        elif self.cnt == 90:
            self.ShootBullet()
        elif self.cnt < 120:
            self.x -= 20
            self.y += math.sin(self.cnt)
        else:
            self.cnt = 0
 

        pass
    def Behavior_2(self):
        self.x -= 9
        if self.cnt % 20 == 0:
            self.ShootBullet()
        pass

    def Behavior_3(self):
        pass
    def Behavior_4(self):
        pass

    def Update(self):
        if self.active == True:
            self.cnt += 1
            self.Behavior[self.pattern]()

        else:
            self.y += 10        
            if self.y > self.owner_app.GetRenderer().GetScreenH():
                self.disp = False
 
    def Draw(self):
        if(self.disp == True):    
            if(self.active == True):
                self.owner_app.GetRenderer().DrawSpriteAdjustCenter(self.sprite_name, self.x, self.y)
            else:
                self.owner_app.GetRenderer().DrawSpriteAdjustCenter(self.sprite_name_dead, self.x, self.y)


# 余裕あったらこのメソッドは見直す
    def Append(self, disp, active):
        self.disp = disp
        self.active = active
#        self.y = random.randint(100, 500)
        self.x = self.owner_app.GetRenderer().GetScreenW()+50

    def AppendLayout(self, pos_x, pos_y, pattern):
        self.disp = True
        self.active = True
        self.x = pos_x
        self.y = pos_y
        self.pattern = pattern
        self.cnt = 0
        self.angle = 0



    def Collision(self):
        self.active = False
        # ダメージ効果音
        self.owner_app.GetMixer().PlaySound(self.damage_sound)
        return True