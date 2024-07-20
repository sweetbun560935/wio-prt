import arcade.key
from random import randint

class Ninja:
    def __init__(self,world,x,y,angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0
        self.move = 0
        self.vx = 0
        self.vy =0
        self.pic = 0
        self.speed =22
        self.status = 1
    def direction(self):
        if self.move == 0:
            self.vx = -self.speed
        elif self.move == 1:
            self.vx = self.speed
    def onhit(self,other,hit_sizex,hit_sizey):
        if((abs(self.x - other.x)<=hit_sizex)and(abs(self.y-other.y)<=hit_sizey)):
            return True
        else: 
            return False
    def Die(self):
        self.vy =-15
    def update(self,delta):
        self.y+=self.vy
        self.x+=self.vx
        if(self.y<0):
            self.status = 0
        if(abs(400-self.x)<=32): 
            self.x = 368
            self.vx = 0
            self.move = 0
        elif(abs(400-self.x)>=368):
            self.x = 32
            self.vx = 0
            self.move = 1
class Sheild():
    TIMEDELAY = 0.2
    def __init__(self,world,x,y,angle):
        self.x = x
        self.y = y
        self.angle = 0        
        self.posx = -100
        self.posy = -100
    def cancel(self):
        self.posx  = -100
    def position(self,x,y):
        self.posx = x
        self.posy = y
    def update(self,delta):
        self.x = self.posx
        self.y = self.posy
class Item():
    def __init__(self,world,x,y,angle):
        self.x = -100
        self.y = randint(1000,1020)
        self.angle = 0        
        self.posx = [32,368] #position x axis 
        self.move = [10,10]
        self.speed = self.move[randint(0,1)]
    def random_location(self,range1,range2):
        self.rand = randint(range1,range2) #random for check item is droping
        if(self.rand == 0):
            self.x = self.posx[randint(0,1)] #random position x axis
        else:
            self.x = -100
        self.y = randint(1000,1020)
        self.speed = self.move[randint(0,1)]
    def cancel(self):
        self.x  = -100
    def setspeed(self,A,B):
        self.move = [A,B]
    def update(self,delta):
            self.y -= self.speed
class World:
    TIMECHANGE = 0.075
    def __init__(self):
        self.addscore = 1
        self.score = 0
        self.time = 0 #time for random items drop
        self.timepic = 0 #time for change pic
        self.check =0
        self.flip = 0
        self.limitscore = 2500 #point of change level
        #speed of item 
        self.speeditem1 =11
        self.speeditem2 =12

        self.live = 1

        self.ninja = Ninja(self,368,100,0)
        self.sheild = Sheild(self,368,100,0)

        self.barrel = Item(self,0,0,0)
        self.shuriken1 = Item(self,0,0,0)
        self.knife = Item(self,0,0,0)
        self.gensheild = Item(self,0,0,0)
        self.barrel2 = Item(self,0,0,0)
        #list of items
        self.item1 = [self.barrel,self.shuriken1,self.knife,self.barrel2]
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE and self.live != 0:
            self.ninja.direction()
            if(self.ninja.x==32 or self.ninja.x==368): #flip character
                self.flip+=1
                self.flip%=2
    def update(self,delta):
        self.score += self.addscore
        self.time += delta
        self.timepic += delta
        self.ninja.update(delta)
        self.gensheild.update(delta)
        if(self.gensheild.y<0): #generate sheild
            self.gensheild.random_location(0,15)

        self.sheild.update(delta)
        if(self.live == 2): #set postion of sheild
            if(self.flip==1):
                self.sheild.position(self.ninja.x+15,self.ninja.y)
            else: 
                self.sheild.position(self.ninja.x-15,self.ninja.y)
        
        j = 0
        timeset = [0.1,0.4,0.7,1,1.3]
        for i in self.item1:
            i.update(delta)
        for i in self.item1: 
            if(i.y<0 and (self.time%2 >=timeset[j] and self.time%2<=timeset[j+1]-0.2)): #random items drop
                i.random_location(0,1)
            j+=1
            if(self.ninja.onhit(i,50,70)==True): #check hit and die
                self.live-=1
                if(self.live == 1):
                    self.sheild.cancel()
                    i.cancel()
                elif(self.live == 0):
                    if(self.flip == 0):
                        self.ninja.angle = 90
                    else:
                        self.ninja.angle = -90
                    self.ninja.Die()
                    self.addscore =0
                break 

        if(self.score>=self.limitscore): #change level
            for i in self.item1:
                i.setspeed(self.speeditem1,self.speeditem2)
            self.gensheild.setspeed(self.speeditem1,self.speeditem2)
            self.speeditem1+=2
            self.speeditem2+=2
            self.limitscore+=2500
            self.ninja.speed+=2
        
        if(self.timepic>=World.TIMECHANGE): #change pic of character
            self.ninja.pic+=1
            self.ninja.pic%=6   
            self.timepic = 0   
        
        if(self.ninja.onhit(self.gensheild,50,70)==True): #check hit sheild
            self.gensheild.cancel()
            if(self.live<=1):
                self.live+=1