import pygame
import time
import random
pygame.init()
display_width=600
display_height=600
boardpx=60 #x coordinate of the snakes moving area with walls and food
boardpy=20
squared=16
gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Snake")
clock=pygame.time.Clock()
black=(0,0,0)
white=(255,255,255)
yellow=(253,253,15)
green=(16,182,46)
darkBlue=(16,16,242)
lightBlue=(16,242,242)
red=(255,0,0)

output=open("HumanResult.txt", "a+")
output.write("(")
noOfTicks=0

####################################################################################
######################################################################################
###################################################################################3
class Board: #board does not have any objects, but it was eaisier for me to group functions this way
    boardw=30
    boardh=30
    array=['.']*boardh #Board.array is a matrix which contains letters: "S" for a snake object, "F" for food and "W" for walls
    numberOfWalls=0 #you can choose number of walls in this game
    Score=0 #easier for me putitng this as a static variable than writing global Score all the time
###############################3
    def init(): #creates a board with 2 snake objects in their starting position with walls(3 in this case) and food
        boardw=Board.boardw
        boardh=Board.boardh
        array=Board.array
        for i in range(boardh):
            array[i]=["."]*boardw
        Snake.initCreate()
        Board.SnakeAdd()
        Board.wallCreate()
        Board.fwGenerator("F")
####################################3
    def SnakeAdd(): #Snake.array contains snake objects, which have their coordinates. I am using this fact to fill up the Board.array with "S"
        array=Board.array
        indicator=Snake.array
        for i in range(len(indicator)):
            array[indicator[i].starty][indicator[i].startx]="S"
#####################################
    def SnakeErase(): #Erases all the "S";convinient to use for updating the board after snake's movement
        array=Board.array
        boardh=Board.boardh
        boardw=Board.boardw
        for i in range(boardh):
            for j in range(boardw):
                if array[i][j]=="S":
                    array[i][j]="."
######################################3
    def update(): #upadates the board only with snake objects
        Board.SnakeErase()
        Board.SnakeAdd()
##########################################
    def notCrash(x,y): #checkes if  the snake does not crash into a wall or an edge
        boardw=Board.boardw
        boardh=Board.boardh
        array=Board.array
        indicator=Snake.array
        if x>=0 and x<=boardw-1 and y>=0 and y<=boardh-1 and array[y][x] in [".","F"]:
            return True
        else:
            if indicator[0].startx==x and indicator[0].starty==y:
                return True
            else:
                return False
##############################################
    def isFree(x,y): #checkes if the snake's tail can be added on the board
        array=Board.array
        if Board.notCrash(x,y) and array[y][x]!="F":
            return True
        else:
            return False
####################################################################
    def fwGenerator(letter): #randomly generates food or walls
        array=Board.array
        boardw=Board.boardw
        boardh=Board.boardh
        foodPlace=[]
        for i in range(boardh):
            for j in range(boardw):
                if array[i][j]==".":
                    index=i*boardw + j
                    foodPlace.append(index)
        foodNumber=random.choice(foodPlace)
        y=foodNumber//boardw
        x=foodNumber- y*boardw            
        array[y][x]=letter


####################################################################
    def wallCreate(): #creates walls based on the number of walls
        numberOfWalls=Board.numberOfWalls
        for i in range(numberOfWalls):
            Board.fwGenerator("W")
    
#####################################################################
#################################################################
class Snake:
    startx=5
    starty=5
    array=[]
##############################################################
    def setValues(self,x,y):
        self.startx=x
        self.starty=y
#############################################################3
    def move(changex,changey): #moves the snake around the board
        indicator=Snake.array
        board=Board.array
        head=indicator[0]
        directionBug=not(indicator[1].startx==(head.startx+changex) and (indicator[1].starty==head.starty+changey))#if the snakes tries to move to the position of its second object
        if Board.notCrash(head.startx+changex,head.starty+changey):
            foodCollect=board[head.starty+changey][head.startx+changex]=="F"
            if foodCollect:
                Snake.grow()
                Board.Score+=1
                Board.update()
                Board.fwGenerator("F")
            if changex!=0 or changey!=0:
                parameter=len(indicator)-1
                while(parameter>0):
                    now=indicator[parameter]
                    previous=indicator[parameter-1]
                    now.setValues(previous.startx,previous.starty)
                    parameter-=1
                head.setValues(head.startx+changex,head.starty+changey)
            Board.update()
        else:
            if directionBug:
                gameOver()
#############################################################################
    def create(self,x,y):
        self.setValues(x,y)
        Snake.array.append(self)
###############################################################################
    def initCreate(): #I chose to have 2 snake objects at the beginning of the game
        startx=Snake.startx
        starty=Snake.starty
        Snake().create(startx,starty)
        Snake().create(startx-1,starty)
