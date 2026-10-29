from stage_base import BaseStage

from actor_birdman    import Birdman
from actor_totem        import TotemPole
from actor_flyboard     import FlyBoard
from actor_tornado      import Tornado
from actor_island       import Island
from actor_fire         import Fire
from actor_bubble       import Bubble
from actor_harpy        import Harpy
from actor_bullet       import Bullet
from actor_airplane     import Airplane
from actor_food         import Food
from actor_uielement    import UIElement
from actor_background   import Background
from actor_laser        import Laser
import collision as col

import pygame


# 定数（このステージしか使わないので、Classに入れても良い）
MAX_BIRD   = 20
MAX_TOTEM   = 4
MAX_FLYBOARD = 6
MAX_TORNADOS = 6
MAX_FOOD     = 6
MAX_FIRE    = 10
MAX_BUBBLE  = 12
MAX_BULLET  = 128
MAX_LASER   = 2

WHITE = (255,255,255)

# True にするとデバッグ用隠しコマンド（1, 2 キー）が有効になる
DEBUG = False

# ハワイを出す座標
DESTINATION_X = 1100
DESTINATION_Y = 600


from enum import Enum

# シーン
class SCENE(Enum):
    START   = 0
    MIDST   = 1
    BOSS    = 2
    CLEAR   = 3
    FAILED  = 4
    

# ハワイのステージ
class HawaiiStage(BaseStage):
    def __init__(self, app, game_state):
        super().__init__(app, game_state)

        pass
    def __del__(self):
        pass

    def InitStage(self):
        # 変数の初期化
        self.score = 0
        self.life = 100
        self.max_combo = 0

        self.combo_count = 0
        self.max_life = 100
        self.journey = 0
        self.max_journey = 4000
        self.max_distance = 6481

        self.wait_cnt = 0

        self.scene = SCENE.START

        self.last_enemy = 0

        # ボスのライフ
        self.boss_life = 100

        for actor in self.actors:
            actor.Init()



    def LoadStageData(self):
        # Actorのインスタンス作成
        # アセットのロード

        # Actorを準備(順番注意)


        self.bg         = Background(self.owner_app, self)
        self.island     = Island(self.owner_app, self)
        self.birds      = [ Birdman(self.owner_app, self) for i in range(MAX_BIRD) ]
        self.totems     = [ TotemPole(self.owner_app, self) for i in range(MAX_TOTEM) ]
        self.flyboards  = [ FlyBoard(self.owner_app, self) for i in range(MAX_FLYBOARD) ]
        

        self.harpy      = Harpy(self.owner_app, self)
        self.bullets    = [ Bullet(self.owner_app, self) for i in range(MAX_BULLET)]
        self.plane      = Airplane(self.owner_app, self)
        self.fires      = [ Fire(self.owner_app, self) for i in range(MAX_FIRE) ]
        self.tornados   = [ Tornado(self.owner_app, self) for i in range(MAX_TORNADOS)]

        self.foods      = [ Food(self.owner_app, self) for i in range(MAX_FOOD)]

        self.lasers     = [ Laser(self.owner_app, self) for i in range(MAX_LASER) ]
        self.bubbles    = [ Bubble(self.owner_app, self) for i in range(MAX_BUBBLE) ]
        self.ui         = UIElement(self.owner_app, self)

        # ゲームオーバーの背景
        self.owner_app.GetRenderer().CreateSprite("game_over", "Asset/game_over.jpg")
        self.owner_app.GetRenderer().CreateFont("onryo", "Asset/onryou.TTF", 50)

        # SE読み込み
        self.crash_sound = "crash_sound"
        self.owner_app.GetMixer().CreateSoundEffects(self.crash_sound, "Asset/crash.wav")      

        # レイアウト読み込み
        self.layout_filename = "layout_hawaii.txt"
        #self.layout_filename = "layout_debug.txt" # デバッグ用
        self.LoadLayoutData(self.layout_filename)

        self.main_bgm   = "Asset/MusMus-BGM-121.mp3"
        self.clear_bgm  = "Asset/MusMus-BGM-139.mp3"
        self.boss_bgm   = "Asset/MusMus-BGM-122.mp3"
        self.failed_bgm   = "Asset/MusMus-BGM-112.mp3"

        pass

    # ステージデータを開放する
    def Release(self):
        self.actors.clear()
        pass


    # ここでメインの処理をする
    def StageMain(self):
        self.Update()

        self.DrawStage()


    # Actorの描画処理を呼ぶ
    def DrawStage(self):
        if(self.scene != SCENE.FAILED):
            for actor in self.actors:
                actor.Draw()

    def Update(self):
        # Actorのアップデート
        # 入力処理
        for actor in self.actors:
            if actor.GetDisp():
                actor.Update()

        if(self.scene == SCENE.START):
            self.SceneStart()
        if(self.scene == SCENE.MIDST):
            self.SceneMidst()
            self.CollisionMidst()
        if(self.scene == SCENE.BOSS):
            self.SceneBoss()
            self.CollisionBoss()
        if(self.scene == SCENE.CLEAR):
            self.SceneClear()
        if(self.scene == SCENE.FAILED):
            self.SceneFailed()



    # スタート中
    def SceneStart(self):
        self.wait_cnt += 1
        wait_frames = 60
        if self.wait_cnt > wait_frames:
            self.scene = SCENE.MIDST
            self.wait_cnt = 0
            self.plane.SetOperable(True)

            # BGM開始する
            self.owner_app.GetMixer().CreateBGM(self.main_bgm)
            self.owner_app.GetMixer().PlayBGM()

        self.plane.MoveToTarget()
        pass

    # ボス戦
    def SceneBoss(self):
        
        # ボスを倒した時
        if self.boss_life <= 0:
            self.boss_life = 0
            self.harpy.SetActive(False)
            self.plane.SetOperable(False)

            self.owner_app.GetMixer().StopBGM()
        
            # 画面上の羽を消す
            for feather in self.harpy.GetFeathers():
                if feather.GetDisp() == True:
                    feather.SetDisp(False)
            # 弾幕を消す
            for bullet in self.bullets:
                if bullet.GetDisp() == True:
                    bullet.SetDisp(False)
            # レーザーを消す
            for laser in self.lasers:
                if laser.GetDisp() == True:
                    laser.SetDisp(False)


        if self.harpy.GetY() > 900:
            self.scene = SCENE.CLEAR
