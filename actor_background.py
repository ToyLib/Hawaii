from actor import Actor

BG_WIDTH = 2048

class Background(Actor):
    def __init__(self, app, stage):
        super().__init__(app, stage)

        # ゲーム中背景
        self.sprite_name = "blue_sky"
        self.owner_app.GetRenderer().CreateSprite(self.sprite_name, "Asset/blue_sky.jpg")
        self.sprite_name_night = "night_sky"
        self.owner_app.GetRenderer().CreateSprite(self.sprite_name_night, "Asset/night_sky.jpg")

    def Init(self):
        super().Init()
        self.disp = True
        self.bg_speed = 8
        self.bg_x = 0

        self.alpha = 0
        
    def __del__(self):
        pass

    def Update(self):
        self.bg_x = (self.bg_x - self.bg_speed) % BG_WIDTH
        pass
                
    def Draw(self):
        if(self.disp == True):
            self.owner_app.GetRenderer().DrawSprite(self.sprite_name , self.bg_x - BG_WIDTH, 0)
            self.owner_app.GetRenderer().DrawSprite(self.sprite_name , self.bg_x, 0)

            if(self.alpha < 255):
                self.alpha += 0.05
            self.owner_app.GetRenderer().SetAlpha(self.sprite_name_night, self.alpha)
            self.owner_app.GetRenderer().DrawSprite(self.sprite_name_night , self.bg_x - BG_WIDTH, 0)
            self.owner_app.GetRenderer().DrawSprite(self.sprite_name_night , self.bg_x, 0)


    # Getter/Setter
    def SetBGSpeed(self, speed):
        self.bg_speed = speed