###############################################################################
    def grow(): #shows how the snake grows
        array=Snake.array
        placeGrow=array[len(array)-1]
        placeBond=array[len(array)-2]
        x=placeGrow.startx
        y=placeGrow.starty
        isFree=Board.isFree
        if y==placeBond.starty:
            if isFree(x-1,y):
                Snake().create(x-1,y)
                Board.update()
            elif isFree(x+1,y):
                Snake().create(x+1,y)
                Board.update()
            elif isFree(x,y-1):
                Snake().create(x,y-1)
                Board.update()
            elif isFree(x,y+1):
                Snake().create(x,y+1)
                Board.update()
            else:
                gameOver()
        else:
             if isFree(x,y-1):
                Snake().create(x,y-1)
                Board.update()
             elif isFree(x,y+1):
                Snake().create(x,y+1)
                Board.update()
             elif isFree(x-1,y):
                Snake().create(x-1,y)
                Board.update()
             elif isFree(x+1,y):
                Snake().create(x+1,y)
                Board.update()
             else:
                gameOver()
####################################################################
    def reset(): #needed when DEBUGING and do not want to pile objects when using the first option in gameOver()
        array=Snake.array
        del array[0:len(array)]
################################################################################
#########################################################################
#########################################################################
def displayBoard(): #draws the Board.array on the game display
    boardw=Board.boardw
    boardh=Board.boardh
    array=Board.array
    indicator=Snake.array
    for i in range(boardh):
        for j in range(boardw):
            x=boardpx+j*squared
            y=boardpy+i*squared
            r=squared//2
            pygame.draw.rect(gameDisplay, green, (x,y,squared,squared))
            if array[i][j]=="W":
                pygame.draw.rect(gameDisplay, black, (x,y,squared,squared))
            elif array[i][j]=="S":
                if indicator[0].startx==j and indicator[0].starty==i:
                    pygame.draw.circle(gameDisplay, darkBlue, (x+r,y+r), r)
                else:
                    pygame.draw.circle(gameDisplay, lightBlue, (x+r,y+r), r)
            else:
                pygame.draw.rect(gameDisplay, green, (x,y,squared,squared))
                if array[i][j]=="F":
                    pygame.draw.circle(gameDisplay, yellow, (x+r,y+r), r)
########################################################################
def gameOver(): #we have 2 options to choose:either reset the game or quit it
    global noOfTicks
    output.write(str(noOfTicks)+","+str(len(Snake.array))+")(")
    noOfTicks=0
    Snake.reset()
    gameDisplay.fill(black)
    messageDisplay("Again?",85,red)
    gameLoop()
    #gameDisplay.fill(black)
    #messageDisplay("Game over",85,red)
    #pygame.quit()
    #quit() #Alternative code if you want to exit the game after the first crash
##############################################################################
def needDisplay(x,y,string,value,color,fontSize): #used to show the Score and our names
    font=pygame.font.SysFont("none",fontSize)
    text=font.render(string+" "+value,True,color)
    gameDisplay.blit(text,(x,y))    
###############################################################################
def textObjects(text,font,color):
    TextSurface=font.render(text,True,color)
    return TextSurface,TextSurface.get_rect()
################################################################################
def messageDisplay(text,fontSize,color): #used to have a nice centered message after the crash
    largeText=pygame.font.Font("freesansbold.ttf",fontSize)
    TextSurf,TextRect=textObjects(text,largeText,color)
    TextRect.center=(display_width//2,display_height//2)
    gameDisplay.blit(TextSurf,TextRect)
    pygame.display.update()
    time.sleep(2)
#################################################################################
def gameLoop():
    global noOfTicks
    noOfTicks=0
    Board.Score=0
    Board.init()
    changex=0
    changey=0
    xp=0
    yp=0
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    changey=0
                    changex=-1
                elif event.key==pygame.K_RIGHT:
                    changey=0
                    changex=1
                elif event.key==pygame.K_UP:
                    changex=0
                    changey=-1
                elif event.key==pygame.K_DOWN:
                    changex=0
                    changey=1
        if xp==0 and yp==0 and changex==-1: #used to DEBUG the snake;e.g. whenever the snake was moving left,if you clicked right key afterwards, the snake would have stopped
            changex=0#
        elif xp*changex==-1: #        
            changex=xp        #    
        elif yp*changey==-1:   #    
            changey=yp          #     
        xp=changex               #   
        yp=changey                # 
        Snake.move(changex,changey)
        gameDisplay.fill(black)
        displayBoard()
        needDisplay(1,0,"Score:",str(Board.Score),white,25)
        needDisplay(1,boardpy+Board.boardh*squared+5,"GALIC Lazar, 56158707","",white,25)
        needDisplay(1,boardpy+Board.boardh*squared+30,"JELACA Aleksa 56158793","",white,25)
        pygame.display.update()
        clock.tick(10)
        noOfTicks+=1
            
##############################################################################################
gameLoop()

output.write("END)\r\n")
output.close()
#########################################################################################
# Change some values if they do not suit you. If you have any questions, ask. Good luck with your part!



                    
