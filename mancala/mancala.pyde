import copy
import math
add_library("sound")

COMPUTER = 1
HUMAN = -1

class MancalaBoard:
    next = {'A':'B','B':'C','C':'D','D':'E','E':'F','F':1,
                1:'L','L':'K','K':'J','J':'I','I':'H','H':'G','G':2,2:'A'}
    oppose = {'A':'G','B':'H','C':'I','D':'J','E':'K','F':'L',
                    'G':'A','H':'B','I':'C','J':'D','K':'E','L':'F'}                
    
    player1 = ['A','B','C','D','E','F']
    invplayer1 = ['F','E','D','C','B','A']
    player2 = ['L','K','J','I','H','G']
    invplayer2 = ['G','H','I','J','K','L']

    def __init__(self):
        self.value = {'A':4,'B':4,'C':4,'D':4,'E':4,'F':4,
                    'G':4,'H':4,'I':4,'J':4,'K':4,'L':4,1:0,2:0}  
        self.move = 0
    
    def possibleMoves(self,player):
        moves = []
        if player == 1:
            for fosse in MancalaBoard.player1:
                if self.value[fosse] != 0:
                    moves.append(fosse)
        elif player == 2:
            for fosse in MancalaBoard.player2:
                if self.value[fosse] != 0:
                    moves.append(fosse)
        return moves

    def doMove(self,player,fosse):
        isRightmost = 0
        if self.value[fosse] == 0:
            return None,None
        global isFinishedRender
        isFinishedRender = False
        
        if player == 1:
            for pit in MancalaBoard.invplayer1:
                if self.value[pit] == 0:
                    continue
                else:
                    if pit == fosse:
                        isRightmost = 1
        current = fosse
        again = False
        graines = self.value[fosse]
        self.value[fosse] = 0
        for value in range(graines):
            current = MancalaBoard.next[current]
            self.value[current]+=1
        if current == player:
            again = True
        else:
            if player == 1:
                if current in MancalaBoard.player1:
                    if self.value[current] == 1:
                        self.value[player]+=(self.value[current] + self.value[self.oppose[current]])
                        self.value[current] = 0
                        self.value[self.oppose[current]] = 0
            if player == 2:
                if current in MancalaBoard.player2:
                    if self.value[current] == 1:
                        self.value[player]+=(self.value[current] + self.value[self.oppose[current]])
                        self.value[current] = 0
                        self.value[self.oppose[current]] = 0
            self.move+=1
        return again,isRightmost

