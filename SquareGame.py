import time
import random
import tkinter
from tkinter import *


#classes
class enemy:
    def __init__(self,x=0,y=0,size=50,color="black"):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.object = canvas.create_rectangle(self.x,self.y,self.x+self.size,self.y+self.size,fill=self.color)
    def randMove(self,radiusX=5,radiusY=5):
        radiusX = random.randint(-radiusX,radiusX)
        radiusY = random.randint(-radiusY,radiusY)
        self.x = self.x + radiusX
        self.y = self.y + radiusY
        canvas.move(self.object,radiusX,radiusY)
    def track(self,obj,speed=1):
        addX = speed
        addY = speed
        if coords(obj)[0] < coords(self.object)[0]:
            addX = -speed
        if coords(obj)[1] < coords(self.object)[1]:
            addY = -speed
        self.x = self.x + addX
        self.y = self.y + addY
        canvas.move(self.object,addX,addY)
    def escape(self,obj,speed=1):
        addX = speed
        addY = speed
        if coords(obj)[0] > coords(self.object)[0]:
            addX = -speed
        if coords(obj)[1] > coords(self.object)[1]:
            addY = -speed
        self.x = self.x + addX
        self.y = self.y + addY
        canvas.move(self.object,addX,addY)


#functions
def keyAssign(key,command):
    canvas.bind_all("<KeyPress-"+str(key)+">",command)
def move(item,amount=10):
    def up(event):
        canvas.move(item,0,-amount)
    def down(event):
        canvas.move(item,0,amount)
    def left(event):
        canvas.move(item,-amount,0)
    def right(event):
        canvas.move(item,amount,0)
    move.up = up
    move.down = down
    move.left = left
    move.right = right
def visuals(item,color="white"):
    def hide(event):
        canvas.itemconfig(item,state=HIDDEN)
    def show(event):
        canvas.itemconfig(item,state=NORMAL)
    def color(event):
        canvas.itemconfig(item,fill=color)
    visuals.hide = hide
    visuals.show = show
    visuals.color = color 
def assign(item):
    move(item)
    visuals(item)
def wasdMove(thing,reverse=False):
    assign(thing)
    keyAssign("w",move.up)
    keyAssign("s",move.down)
    keyAssign("a",move.left)
    keyAssign("d",move.right)
    keyAssign("W",move.up)
    keyAssign("S",move.down)
    keyAssign("A",move.left)
    keyAssign("D",move.right)
def arrowMove(thing):
    assign(thing)
    keyAssign("Up",move.up)
    keyAssign("Down",move.down)
    keyAssign("Left",move.left)
    keyAssign("Right",move.right)
def PASS(event=None):
    pass
def keyClear(exception=""):
    for n in "1234567890qwertyuiopasdfghjklzxcvbnm":
        if n not in exception:
            keyAssign(n,PASS)
def distance(coord1,coord2):
    return ( abs(coord1[0]-coord2[0])**2 + abs(coord1[1]-coord2[1])**2 )**(1/2)
def coords(item):
    return [(canvas.coords(item)[0]+canvas.coords(item)[2])/2,(canvas.coords(item)[1]+canvas.coords(item)[3])/2]    
def pause(event=None):
    global state
    if state=="playing":
        state="paused"
        canvas.itemconfig(text,text="PAUSED",state=NORMAL)
    else:
        state="playing"
        canvas.itemconfig(text,state=HIDDEN)
        wasdMove(player)
def restart(event=None):
    global state
    state = "restart"
def exitProgram(event=None):
    global done
    done = True
def sequence(message=[],wait=1,style=('Times', '72', 'bold')):
    for n in message:
     canvas.itemconfig(text,text=n,font=style)
     window.update()
     time.sleep(2)
#window initiation
window = Tk()
window.title("The Square Game")


