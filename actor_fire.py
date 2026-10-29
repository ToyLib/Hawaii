from actor import Actor

class Fire(Actor):
    def __init__(self, app, stage):
        super().__init__(app, stage)

        self.sprite_name = "fire"
        self.owner_app.GetRenderer().CreateSprite(self.sprite_name, "Asset/bomb.png")
        self.w, self.h = self.owner_app.GetRenderer().GetSpriteSize(self.sprite_name)


    def __del__(self):
        pass

    def Init(self):
        super().Init()
        self.anim = 0

    def Update(self):
        if self.disp == False:
            return

        self.cnt += 1
        if(self.cnt % 3 == 0):
            self.anim += 1
            if self.anim == 15:
                self.anim = 0
                self.disp = False
                
    def Draw(self):
        if(self.disp == True):
            self.owner_app.GetRenderer().DrawSpriteRectAdjustCenter(self.sprite_name, self.anim*80, 0, 80, 80, self.x, self.y )

    def Spawn(self, x, y):
        self.disp = True
        self.x = x
        self.y = y