class Game:
    def __init__(self):
        self.state = MancalaBoard()
    
    def setSide(self,side):
        if side == 1:
            self.state.move = 1
            self.playerSide = {HUMAN:1,COMPUTER:2}
        elif side == 2:
            self.state.move = 0
            self.playerSide = {HUMAN:2,COMPUTER:1}
    
    def gameOver(self):
        p1=0
        p2=0
        #player1 has 0 left
        for fosse in self.state.player1:
            if self.state.value[fosse] == 0:
                p1+=1
        if p1 == 6:
            for fosse in self.state.player2:
                self.state.value[2]+=self.state.value[fosse]
                self.state.value[fosse]=0
            return True
        
        #player2 has 0 left
        for fosse in self.state.player2:
            if self.state.value[fosse] == 0:
                p2+=1
        if p2 == 6:
            for fosse in self.state.player1:
                self.state.value[1]+=self.state.value[fosse]
                self.state.value[fosse]=0
            return True
        
        return False
    
    def H1(self):
        #leftmost pit value
        if self.playerSide[COMPUTER] == 1:
            for pit in MancalaBoard.player1:
                if self.state.value[pit] !=0:
                    return self.state.value[pit]
        elif self.playerSide[COMPUTER] == 2:
            for pit in MancalaBoard.player2:
                if self.state.value[pit] !=0:
                    return self.state.value[pit]
        return 0
    
    def H2(self):
        #sum of all the stones in the player side
        sum = 0
        if self.playerSide[COMPUTER] == 1:
            for pit in MancalaBoard.player1:
                sum+=self.state.value[pit]
        elif self.playerSide[COMPUTER] == 2:
            for pit in MancalaBoard.player2:
                sum+=self.state.value[pit]
        return sum
    
    def H3(self):
        #number of non empty pits
        sum = 0
        if self.playerSide[COMPUTER] == 1:
            for pit in MancalaBoard.player1:
                if self.state.value[pit] !=0:
                    sum+=1
        elif self.playerSide[COMPUTER] == 2:
            for pit in MancalaBoard.player2:
                if self.state.value[pit] !=0:
                    sum+=1
        return sum
    
    def evaluateH(self,H4,H5,H6,H7):
        W1 = 0.225 
        W2 = 0.122 
        W3 = 0.654 
        W4 = 1 
        W5 = 0.484 
        W6 = 0.694 
        W7 = 0.918 
        W8 = 0.667 
        W9 = 0.194 
        W10 = 0.297
        H1 = self.H1()
        H2 = self.H2()
        H3 = self.H3()
        H8 = self.state.value[self.playerSide[COMPUTER]] + self.state.value[self.playerSide[HUMAN]]
        H9 = 0
        H10 = 0
        if self.state.value[self.playerSide[HUMAN]]>=5:
            H9 = - self.state.value[self.playerSide[HUMAN]]*1.5 - self.state.value[self.playerSide[COMPUTER]]
        if self.state.value[self.playerSide[COMPUTER]]>=5:
            H10 = self.state.value[self.playerSide[COMPUTER]]*1.5 - self.state.value[self.playerSide[HUMAN]]
            
        return H1*W1 + H2*W2 + H3*W3 + H4*W4 + H5*W5 + H6*W6 + H7*W7 + H8*W8 + H9*W9 + H10*W10
    
    def evaluate(self):
        return self.state.value[self.playerSide[COMPUTER]] - self.state.value[self.playerSide[HUMAN]]

    def findWinner(self):
        if self.state.value[self.playerSide[COMPUTER]] > self.state.value[self.playerSide[HUMAN]]:
            return self.playerSide[COMPUTER] , self.state.value[self.playerSide[COMPUTER]]
        if self.state.value[self.playerSide[HUMAN]] > self.state.value[self.playerSide[COMPUTER]]:
            return self.playerSide[HUMAN] , self.state.value[self.playerSide[HUMAN]]



def NegaMaxAlphaBetaPruning1(game, player, depth, alph, beta):
    if game.gameOver() or depth == 1:
        bestValue = game.evaluate()
        bestPit = None
        if player == HUMAN:
            bestValue = - bestValue
        return bestValue, bestPit
    bestValue = float('-inf')
    bestPit = None
    for pit in game.state.possibleMoves(game.playerSide[player]):
        child_game = copy.deepcopy(game)
        again, right = child_game.state.doMove(game.playerSide[player], pit)
        
        if again:
            value, _ = NegaMaxAlphaBetaPruning1 (child_game, player, depth-1, alph, beta)
        else:
            value, _ = NegaMaxAlphaBetaPruning1 (child_game, -player, depth-1, -beta, -alph)
        
        value = - value
        if value > bestValue:
            bestValue = value
            bestPit =pit
        if bestValue > alph:
            alph = bestValue
        if beta <= alph:
            break
    return bestValue, bestPit
    

def NegaMaxAlphaBetaPruning(game, player, depth, alph, beta, again, right, storeC, storeH):
    if game.gameOver() or depth == 1:
        H4 = game.state.value[game.playerSide[COMPUTER]] - storeC
        H6 = game.state.value[game.playerSide[HUMAN]] - storeH
        H7 = 1 if again else 0
        H5 = right
        bestValue = game.evaluateH(H4,H5,H6,H7)
        bestPit = None
        if player == HUMAN:
            bestValue = - bestValue
        return bestValue, bestPit
    bestValue = float('-inf')
    bestPit = None
    for pit in game.state.possibleMoves(game.playerSide[player]):
        child_game = copy.deepcopy(game)
        again, right = child_game.state.doMove(game.playerSide[player], pit)
        
        if again:
            value, _ = NegaMaxAlphaBetaPruning (child_game, player, depth-1, alph, beta, again, right, storeC, storeH)
        else:
            value, _ = NegaMaxAlphaBetaPruning (child_game, -player, depth-1, -beta, -alph, again, right, storeC, storeH)
        
        value = - value
        if value > bestValue:
            bestValue = value
            bestPit =pit
        if bestValue > alph:
            alph = bestValue
        if beta <= alph:
            break
    return bestValue, bestPit


        
