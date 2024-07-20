import arcade 
from models import World
from random import randint
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle
    def draw(self):
        self.sync_with_model()
        super().draw()

class NinninWindow(arcade.Window):
    SLEEP = 0.5
    def __init__(self,width,height):
        super().__init__(width,height)
        self.background = None
        arcade.set_background_color(arcade.color.AMAZON)
        self.wait_time = 0
        self.rand = 0
        self.setninja1 = ['images/char1.png','images/char2.png','images/char3.png','images/char4.png','images/char5.png','images/char6.png']
        self.setninja2 = ['images/char1flip.png','images/char2flip.png','images/char3flip.png','images/char4flip.png','images/char5flip.png','images/char6flip.png']
        self.setninja = [self.setninja1,self.setninja2]
        self.setsheild = ['images/sheild.png','images/sheildflip.png']
        self.background = arcade.load_texture("images/background.png")
        self.world = World()
        #character
        self.ninja = ModelSprite(self.setninja[0][0],model = self.world.ninja)
        self.sheild = ModelSprite(self.setsheild[0],model = self.world.sheild)
        #item
        self.gensheild = ModelSprite('images/item4.png',model = self.world.gensheild)
        self.barrel = ModelSprite('images/item1.png',model = self.world.barrel)
        self.barrel2 = ModelSprite('images/item1.png',model = self.world.barrel2)
        self.shuriken = ModelSprite('Images/item2.png',model = self.world.shuriken1)
        self.knife = ModelSprite('images/item3.png',model = self.world.knife)
        #text
        self.textscore = self.ReadScore()
    def setup(self): #for restart
        self.world = World()
        #character
        self.ninja = ModelSprite(self.setninja[0][0],model = self.world.ninja)
        self.sheild = ModelSprite(self.setsheild[0],model = self.world.sheild)
        #item
        self.gensheild = ModelSprite('images/item4.png',model = self.world.gensheild)
        self.barrel = ModelSprite('images/item1.png',model = self.world.barrel)
        self.barrel2 = ModelSprite('images/item1.png',model = self.world.barrel2)
        self.shuriken = ModelSprite('Images/item2.png',model = self.world.shuriken1)
        self.knife = ModelSprite('images/item3.png',model = self.world.knife)
        #text
        self.textscore = self.ReadScore()    
    def ReadScore(self):
        file = open("highscore.txt","r")
        return file.read()
    def WriteScore(self):
        file = open("highscore.txt","w")
        file.write(str(self.world.score))
        file.close()
    def on_key_press(self, key, key_modifiers):
        if(self.world.ninja.status == 1):  #gameplay
            self.world.on_key_press(key, key_modifiers)
        elif(self.world.ninja.status == 0): #gamerestart
            self.setup()
    def update(self,delta):
        if(self.world.ninja.status == 1): #gameplay
            self.world.update(delta)
            
            self.ninja = ModelSprite(self.setninja[self.world.flip][self.world.ninja.pic],model = self.world.ninja) #change pic character
            self.sheild = ModelSprite(self.setsheild[self.world.flip],model = self.world.sheild) #change pic sheild
            #write score & highscore
            self.textscore = self.ReadScore()
            if(self.world.score>int(self.textscore)): 
                self.WriteScore()
    def drawgameplay(self):
        self.ninja.draw()
        self.sheild.draw()
        self.gensheild.draw()
        self.barrel.draw()
        self.shuriken.draw()
        self.knife.draw()
        self.barrel2.draw()
        arcade.draw_text(str("Score: "+str(self.world.score)),self.width - 400, self.height - 80,arcade.color.BLUE, 20)
        arcade.draw_text(str("HighScore: "+self.textscore),self.width - 400, self.height - 30,arcade.color.RED, 30)
    def drawgameover(self):
        arcade.draw_text(str("Press Any KEY To Restart"),self.width-340, self.height - 400,arcade.color.RED, 20)
        arcade.draw_text(str("HighScore: "+self.textscore),self.width - 280, self.height - 450,arcade.color.BLUE, 15)
        arcade.draw_text(str("YourScore: "+str(self.world.score)),self.width - 270, self.height -500,arcade.color.BLUE, 15)
    def on_draw(self):
        arcade.start_render()
        
        if(self.world.ninja.status == 1):
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
            self.drawgameplay()
        elif(self.world.ninja.status == 0):
            self.drawgameover()
        


if __name__ == '__main__':
    window =NinninWindow(SCREEN_WIDTH,SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()