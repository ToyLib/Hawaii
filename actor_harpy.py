
from actor import Actor
from actor_feather import Feather

import math

MAX_FEATHER = 8

class Harpy(Actor):
    def __init__(self, app, stage):
        super().__init__(app, stage)
        self.cnt = 0
        self.angle = 0

        self.sprite_name = "harpy"
        self.owner_app.GetRenderer().CreateSprite(self.sprite_name, "Asset/harpy.png")
        self.sprite_name_dead = "harpy_dead"
        self.owner_app.GetRenderer().CreateSprite(self.sprite_name_dead, "Asset/harpy_dead.png")
 
        # スプライトから当たり判定用のサイズ取得
        self.w, self.h = self.owner_app.GetRenderer().GetSpriteSize(self.sprite_name)
        self.w = self.w / 2
        self.h = self.h / 2
        self.radius = self.w / 2 # 微調整

        self.feathers = [ Feather(app, stage, self) for i in range(MAX_FEATHER) ]

        # 行動パターンをリスト化
        self.Behavior = [
            self.Behavior_0, 
            self.Behavior_1, 
            self.Behavior_2, 
            self.Behavior_3, 
            self.Behavior_4]
        
        self.behave_cnt = 0
        self.behave_id = 0

        self.damage_sound = "hyun_sound"
        self.owner_app.GetMixer().CreateSoundEffects(self.damage_sound, "Asset/hyun.mp3") 

        self.life = 100       


    def __del__(self):
        pass

    def Init(self):
        super().Init()
        self.x = 1300
        self.y = 400
        self.cnt = 0
        self.angle = 0
        self.behave_id = 0
        self.behave_cnt = 0
        self.life = 100

        #self.bullets = self.owner_stage.GetBullets()


    def Update(self):
        self.cnt += 1

        if self.active == True:
            self.Behavior[self.behave_id]()
        else:
            self.y += 5
        

    def Behavior_0(self):
        self.behave_cnt += 1   
            
        if self.behave_cnt == 1:
            self.SetTarget(1000, 400, 30)

        self.MoveToTarget()

        if self.behave_cnt == 120:
            self.behave_id = 1
            self.behave_cnt = 0


    def Behavior_1(self):
        self.behave_cnt += 1

        self.angle += 10
        self.x += math.cos(math.radians(self.angle)) * 20
        self.y -= math.sin(math.radians(self.angle)) * 20


        # 弾幕を出す
        if self.behave_cnt % 10 == 0:
            bullet_angle = 20

            for i in range(0, int(360/bullet_angle)):
                for bullet in  self.owner_stage.GetBullets():
                    if(bullet.GetDisp() == False):
                        x = self.x + math.cos(math.radians(i*bullet_angle)) * 50
                        y = self.y + math.sin(math.radians(i*bullet_angle)) * 50
                        bullet.Spawn(x, y)
                        bullet.SetAngle(i*bullet_angle)
                        bullet.SetSpeed(5)
                        break

        if self.behave_cnt == 108:
            self.behave_cnt = 0
            self.behave_id = 2


    def Behavior_2(self):
        self.behave_cnt += 1

        if self.behave_cnt == 10:
            val = 100
            self.feathers[0].Spawn(self.x, self.y)
            self.feathers[0].SetTarget(self.x + 50, self.y - 100, val)

            self.feathers[1].Spawn(self.x, self.y)
            self.feathers[1].SetTarget(self.x + 100, self.y - 150, val)

            self.feathers[2].Spawn(self.x, self.y)
            self.feathers[2].SetTarget(self.x + 10, self.y + 100, val)

            self.feathers[3].Spawn(self.x, self.y)
            self.feathers[3].SetTarget(self.x + 100, self.y + 150, val)


        # 羽を飛ばす
        cnt_offset = 200
        if self.behave_cnt == cnt_offset:
            self.feathers[0].SetTarget(-60, 360, 10)
        if self.behave_cnt == cnt_offset + 50:
            self.feathers[1].SetTarget(-60, 360, 10)
        if self.behave_cnt == cnt_offset + 100:
            self.feathers[2].SetTarget(-60, 360, 10)
        if self.behave_cnt == cnt_offset + 150:
            self.feathers[3].SetTarget(-60, 360, 10)

        if self.behave_cnt == cnt_offset + 250:
            self.behave_cnt = 0
            self.behave_id = 3

    def Behavior_3(self):
        self.behave_cnt += 1

        cnt_offset = 10

        if self.behave_cnt == cnt_offset:
            self.SetTarget(1000, 100, 30)
        if self.behave_cnt == cnt_offset + 200:
            self.SetTarget(1000, 600, 30)
        if self.behave_cnt == cnt_offset + 400:
            self.SetTarget(1000, 100, 30)
        if self.behave_cnt == cnt_offset + 600:
            self.SetTarget(1000, 600, 30)
        if self.behave_cnt == cnt_offset + 800:
            self.SetTarget(1000, 400, 30)

        if self.behave_cnt == cnt_offset + 1000:
            self.behave_cnt = 0
            self.behave_id = 4

        self.MoveToTarget()    


        # 弾幕を出す
        if(self.behave_cnt > cnt_offset):
            if self.behave_cnt % 15 == 0:
                bullet_angle = 20

                for i in range(0, int(360/bullet_angle)):
                    for bullet in  self.owner_stage.GetBullets():
                        if(bullet.GetDisp() == False):
                            x = self.x + math.cos(math.radians(i*bullet_angle)) * 50
                            y = self.y + math.sin(math.radians(i*bullet_angle)) * 50
                            bullet.Spawn(x, y)
                            bullet.SetAngle(i*bullet_angle)
                            bullet.SetSpeed(5)
                            break

        pass
    def Behavior_4(self):
        self.behave_cnt += 1
        cnt_offset = 10

        feather_angle = 45
        if self.behave_cnt == cnt_offset:
            for i in range(0, 8):
                for feather in self.feathers:
                    if(feather.GetDisp() == False):
                        x = self.x + math.cos(math.radians(i*feather_angle)) * 50
                        y = self.y + math.sin(math.radians(i*feather_angle)) * 50
                        feather.Spawn(x, y)
                        dst_x = self.x + math.cos(math.radians(i*feather_angle)) * 200
                        dst_y = self.y + math.sin(math.radians(i*feather_angle)) * 200
                        feather.SetTarget(dst_x, dst_y, 60)
                        feather.SetOffset(200, i*feather_angle)
                        break

        if self.behave_cnt == cnt_offset + 150:
            for feather in self.feathers:
                if(feather.GetDisp() == True):
                    feather.SetBehaveID(1)

        if self.behave_cnt == cnt_offset + 150:
            self.SetTarget(800, 200, 30)
        if self.behave_cnt == cnt_offset + 270:
            self.SetTarget(1000, 500, 30)
        if self.behave_cnt == cnt_offset + 390:
            self.SetTarget(1000, 200, 30)
        if self.behave_cnt == cnt_offset + 510:
            self.SetTarget(800, 500, 30)
        if self.behave_cnt == cnt_offset + 630:
            self.SetTarget(1000, 400, 30)


        # 羽を飛ばす
        if self.behave_cnt == cnt_offset + 900:
            for feather in self.feathers:
                if feather.GetDisp():
                    feather.SetTarget(-60, 360, 10)
                    feather.SetBehaveID(0)
                    break
        if self.behave_cnt == cnt_offset + 950:
            for feather in self.feathers:
                if feather.GetDisp():
                    feather.SetTarget(-60, 360, 10)
                    feather.SetBehaveID(0)
                    break
        if self.behave_cnt == cnt_offset + 1000:
            for feather in self.feathers:
                if feather.GetDisp():
                    feather.SetTarget(-60, 360, 10)
                    feather.SetBehaveID(0)
                    break
        if self.behave_cnt == cnt_offset + 1050:
            for feather in self.feathers:
                if feather.GetDisp():
                    feather.SetTarget(-60, 360, 10)
                    feather.SetBehaveID(0)
                    break
        if self.behave_cnt == cnt_offset + 1100:
            for feather in self.feathers:
                if feather.GetDisp():
                    feather.SetTarget(-60, 360, 10)
                    feather.SetBehaveID(0)
                    break
        if self.behave_cnt == cnt_offset + 1150:
            for feather in self.feathers:
                if feather.GetDisp():
                    feather.SetTarget(-60, 360, 10)
                    feather.SetBehaveID(0)
                    break
        if self.behave_cnt == cnt_offset + 1200:
            for feather in self.feathers:
                if feather.GetDisp():
                    feather.SetTarget(-60, 360, 10)
                    feather.SetBehaveID(0)
                    break
        if self.behave_cnt == cnt_offset + 1250:
            for feather in self.feathers:
                if feather.GetDisp():
                    feather.SetTarget(-60, 360, 10)
                    feather.SetBehaveID(0)
                    break


        if self.behave_cnt == cnt_offset + 1400:
            self.behave_id = 1
            self.behave_cnt = 0

        self.MoveToTarget()


    def Draw(self):
        if(self.disp == True):    
            if(self.active == True):
                self.owner_app.GetRenderer().DrawSpriteAdjustCenter(self.sprite_name, self.x, self.y)
            else:
                self.owner_app.GetRenderer().DrawSpriteAdjustCenter(self.sprite_name_dead, self.x, self.y)



    # 出現
    def Spawn(self):
        self.Init()
        self.disp = True
        self.active = True
        self.x = self.owner_app.GetRenderer().GetScreenW()


    def GetFeathers(self):
        return self.feathers
    #def GetBullets(self):
    #    return self.bullets

    def Collision(self):
        self.life -= 1.5
        if self.life > 0:
            return False
        else:
            self.life = 0
            # ダメージ効果音
            self.owner_app.GetMixer().PlaySound(self.damage_sound)
            return True

    def GetLife(self):
        return self.life