pits = {} 

game = Game()
currentPlayer = 0
selected = 'None'

class pit:
    def __init__(self,index,posx,posy):
        self.posx = posx
        self.posy = posy
        self.index = index
        self.value = game.state.value[self.index]        
        self.r = 170/2
    
    def appear(self,col1,col2):
        if self.value > game.state.value[self.index]:
            self.value-=1
        elif self.value < game.state.value[self.index]:
            self.value+=1
        fill(col1)
        circle(self.posx,self.posy,self.r*2)
        textSize(20)
        fill(col2)
        text(self.index+' : '+str(self.value), self.posx-20, self.posy+60)
        if self.value != game.state.value[self.index]:
            return True
        else:
            return False
        
    def click(self):
        if ((mouseX-self.posx)**2 + (mouseY-self.posy)**2) <= self.r**2:
            return True
        else:
            return False

def setup():
    size(1920,1200)
    frameRate(4)
    global HUMAN
    global COMPUTER
    global pits
    global game
    global currentPlayer
    global img
    global wood
    global board
    img = loadImage("bg.jpg")
    wood = loadImage("wood2.jpg")
    board = loadImage("wood1.jpg")
    game.setSide(1)
    bg = SoundFile(this,"bg.mp3")
    bg.loop()
    cpt = 0
    for posx in range(300,width-300,250):
        pits[MancalaBoard.player1[cpt]] = pit(MancalaBoard.player1[cpt],posx,height/2+200)
        cpt+=1
        
    cpt = 0
    for posx in range(width-300,300,-250):
        pits[MancalaBoard.player2[cpt]] = pit(MancalaBoard.player2[cpt],posx,height/2-200)
        cpt+=1

def render(turn):
    global pits
    global isFinishedRender
    cpt=0
    
    fill(0)
    rect(width/2-800, height/2-440, 100, 70)
    fill(255)
    textSize(20)
    text("Home", width/2-780, height/2-400)
    
    if turn == 1:
        col1 = color(201, 166, 135)
        col2 = 255
    elif turn == 2:
        col2 = color(201, 166, 135)
        col1 = 255
    
    fill(col1)
    ellipse(width-130, height/2, 100, 400)
    textSize(20)     
    fill(col2)
    text('1'+' : '+str(game.state.value[1]), width-130-20, 600)
    
    fill(col2)
    ellipse(170,height/2, 100, 400)
    textSize(20)     
    fill(col1)
    text('2'+' : '+str(game.state.value[2]), 170-20, 600)
    
    for pit in MancalaBoard.player1:
        notFinished = pits[pit].appear(col1,col2)
        if notFinished:
            cpt+=1
    for pit in MancalaBoard.player2:
        notFinished = pits[pit].appear(col2,col1)
        if notFinished:
            cpt+=1
    if cpt == 0:
        isFinishedRender = True
    else:
        isFinishedRender = False
        

etat = 0
p = 1

def mainScreen():
    global p
    image(img, 0, 0,width, height)
    fill(120)
    if p == -1:
        fill(0)
    rect(width/2+70, height/2-300, 100, 70)
    fill(255)
    textSize(18)
    text("Player2", width/2+90, height/2-260)
    fill(120)
    if p == 1:
        fill(0)
    rect(width/2-200, height/2-300, 100, 70)
    fill(255)
    textSize(18)
    text("Player1", width/2-180, height/2-260)
    fill(255)
    textSize(40)
    text("Select side:", width/2-200, height/2-320)
    fill(255,0,255)
    image(wood,width/2-250, height/2-50, 500, 100)
    fill(255)
    textSize(25)
    text("Play", width/2-40, height/2+10)
    image(wood,width/2-250, height/2+80, 500, 100)
    fill(255)
    textSize(25)
    text("Computer VS Computer", width/2-140, (height/2)+135)

