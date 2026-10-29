from actor import Actor


import pygame

class Airplane(Actor):
    def __init__(self, app, stage):
        super().__init__(app, stage)

        self.sprite_name = "plane"
        self.owner_app.GetRenderer().CreateSprite(self.sprite_name, "Asset/airplane.png")

        # スプライトから当たり判定用のサイズ取得
        self.w, self.h = self.owner_app.GetRenderer().GetSpriteSize(self.sprite_name)
        self.radius = self.h/2/2# 微調整

        self.sprite_name_dead = "plane_dead"
        self.owner_app.GetRenderer().CreateSprite(self.sprite_name_dead, "Asset/plane_dead.png")


        self.pin_sound = "pin_sound"
        self.owner_app.GetMixer().CreateSoundEffects(self.pin_sound, "Asset/pin.mp3")        


        self.damage_sound = "ite_sound"
        self.owner_app.GetMixer().CreateSoundEffects(self.damage_sound, "Asset/ite.mp3") 

        self.heal_sound = "heal_sound"
        self.owner_app.GetMixer().CreateSoundEffects(self.heal_sound, "Asset/heal.mp3")       


    def __del__(self):
        pass

    def Init(self):
        super().Init()
        self.x = 0
        self.y = 200
        self.disp = True
        self.active = True
        self.shot_key_pressed = False
        self.speed = 4
        # 操作可能であるか
        self.operable = False
        self.SetTarget(200, 200, 60)

        self.collision_cnt = 60
        


    def Update(self):
        # 生きている時
        if self.active == True:
            self.collision_cnt += 1

            if self.operable == True:
                key = pygame.key.get_pressed()

                if key[pygame.K_UP] == True:
                    self.y -= self.speed
                    if self.y < -10:
                        self.y = -10
                if key[pygame.K_DOWN] == True:
                    self.y += self.speed
                    if self.y > self.owner_app.GetRenderer().GetScreenH() + 10:
                        self.y = self.owner_app.GetRenderer().GetScreenH() + 10
                if key[pygame.K_LEFT] == True:
                    self.x -= self.speed
                    if self.x < -10:
                        self.x = -10
                if key[pygame.K_RIGHT] == True:
                    self.x += self.speed
                    if self.x > self.owner_app.GetRenderer().GetScreenW() - 50:
                        self.x = self.owner_app.GetRenderer().GetScreenW() - 50

                if key[pygame.K_SPACE] == 1:
                    if self.shot_key_pressed == False:
                        self.shot_key_pressed = True
                        for laser in self.owner_stage.GetLasers():
                            if laser.GetDisp() == False:
                                laser.Spawn(self.x+100, self.y)                   
                                break
                        self.owner_app.GetMixer().PlaySound(self.pin_sound)
                else :
                    self.shot_key_pressed = False
        # 死んだ時
        else:
            self.y += 10       


    def Draw(self):
        if(self.disp == True):
            if(self.active == True):
                #self.owner_app.GetRenderer().DrawSprite(self.sprite_name, self.x, self.y)
                if self.collision_cnt > 60:
                    self.owner_app.GetRenderer().DrawSpriteAdjustCenter(self.sprite_name, self.x, self.y)
                else:
                    if self.collision_cnt %2 == 0:
                        self.owner_app.GetRenderer().DrawSpriteAdjustCenter(self.sprite_name, self.x, self.y)

            else:
                self.owner_app.GetRenderer().DrawSpriteAdjustCenter(self.sprite_name_dead, self.x, self.y)

    # ターゲット座標に向かって動かす
    def MoveTo(self, x, y, val):
        move_x = x - self.x
        move_y = y - self.y

        self.x += int(move_x / val)
        self.y += int(move_y / val)


    # 操作可否を設定
    def SetOperable(self, operable):
        self.operable = operable

    # 撃たれた時
    def Collision(self):
        if self.collision_cnt > 60 :
            self.collision_cnt = 0

            # ダメージ効果音
            self.owner_app.GetMixer().PlaySound(self.damage_sound)

            for bubble in self.owner_stage.GetBubbles():
                bubble.SetMessage("痛っ！")
                bubble.Spawn(self.x+ 50,self.y)
                break


            return True
        else:
            return False

    # アイテムを取った時
    def ItemGet(self):
        for bubble in self.owner_stage.GetBubbles():
            bubble.SetMessage("回復")
            bubble.Spawn(self.x+ 50,self.y)
            break

        # 回復効果音
        self.owner_app.GetMixer().PlaySound(self.heal_sound)

