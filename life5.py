from Tkinter import * 
from itertools import * 

from random import randint
class Life(object):
    def __init__(self,nrows,ncols):
        self.nrows = nrows
        self.ncols = ncols
        self.board = []
        self.neighbors = []
        self.generation = 1
        for i in range(self.nrows):
            column=[]
            self.board.append([0]*self.ncols)
            self.neighbors.append([0]*self.ncols)

    def randomize(self):
        self.board = []
        for i in range(self.nrows):
            column=[]
            for j in range(self.ncols):
                rint=0
                if randint(0,8)>=8:  rint=1
                column.append(rint)
            self.board.append(column)


    def setPatternFromTuple(self,tuple):
        self.clear()
        for val in tuple:
            i = val%self.nrows
            j = val/self.nrows
            self.board[i][j] = 1

    def getTupleFromPattern(self):
        patternList = []
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.board[i][j]:
                    patternList.append(i+j*self.ncols)
        return tuple(patternList)

    def printBoardGraphics(self,canvas):
        for i in range(self.ncols):
            for j in range(self.nrows):
                if(self.board[j][i]) == 1:
                    canvas.create_rectangle(10*i+5,10*j+5,10*(i+1)+5,10*(j+1)+5,fill='red')
                else:
                    canvas.create_rectangle(10*i+5,10*j+5,10*(i+1)+5,10*(j+1)+5,fill='white')

    def printBoard(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                if(self.board[i][j]) == 1:
                    print("*"),
                else:
                    print("o"),
            print("")


    def clear(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.board[i][j]=0

    def clearNeighbors(self):
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.neighbors[i][j]=0

    def update(self):
        self.generation+=1
        self.clearNeighbors()

        for i in range(self.nrows):
            for j in range(self.ncols):
                if(self.board[i][j]):

                    iplus=(i+1)%self.nrows
                    iminus=(i-1)%self.nrows
                    jplus=(j+1)%self.ncols
                    jminus=(j-1)%self.ncols
                    self.neighbors[iminus][j     ]+=1
                    self.neighbors[iminus][jminus]+=1
                    self.neighbors[iminus][jplus ]+=1
                    self.neighbors[iplus ][j     ]+=1
                    self.neighbors[iplus ][jminus]+=1
                    self.neighbors[iplus ][jplus ]+=1
                    self.neighbors[i     ][jminus]+=1
                    self.neighbors[i     ][jplus ]+=1

        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.board[i][j]==0:
                    if self.neighbors[i][j]==3 : self.board[i][j]=1
                else:
                    if self.neighbors[i][j]!=2 and self.neighbors[i][j]!=3: self.board[i][j]=0

class Controller(object):
    def __init__(self):
        self.pause=1
        self.enumerate=0
        self.root = Tk()
        self.root.title("Game of Life")

        labelfont = ('times', 20, 'bold')
        self.label = Label(self.root,font=labelfont,text='Game of Life')

        self.label.pack()

        self.frame0=Frame(self.root)
        self.frame0.pack()
        self.randomButton = Button(self.frame0,text='random',width=10,command=self.random)
        self.randomButton.pack(side=LEFT)
        self.clearButton = Button(self.frame0,text='clear',width=10,command=self.clear)
        self.clearButton.pack(side=LEFT)
        self.pauseButton = Button(self.frame0, text='pause',width=10,command=self.playPauseGame)
        self.pauseButton.pack(side=LEFT)

        self.frame1=Frame(self.root)
        self.frame1.pack()
        self.rowLabel = Label(self.frame1,text="rows")
        self.rowLabel.pack(side=LEFT)
        self.rowsText = Spinbox(self.frame1,width=5,from_=1, to = 100,command=self.reshape)
        self.rowsText.pack(side=LEFT)
        self.colLabel = Label(self.frame1,text="cols")
        self.colLabel.pack(side=LEFT)
        self.colsText = Spinbox(self.frame1,width=5,from_=1, to = 100,command=self.reshape)
        self.colsText.pack(side=LEFT)

        self.rowsText.delete(0,"end")
        self.rowsText.insert(0,40)

        self.colsText.delete(0,"end")
        self.colsText.insert(0,40)

        self.frame2=Frame(self.root)
        self.frame2.pack()
        self.genTextLabel=Label(self.frame2,text="generation ")
        self.genLabel = Label(self.frame2,text="0")
        self.genTextLabel.pack(side=LEFT)
        self.genLabel.pack(side=LEFT)

        self.canvas = Canvas(self.root,width=500,height=500,background='white')
        self.canvas.bind("<Button-1>",lambda event:self.clickCell(event))
        self.canvas.bind("<B1-Motion>",lambda event:self.clickCell(event))
        self.canvas.pack(side=TOP)

        self.frame3=Frame(self.root)
        self.frame3.pack()
        


        self.enumerateButton = Button(self.frame3, text='Find Still Lives',command=self.findStillLife)
        self.enumerateButton.pack(side=LEFT)

        self.sizeLabel=Label(self.frame3, text = 'of size:')
        self.sizeLabel.pack(side=LEFT)

        self.stillSize = Spinbox(self.frame3,width=5,from_=1, to = 1000)
        self.stillSize.pack(side=LEFT)
        self.stillSize.delete(0,"end")
        self.stillSize.insert(0,20)

        self.cancelEnumerateButton = Button(self.frame3, text='Abandon Search',command=self.cancelSearch)
        self.cancelEnumerateButton.pack(side=LEFT)

        self.random()
        self.root.mainloop()

    def cancelSearch(self):
        self.enumerate=0

    def reshape(self):

        self.nrows = int(self.rowsText.get())
        self.ncols = int(self.colsText.get())

        self.canvas.config(width=11*self.ncols,height=11*self.nrows)

        self.pattern=Life(self.nrows,self.ncols)
        self.canvas.delete(ALL)
        self.pattern.printBoardGraphics(self.canvas)

        self.pattern.generation=1
        self.genLabel.config(text=str(self.pattern.generation))


    def clickCell(self,event):
        i = int((event.x-5)/10)
        j = int((event.y-5)/10)

        if -1<i<self.ncols  and -1<j<self.nrows:
            self.pattern.board[j][i]=1
            self.canvas.delete(ALL)
            self.pattern.printBoardGraphics(self.canvas)
            self.canvas.update()

    def pauseButtonConfigure(self):
        if self.pause ==0:
            self.pauseButton.config(text='pause')
        else:
            self.pauseButton.config(text='play')

    def clear(self):
        self.pause=1
        self.pauseButtonConfigure()

        self.reshape()

    def random(self):
        self.pause=1
        self.pauseButtonConfigure()

        self.nrows = int(self.rowsText.get())
        self.ncols = int(self.colsText.get())

        self.canvas.config(width=11*self.ncols,height=11*self.nrows)

        self.pattern=Life(self.nrows,self.ncols)
        self.pattern.randomize()
        self.canvas.delete(ALL)
        self.pattern.printBoardGraphics(self.canvas)

        self.pattern.generation=1
        self.genLabel.config(text=str(self.pattern.generation))

    def findStillLife(self):
        self.enumerate=1
        self.pause = 0
        self.pauseButton.config(text='pause')

        n = self.nrows*self.ncols
        i = int(self.stillSize.get())
        for j in combinations(range(n),i):
            if not self.enumerate: break
            self.pattern.setPatternFromTuple(j)

            self.canvas.delete(ALL)
            self.pattern.printBoardGraphics(self.canvas)
            self.canvas.update()

            self.pattern.update()
            k = self.pattern.getTupleFromPattern()
            if set(j) == set(k): 
                print('='*30)
                print j
                self.pattern.printBoard()
        self.enumerate=0
        self.pause = 1
        self.pauseButton.config(text='play')

    def playPauseGame(self):
        self.pause=1-self.pause
        self.pauseButtonConfigure()

        if not self.enumerate:
            self.pauseTime=50
            while not self.pause:
                self.pattern.update()
                self.canvas.update()
                self.canvas.after(self.pauseTime)
                self.genLabel.config(text=str(self.pattern.generation))
                self.canvas.delete(ALL)
                self.pattern.printBoardGraphics(self.canvas)
                self.canvas.update()

if __name__=="__main__": a = Controller()