#            self.plane.SetActive(False)
            self.plane.SetTarget(DESTINATION_X, DESTINATION_Y, 100)
            # BGM開始する
            self.owner_app.GetMixer().CreateBGM(self.clear_bgm)
            self.owner_app.GetMixer().PlayBGM()


        # ライフの確認
        if self.life <= 0:
            self.life = 0
            self.plane.SetActive(False)
            self.plane.SetOperable(False)


        if self.plane.GetY() > 900 :
            self.scene = SCENE.FAILED
            self.owner_app.GetMixer().CreateBGM(self.failed_bgm)
            self.owner_app.GetMixer().PlayBGM()
        pass

    # クリア中
    def SceneClear(self):

        # 加速度で制御するようにするべきか
        self.bg.SetBGSpeed(0)

        self.wait_cnt += 1
        if self.wait_cnt > 300:
            # 継続中のコンボも最大コンボに反映する
            self.ResetCombo()
            self.Transition()
 
        self.island.Update()
        self.plane.MoveToTarget()


    def SceneFailed(self):
        self.owner_app.GetRenderer().DrawSprite("game_over", 0, 0)
        self.owner_app.GetRenderer().DrawText("onryo", "ハワイに辿り着けませんでした。。", 100, 200, WHITE)
        self.owner_app.GetRenderer().DrawText("onryo", "皆が遊んでる間、東京でお仕事頑張ってください。。", 100, 350, WHITE)
        
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN] == 1:
            self.scene = SCENE.START
            self.InitStage()
            self.owner_app.GetMixer().StopBGM()


    # ゲームのメイン
    def SceneMidst(self):
        # ハワイまでの距離を計測
        self.journey += 1

        # ハワイに着いた時
        if self.journey > self.max_journey:

            self.scene = SCENE.BOSS
            self.boss_flag = True
            self.journey = self.max_journey
            self.harpy.Append(True, True)
            if self.island.GetDisp() == False:
                self.island.Append(DESTINATION_X, DESTINATION_Y)

            # ボスBGM開始する
            self.owner_app.GetMixer().CreateBGM(self.boss_bgm)
            self.owner_app.GetMixer().PlayBGM()


        # 敵の出現        
        if self.last_enemy < len(self.layout):
            while self.layout[self.last_enemy].frame == self.journey:
                # 鳥人
                if self.layout[self.last_enemy].enemy_type == 0:
                    for bird in self.birds:
                        if bird.GetDisp() == False:
                            bird.AppendLayout(self.layout[self.last_enemy].pos_x, self.layout[self.last_enemy].pos_y, self.layout[self.last_enemy].pattern)
                            break
                # トーテム
                elif self.layout[self.last_enemy].enemy_type == 1:
                    for totem in self.totems:
                        if totem.GetDisp() == False:
                            totem.AppendLayout(self.layout[self.last_enemy].pos_x, self.layout[self.last_enemy].pos_y, self.layout[self.last_enemy].pattern)
                            break
                # フライボード
                elif self.layout[self.last_enemy].enemy_type == 2:
                    for flyboard in self.flyboards:
                        if flyboard.GetDisp() == False:
                            flyboard.AppendLayout(self.layout[self.last_enemy].pos_x, self.layout[self.last_enemy].pos_y, self.layout[self.last_enemy].pattern)
                            break
                # 最終行のチェック
                self.last_enemy += 1
                if self.last_enemy >= len(self.layout):
                    break

        # ライフの確認
        if self.life <= 0:
            self.life = 0
            self.plane.SetActive(False)


        # 画面外でゲームオーバーに遷移する
        if self.plane.GetY() > 900 :
            self.scene = SCENE.FAILED
            self.owner_app.GetMixer().CreateBGM(self.failed_bgm)
            self.owner_app.GetMixer().PlayBGM()

        # デバッグ用
        self.Debug()

    # 当たり判定
    def CollisionMidst(self):

        self.CheckCollision(self.birds)
        self.CheckCollision(self.flyboards)
        

        # トーテムポール
        for totem in self.totems:
            if totem.GetActive() == True:
                # レーザー
                for laser in self.lasers:
                    if laser.GetDisp() == True:
                        if col.CollisionSquare(totem, laser) == True:

                            if totem.Collision() == True:
                                self.score += 1000
                            else:
                                self.owner_app.GetMixer().PlaySound(self.crash_sound)
                                
                            # 爆発表示                                                            
                            for fire in self.fires:
                                if fire.GetDisp() == False:
                                    fire.Append(laser.GetX(), laser.GetY())
                                    break
                            laser.SetDisp(False)

                # 自機
                if(self.plane.GetActive() == True):
                    if col.CollisionCircle(self.plane, totem) == True:
                        # 敵と自機が当たっている時
                        for fire in self.fires:
                            # 爆発表示                                
                            if fire.disp == False:
                                fire.Append(totem.GetX(), totem.GetY())
                                break
                        #totem.SetActive(False)

                        # 当たった時
                        if self.plane.Collision() == True:
                            self.life -= 6

                            # コンボリセット
                            self.ResetCombo()

        # トルネード
        for tornado in self.tornados:
            if tornado.GetDisp() == True and self.plane.GetActive() == True:
                if col.CollisionCircle(tornado, self.plane) == True:
                    #自機とトルネードが当たった時
                    if self.plane.Collision() == True:
                        self.life -= 3

        # アイテム
        for food in self.foods:
            if food.GetDisp() == True :#and self.plane.GetActive() == True:
                if col.CollisionCircle(food, self.plane) == True:
                    #自機と弾幕が当たった時
                    self.plane.ItemGet()
                    food.SetDisp(False)
                    self.life += 20
                    if self.life > 100:
                        self.life = 100


        # 弾幕
        for bullet in self.bullets:
            if bullet.GetDisp()  == True and self.plane.GetActive() == True:
                if col.CollisionCircle(bullet, self.plane) == True:
                    #自機と弾幕が当たった時
                    if self.plane.Collision() == True:
                        self.life -= 3
                        bullet.SetDisp(False)
                        


    # ボス戦用
    def CollisionBoss(self):

        self.CollisionMidst()

        # ボス
        if self.harpy.GetActive() == True:
            # レーザー
            for laser in self.lasers:
                if laser.GetDisp() == True:

                    if col.CollisionSquare(self.harpy, laser) == True:

                        if self.harpy.Collision() == True:
                            self.boss_life = self.harpy.GetLife()
                        else:
                            # レーザーとボスが当たった時
                            self.boss_life = self.harpy.GetLife()#-= 1.5
                            laser.SetDisp(False)
                            self.score += 5000
                        
                            for fire in self.fires:
                                # 爆発表示                                
                                if fire.disp == False:
                                    fire.Append(laser.GetX(), laser.GetY())
                                    break

                
                # 羽
                for feather in self.harpy.GetFeathers():
                    if feather.GetDisp() == True:
                        if col.CollisionSquare(feather, laser) == True:
                            # レーザーと羽が当たった時
                            laser.SetDisp(False)
                            

                        if col.CollisionSquare(feather, self.plane) == True:
                            # 自機と羽が当たった時
                             if self.plane.Collision() == True:

                                # 爆発表示    
                                for fire in self.fires:
                                    if fire.disp == False:
                                        fire.Append(feather.GetX(), feather.GetY())
                                        break

                                self.life -= 5
                                feather.SetDisp(False)
                                self.owner_app.GetMixer().PlaySound(self.crash_sound)


    # 衝突チェック
    def CheckCollision(self, enemies):
        # 敵
        for enemy in enemies:
            if enemy.GetActive() == True:
                # レーザー
                for laser in self.lasers:
                    if laser.GetDisp() == True:
                        if col.CollisionSquare(enemy, laser) == True:
                            # 敵とレーザーが当たっている時
                            # コンボ加算
                            if enemy.Collision() == True:
                                self.combo_count += 1
                                score = 100 * self.combo_count
                                self.score += score
                                
                            # 吹き出し
                            for bubble in self.bubbles:
                                if bubble.GetDisp() == False:
                                    bubble.SetMessage("グエっ")
                                    bubble.Append(enemy.GetX(), enemy.GetY())
                                    break

                # 自機
                if(self.plane.GetActive() == True):
                    if col.CollisionCircle(self.plane, enemy) == True:

                        # 当たった時
                        if self.plane.Collision() == True:

                            # 敵と自機が当たっている時
                            for fire in self.fires:
                                # 爆発表示                                
                                if fire.disp == False:
                                    fire.Append(enemy.GetX(), enemy.GetY())
                                    break
                            enemy.SetActive(False)


                            self.life -= 6

                            # コンボリセット
                            self.ResetCombo()
                            enemy.Append(False, False)

                            # 吹き出し
                            for bubble in self.bubbles:
                                if bubble.GetDisp() == False:
                                    bubble.SetMessage("痛っ！")
                                    bubble.Append(self.plane.GetX() + 50,self.plane.GetY())
                                    break

                if(enemy.GetX() < -100):
                    # 通り過ぎたら消える
                    enemy.Append(False, False)
                    # コンボリセット
                    self.ResetCombo()

        pass

    # 最大コンボを更新してからコンボをリセットする
    def ResetCombo(self):
        if self.max_combo < self.combo_count:
            self.max_combo = self.combo_count
        self.combo_count = 0


    def GetBullets(self):
        return self.bullets
    def GetLasers(self):
        return self.lasers
    def GetTornados(self):
        return self.tornados
    def GetBubbles(self):
        return self.bubbles
    def GetFoods(self):
        return self.foods

    
    def Debug(self):
        ## デバッグ用隠しコマンド
        if DEBUG == False:
            return
        key = pygame.key.get_pressed()
        if key[pygame.K_2] == True:
            self.journey = self.max_journey - 100
        if key[pygame.K_1] == True:
            self.life = 1



