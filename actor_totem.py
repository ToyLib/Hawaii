from actor import Actor
import math

class TotemPole (Actor):
    def __init__(self, app, stage):
        super().__init__(app, stage)
        self.cnt = 0
        self.angle = 0

        self.sprite_name = "totem"
        self.owner_app.GetRenderer().CreateSprite(self.sprite_name, "Asset/totem_pole.png")
        self.sprite_name_dead = "totem_dead"
        self.owner_app.GetRenderer().CreateSprite(self.sprite_name_dead, "Asset/totem_pole_dead.png")

        # スプライトから当たり判定用のサイズ取得
        self.w, self.h = self.owner_app.GetRenderer().GetSpriteSize(self.sprite_name)
        self.radius = self.w # 使わない
        self.w /= 4

        self.life = 10

        self.pattern = 0

        # 行動パターンをリスト化
        self.Behavior = [
            self.Behavior_0, 
            self.Behavior_1, 
            self.Behavior_2, 
            self.Behavior_3, 
            self.Behavior_4]


        self.damage_sound = "gue2_sound"
        self.owner_app.GetMixer().CreateSoundEffects(self.damage_sound, "Asset/gue2.mp3")



    def __del__(self):
        pass

    def Init(self):
        super().Init()
    
    # 弾幕を撃つ
    def ShootBullet(self):
        bullet_angle = 30
        for i in range(0, int(360/bullet_angle)):
            for bullet in  self.owner_stage.GetBullets():
                if(bullet.GetDisp() == False):
                    x = self.x + math.cos(math.radians(i*bullet_angle)) * 50
                    y = self.y + math.sin(math.radians(i*bullet_angle)) * 50
                    bullet.Spawn(x, y)
                    bullet.SetAngle(i*bullet_angle)
                    bullet.SetSpeed(5)
                    break
        

    # パターン別
    def Behavior_0(self):
        self.angle += 2
        self.y += math.sin(math.radians(self.angle)) * 2
        self.x -= 2

        if self.cnt % 30 == 0:
            self.ShootBullet()

    def Behavior_1(self):
        pass
    def Behavior_2(self):
        pass

    def Behavior_3(self):
        pass
    def Behavior_4(self):
        pass

    # 撃たれた時
    def Collision(self):
        self.life -= 1

        if self.life <= 0:
            self.active = False
            # ダメージ効果音
            self.owner_app.GetMixer().PlaySound(self.damage_sound)
            return True
        else:
            return False

    def Update(self):

        if self.active == True:
            self.cnt += 1
            self.Behavior[self.pattern]()

        else:
            self.y += 5
            if self.y > self.owner_app.GetRenderer().GetScreenH():
                self.disp = False
 
    def Draw(self):
        if self.disp == True:    
            if self.active == True:
                self.owner_app.GetRenderer().DrawSpriteAdjustCenter(self.sprite_name, self.x, self.y)
            else:
                self.owner_app.GetRenderer().DrawSpriteAdjustCenter(self.sprite_name_dead, self.x, self.y)


    def SpawnFromLayout(self, pos_x, pos_y, pattern):
        self.disp = True
        self.active = True
        self.x = pos_x
        self.y = pos_y
        self.pattern = pattern
        self.cnt = 0
        self.angle = 0
        self.life = 10