def draw():
    global isFinishedRender
    global game
    global currentPlayer
    global selected
    global etat
    
    if etat == 0:
        mainScreen()
    else:
        if game.state.move%2==0:
            currentPlayer=COMPUTER
        else:
            currentPlayer=HUMAN
            
        if not isFinishedRender:
            background(201, 166, 135)
            fill(255)
            textSize(60)
            text('Player '+str(game.playerSide[currentPlayer])+' turn', width/2-200, height/2-320)
            image(board,110,(height/2)-300,width-140,600)
            render(game.playerSide[currentPlayer])
        else:
            if etat == 1:
                #HvsC
                if not game.gameOver():
                    if currentPlayer == COMPUTER:
                        if game.state.move == 0:
                            done,_ = game.state.doMove(game.playerSide[currentPlayer], 'C')
                            done,_ = game.state.doMove(game.playerSide[currentPlayer], 'F')
                            print(game.state.value)
                        else:
                            storeC = game.state.value[game.playerSide[COMPUTER]]
                            storeH = game.state.value[game.playerSide[HUMAN]]    
                            _, bp = NegaMaxAlphaBetaPruning (game, COMPUTER, 8,float('-inf'),float('inf'),False,0,storeC,storeH)
                            print(bp)
                            done,_ = game.state.doMove(game.playerSide[currentPlayer], bp)
                            print(game.state.value)
                else:
                    render(game.playerSide[currentPlayer])
                    fill(255)
                    textSize(60)
                    winner,_ = game.findWinner()
                    text('Player '+str(winner)+' wins!!!!!!', width/2-200, height/2)
            elif etat == 2:
                #CvsC
                if not game.gameOver():
                    if currentPlayer == COMPUTER:
                            storeC = game.state.value[game.playerSide[COMPUTER]]
                            storeH = game.state.value[game.playerSide[HUMAN]]
                            _, bp = NegaMaxAlphaBetaPruning (game, COMPUTER, 8,float('-inf'),float('inf'),False,0,storeC,storeH)
                            print(bp)
                            done,_ = game.state.doMove(game.playerSide[currentPlayer], bp)
                            print(game.state.value)
                    if currentPlayer == HUMAN:
                            _, bp = NegaMaxAlphaBetaPruning1(game, HUMAN, 8,float('-inf'),float('inf'))
                            print(bp)
                            done,_ = game.state.doMove(game.playerSide[currentPlayer], bp)
                            print(game.state.value)
                else:
                    render(game.playerSide[currentPlayer])
                    fill(255)
                    textSize(60)
                    winner,_ = game.findWinner()
                    text('Player '+str(winner)+' wins!!!!!!', width/2-200, height/2)
                    

side = 1
def mouseClicked():
    global game
    global currentPlayer
    global selected
    global next
    global etat
    global p
    global side
    global isFinishedRender
    
    if etat == 0:
        if(mouseY>=(height/2-300) and mouseY<=(height/2-230)):
            if (mouseX>= (width/2+70) and mouseX<= (width/2+170)):
                side = 2
                p = -1
            if (mouseX>= (width/2-200) and mouseX<= (width/2-100)):
                side = 1
                p = 1
        if(mouseX>= (width/2-250) and mouseX<= (width/2+250)):
            if (mouseY>=(height/2-50) and mouseY<=(height/2+50)):
                isFinishedRender = False
                game.state = MancalaBoard()
                game.setSide(side)
                etat = 1
            elif (mouseY>=(height/2+80) and mouseY<=(height/2+180)):
                isFinishedRender = False
                game.state = MancalaBoard()
                game.setSide(side)
                etat = 2
    else:
        if currentPlayer == HUMAN and not game.gameOver():
            if game.playerSide[currentPlayer] == 1:
                for pit in MancalaBoard.player1:
                    if(pits[pit].click()):
                        done,_ = game.state.doMove(game.playerSide[currentPlayer], pit)
            else:
                for pit in MancalaBoard.player2:
                    if(pits[pit].click()):
                        done,_ = game.state.doMove(game.playerSide[currentPlayer], pit)
                        
        if(mouseY>=(height/2-440) and mouseY<=(height/2-370)):
            if (mouseX>= (width/2-800) and mouseX<= (width/2-700)):
                etat = 0
