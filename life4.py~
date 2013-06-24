from Tkinter import * 
from random import randint
class Life(object):
    def __init__(self,nrows,ncols):
        self.nrows = nrows
        self.ncols = ncols
        self.board = []
        self.neighbors = []
        self.generation = 1
        for i in range(nrows):
            column=[]
            for j in range(ncols):
                rint=0
                if randint(0,8)>=8:  rint=1
                column.append(rint)
            self.board.append(column)
            self.neighbors.append([0]*ncols)


    def printBoardGraphics(self,canvas):
        for i in range(self.nrows):
            for j in range(self.ncols):
                if(self.board[i][j]) == 1:
                    canvas.create_rectangle(10*i+5,10*j+5,10*(i+1)+5,10*(j+1)+5,fill='red')
                else:
                    canvas.create_rectangle(10*i+5,10*j+5,10*(i+1)+5,10*(j+1)+5,fill='white')

    def update(self):
        self.generation+=1
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.neighbors[i][j]=0
            

        for i in range(self.nrows):
            for j in range(self.ncols):
                if(self.board[i][j]):
                    if i>0:
                        self.neighbors[i-1][j]+=1
                        if j>0: self.neighbors[i-1][j-1]+=1
                        if j<self.ncols-1: self.neighbors[i-1][j+1]+=1
                        
                    if i<self.nrows-1:
                        self.neighbors[i+1][j]+=1
                        if j>0: self.neighbors[i+1][j-1]+=1
                        if j<self.ncols-1: self.neighbors[i+1][j+1]+=1

                    if j>0:self.neighbors[i][j-1]+=1
                    if j<self.ncols-1:self.neighbors[i][j+1]+=1

        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.board[i][j]==0:
                    if self.neighbors[i][j]==3 : self.board[i][j]=1
                else:
                    if self.neighbors[i][j]!=2 and self.neighbors[i][j]!=3: self.board[i][j]=0

class Controller(object):
    def __init__(self):
        self.pause=1
        self.root = Tk()
        self.root.title="hello"
        self.frame0=Frame(self.root)
        self.frame0.pack()
        self.spawnButton = Button(self.frame0,text='spawn',width=10,command=self.start)
        self.spawnButton.pack(side=LEFT)
        self.pauseButton = Button(self.frame0, text='pause',width=10,command=self.pauseGame)
        self.pauseButton.pack(side=LEFT)

        self.frame1=Frame(self.root)
        self.frame1.pack()
        self.rowLabel = Label(self.frame1,text="rows")
        self.rowLabel.pack(side=LEFT)
        self.rowsText = Spinbox(self.frame1,width=5,from_=1, to = 100)
        self.rowsText.pack(side=LEFT)
        self.colLabel = Label(self.frame1,text="cols")
        self.colLabel.pack(side=LEFT)
        self.colsText = Spinbox(self.frame1,width=5,from_=1, to = 100)
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
        self.canvas.pack()

        self.start()

        self.root.mainloop()



    def pauseButtonConfigure(self):
        if self.pause ==0:
            self.pauseButton.config(text='pause')
        else:
            self.pauseButton.config(text='play')


    def start(self):
        self.pause=1
        self.pauseButtonConfigure()

        self.nrows = int(self.rowsText.get())
        self.ncols = int(self.colsText.get())
        self.pattern=Life(self.nrows,self.ncols)
        self.canvas.delete(ALL)
        self.pattern.printBoardGraphics(self.canvas)

        self.pattern.generation=1
        self.genLabel.config(text=str(self.pattern.generation))



    def pauseGame(self):
        self.pause=1-self.pause
        self.pauseButtonConfigure()
        self.pauseTime=50
        while not self.pause:
            self.canvas.delete(ALL)
            self.pattern.printBoardGraphics(self.canvas)
            self.pattern.update()
            self.canvas.update()
            self.canvas.after(self.pauseTime)
            self.genLabel.config(text=str(self.pattern.generation))
a=Controller()