#widget initiation
canvas = Canvas(window,width=500,height=500)
stats = Label(window,text="Made by Alexander Ng")
pauseButton = Button(window,text="Pause (P)",command=pause)
exitButton = Button(window,text="Exit (O)",command=exitProgram)
restartButton = Button(window,text="RESTART (R)",command=restart)
#widget geometry
canvas.grid(row=0,column=0)
stats.grid(row=1,column=0)
pauseButton.grid(row=2,column=0,sticky=W,padx=50)
restartButton.grid(row=2,column=0,sticky=N)
exitButton.grid(row=2,column=0,sticky=E,padx=50)



#variable initiation
state = "playing"
won = False
lost = False
done = False
level = 1
timeleft = 60
timeup = 0
lives = 10
enemyNum = (level*5)+10
player = canvas.create_rectangle(185,235,215,265,fill="white")
enemies = [enemy(random.randint(0,400),random.randint(0,500),25,random.choice(["red","blue","yellow"])) for n in range(enemyNum)]
text = canvas.create_text(250, 250, text="", font=('Times', '72', 'bold'))
reds,blues,greens,yellows = 0,0,0,0
keyAssign("p",pause)
keyAssign("o",exitProgram)
keyAssign("r",restart)
wasdMove(player)

#intro sequence
sequence(["Welcome to","         The\nSquare Game!","     made by\nAlexander Ng"],2,('Times', '72', 'bold'))
     
