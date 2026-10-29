from actor import Actor
import math

class Tornado(Actor):
    def __init__(self, app, stage):
        super().__init__(app, stage)

        self.cnt = 0
        self.move_cnt = 0
        self.move_val = 0

        self.sprite_name = "tornado"
        self.owner_app.GetRenderer().CreateSprite(self.sprite_name, "Asset/tornado.png")
        # スプライトから当たり判定用のサイズ取得
        self.w, self.h = self.owner_app.GetRenderer().GetSpriteSize(self.sprite_name)
        self.w = self.w / 2
        self.h = self.h / 2
        self.radius = self.w

        self.angle = 0


        # 行動パターンをリスト化
        self.Behavior = [
            self.Behavior_0, 
            self.Behavior_1, 
            self.Behavior_2, 
            self.Behavior_3, 
            self.Behavior_4]

        self.behave_cnt = 0
        self.behave_id = 0

        self.parent_actor = None

        self.wind_sound = "wind_sound"
        self.owner_app.GetMixer().CreateSoundEffects(self.wind_sound, "Asset/Wind-Synthetic01-2.mp3")

    def __del__(self):
        pass

    def Init(self):
        super().Init()

        self.disp = False


    def Update(self):
        
        self.cnt += 1
        self.Behavior[self.behave_id]()
            

    def Behavior_0(self):
        self.x = self.parent_actor.GetX()
        self.y = self.parent_actor.GetY() + 80
        pass

    def Behavior_1(self):
        self.behave_cnt += 1

        self.angle += 0.5
        self.x -= math.cos(self.angle) * 10
        self.y -= math.sin(self.angle) * 10

        if self.behave_cnt > 60:
            self.behave_id = 2
            self.behave_cnt = 0
            self.owner_app.GetMixer().PlaySound(self.wind_sound)
    
        pass

    def Behavior_2(self):
        self.behave_cnt += 1
#        self.x -= 10

        self.angle += 0.1
        self.x -= math.cos(self.angle) * 20
        self.y -= math.sin(self.angle) * 20

        self.x -= 5


        if self.x < -50:
            self.disp = False

        pass

    def Behavior_3(self):
        pass

    def Behavior_4(self):
        pass


    def Draw(self):
        if(self.disp == True):
            self.owner_app.GetRenderer().DrawSpriteAdjustCenter(self.sprite_name, self.x, self.y)


  
    # 出現
    def Append(self, x, y):
        self.disp = True
        self.x = x
        self.y = y+80
        self.behave_id = 0

    # 振る舞いIDを変更（同時にカウンタもリセット）
    def SetBehaveID(self, behave_id):
        self.behave_id = behave_id
        self.behave_cnt = 0
    
    def SetParentActor(self, parent):
        self.parent_actor = parent