#start game
canvas.itemconfig(text,state=HIDDEN,text="PAUSED", font=('Times', '72', 'bold'))
while not done:
    if state=="playing":
        if timeleft <= 0:
            lost = True
        #time/variable update
        length = len(str(round(timeleft))) + 3
        timeleft = timeleft - 0.01
        time.sleep(0.0001)
        if timeleft > 50:
            message = "Level:"+str(level)+" Time: "+str(timeleft)[:length]+"     Total:"+str(enemyNum)+" - Reds:"+str(reds)+" Yellows:"+str(yellows)+" Greens:"+str(greens)+" Blues:"+str(blues)+"\nYou must get rid of all Blue and Yellow squares before time runs out\nTouch a square to change it's color, but don't touch red\n Red->Blue        Blue->Yellow->Green"
        else:
            message = "Level:"+str(level)+" Time: "+str(timeleft)[:length]+"     Total:"+str(enemyNum)+" - Reds:"+str(reds)+" Yellows:"+str(yellows)+" Greens:"+str(greens)+" Blues:"+str(blues)+"\nRed->Blue        Blue->Yellow->Green"
        stats.config(text=message)
        reds,blues,greens,yellows = 0,0,0,0
        won = True
        #player boundary wrap
        if coords(player)[0] < 1-15:
            canvas.coords(player,[400-15,coords(player)[1]-15,400+15,coords(player)[1]+15])
        elif coords(player)[0] > 399+15:
            canvas.coords(player,[0-15,coords(player)[1]-15,0+15,coords(player)[1]+15])
        elif coords(player)[1] < 1-15:
            canvas.coords(player,[coords(player)[1]-15,500-15,coords(player)[1]+15,500+15])
        elif coords(player)[1] > 499+15:
            canvas.coords(player,[coords(player)[0]-15,0-15,coords(player)[0]+15,0+15])
        #going through enemies
        for i in range(len(enemies)):
            e = enemies[i]
            #boundary wrap
            if coords(e.object)[0] < 1-e.size/2:
                canvas.coords(e.object,[400-e.size/2,coords(e.object)[1]-e.size/2,400+e.size/2,coords(e.object)[1]+e.size/2])
            elif coords(e.object)[0] > 399+e.size/2:
                canvas.coords(e.object,[0-e.size/2,coords(e.object)[1]-e.size/2,0+e.size/2,coords(e.object)[1]+e.size/2])
            elif coords(e.object)[1] < 1-e.size/2:
                canvas.coords(e.object,[coords(e.object)[1]-e.size/2,500-e.size/2,coords(e.object)[1]+e.size/2,500+e.size/2])
            elif coords(e.object)[1] > 499+e.size/2:
                canvas.coords(e.object,[coords(e.object)[0]-e.size/2,0-e.size/2,coords(e.object)[0]+e.size/2,0+e.size/2])
            #enemy collision
            for o in enemies:
                if o!=e and e.color!="blue":
                    if distance(coords(e.object),coords(o.object))<10:
                        if e.color == "red" and o.color != "yellow":
                            e.escape(o.object,2)
                        elif e.color == "yellow" and o.color == "blue":
                            e.escape(o.object)
                        elif e.color == o.color:
                            e.escape(o.object)
            #enemy actions
            if e.color == "green":
                greens = greens + 1
                if distance(coords(player),coords(e.object)) > 75:
                    e.track(player,1.5)
                else:
                    e.escape(player,1)
            elif e.color == "red":
                reds = reds + 1
                e.track(player,0.5)
                if distance(coords(player),coords(e.object)) < 3:
                    canvas.delete(e.object)
                    enemies.pop(i)
                    enemies.append(enemy(random.randint(0,400),random.randint(0,500),25,"blue"))
            elif e.color == "yellow":
                yellows = yellows + 1
                won = False
                if timeleft%4.<0.5:
                    e.escape(player,0.5)
                else:
                    e.randMove(2,2)
                if distance(coords(player),coords(e.object)) < 4:
                    e.color = "green"
                    canvas.itemconfig(e.object,fill="green")
            elif e.color == "blue":
                blues = blues + 1
                won = False
                if distance(coords(player),coords(e.object)) < 8:
                    canvas.delete(e.object)
                    enemies.pop(i)
                    enemies.append(enemy(random.randint(0,400),random.randint(0,500),25,"yellow"))
        if won:
            state = "up"
            canvas.itemconfig(text,state=NORMAL,text="YOU PASSED\n    LEVEL "+str(level))
            stats.config(text="You passed Level "+str(level)+" with:\n"+str(timeleft)[:length]+" seconds left, "+str(greens)+" Green Squares, and "+str(reds)+" Red squares\nOn to level "+str(level+1)+"!!!!!")
            if level <= 25:
                level = level + 1
            else:
                state = "done"
    elif state == "sandbox" and False: #never going to happen, UNFINISHED
        if lives <= 0:
            lost = True
        wasdMove(player)
        #time/variable update
        length = len(str(round(timeleft))) + 3
        timeup = timeup + 0.01
        time.sleep(0.0001)
        if timeleft < 10:
            message = "Lives:"+str(lives)+" Time: "+str(timeup)[:length]+"     Total:"+str(enemyNum)+" - Reds:"+str(reds)+" Yellows:"+str(yellows)+" Greens:"+str(greens)+" Blues:"+str(blues)+"\nYou must get as many greens as possible without dying\nTouch a square to change it's color, but don't touch red\n Red->Blue        Blue->Yellow->Green"
        else:
            message = "Lives:"+str(lives)+" Time: "+str(timeup)[:length]+"     Total:"+str(enemyNum)+" - Reds:"+str(reds)+" Yellows:"+str(yellows)+" Greens:"+str(greens)+" Blues:"+str(blues)+"\nRed->Blue        Blue->Yellow->Green"
        stats.config(text=message)
        reds,blues,greens,yellows = 0,0,0,0
        #player boundary wrap
        if coords(player)[0] < 1-15:
            canvas.coords(player,[400-15,coords(player)[1]-15,400+15,coords(player)[1]+15])
        elif coords(player)[0] > 399+15:
            canvas.coords(player,[0-15,coords(player)[1]-15,0+15,coords(player)[1]+15])
        elif coords(player)[1] < 1-15:
            canvas.coords(player,[coords(player)[1]-15,500-15,coords(player)[1]+15,500+15])
        elif coords(player)[1] > 499+15:
            canvas.coords(player,[coords(player)[0]-15,0-15,coords(player)[0]+15,0+15])
        #going through enemies
        for i in range(len(enemies)):
            e = enemies[i-1]
            #boundary wrap
            if coords(e.object)[0] < 1-e.size/2:
                canvas.coords(e.object,[400-e.size/2,coords(e.object)[1]-e.size/2,400+e.size/2,coords(e.object)[1]+e.size/2])
            elif coords(e.object)[0] > 399+e.size/2:
                canvas.coords(e.object,[0-e.size/2,coords(e.object)[1]-e.size/2,0+e.size/2,coords(e.object)[1]+e.size/2])
            elif coords(e.object)[1] < 1-e.size/2:
                canvas.coords(e.object,[coords(e.object)[1]-e.size/2,500-e.size/2,coords(e.object)[1]+e.size/2,500+e.size/2])
            elif coords(e.object)[1] > 499+e.size/2:
                canvas.coords(e.object,[coords(e.object)[0]-e.size/2,0-e.size/2,coords(e.object)[0]+e.size/2,0+e.size/2])
            #enemy collision
            for o in enemies:
                if o!=e and e.color!="blue":
                    if distance(coords(e.object),coords(o.object))<10:
                        if e.color == "red" and o.color != "yellow":
                            e.escape(o.object,2)
                        elif e.color == "yellow" and o.color == "blue":
                            e.escape(o.object)
                        elif e.color == o.color:
                            e.escape(o.object)
            #enemy actions
            if e.color == "green":
                greens = greens + 1
                if distance(coords(player),coords(e.object)) > 75:
                    e.track(player,1.5)
                else:
                    e.escape(player,1)
            elif e.color == "red":
                reds = reds + 1
                e.track(player,0.5)
                if distance(coords(player),coords(e.object)) < 3:
                    canvas.delete(e.object)
                    enemies.pop(i)
                    lives = lives - 1
            elif e.color == "yellow":
                yellows = yellows + 1
                e.randMove(2,2)
                if distance(coords(player),coords(e.object)) < 4:
                    e.color = "green"
                    canvas.itemconfig(e.object,fill="green")
            elif e.color == "blue":
                blues = blues + 1
                if distance(coords(player),coords(e.object)) < 8:
                    canvas.delete(e.object)
                    enemies.pop(i)
                    enemies.append(enemy(random.randint(0,400),random.randint(0,500),25,"yellow"))
    elif state == "paused":
        keyClear(['p','o',"r"])
        time.sleep(0.2)
    elif state == "up":
        time.sleep(5)
        canvas.delete(ALL)
        if level <= 4:
            enemyNum = (level*5)+10
            timeleft = 60
        else:
            enemyNum = 30
            timeleft = 60 - 2*level
        player = canvas.create_rectangle(185,235,215,265,fill="white")
        enemies = [enemy(random.randint(0,400),random.randint(0,500),25,random.choice(["red","blue","yellow"])) for n in range(enemyNum)]
        text = canvas.create_text(250, 250, text="", font=('Times', '72', 'bold'))
        sequence(["Starting in...","3...","2...","1...","Go!"],0.5)
        canvas.itemconfig(text,state=HIDDEN,text="PAUSED", font=('Times', '72', 'bold'))
        reds,blues,greens,yellows = 0,0,0,0
        keyAssign("p",pause)
        keyAssign("o",exitProgram)
        keyAssign("r",restart)
        wasdMove(player)
        state = "playing"
    elif state == "menu" and False:
        #UNFINISHED
        state = "playing"
    elif state == "restart":
        state = "up"
        level = 1
        canvas.itemconfig(text,state=NORMAL,text="RESTARTING")
        canvas.itemconfig(stats,text="Made by Alexander Ng")
    elif state == "done":
        canvas.delete(ALL)
        text = canvas.create_text(250, 250, text="", font=('Times', '72', 'bold'))
        sequence(["         You\nhave finished","         the\nlast level","Thanks for\n      playing...","         The\nSquare Game!","     made by\nAlexander Ng"],0.5)
        done = True
    if lost:
        done = True
    window.update()
if lost:
    stats.config(text="Time: "+str(abs(round(timeleft)))+"       Reds:"+str(reds)+" Yellows:"+str(yellows)+" Greens:"+str(greens)+" Blues:"+str(blues)+"\nGood Luck Next Time!!!!!")
    canvas.itemconfig(text,state=NORMAL,text="YOU LOST!")
if done and not lost:
    window.destroy()
