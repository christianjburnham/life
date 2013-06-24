from Tkinter import * 
from random import randint
class Life:
    def __init__(self,nrows,ncols):
        self.nrows = nrows
        self.ncols = ncols
        self.board = []
        self.neighbors=[]
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
                    canvas.create_rectangle(10*i,10*j,10*(i+1),10*(j+1),fill='red')


    def update(self):
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

#        self.printNeighbors()

        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.board[i][j]==0:
                    if self.neighbors[i][j]==3 : self.board[i][j]=1
                else:
                    if self.neighbors[i][j]!=2 and self.neighbors[i][j]!=3: self.board[i][j]=0
                    
        
def start():
    nrows = int(entry_rows.get())
    ncols = int(entry_cols.get())

    pattern=Life(nrows,ncols)
    pauseTime=50
    while not pause:
        canvas.delete(ALL)
        pattern.printBoardGraphics(canvas)
        pattern.update()
        canvas.update()
        canvas.after(pauseTime)


def pauseGame():
    global pause
    pause=1-pause



pause=0
root = Tk()
frame0=Frame(root)
frame0.pack()
spawnButton = Button(frame0,text='spawn',command=start)
spawnButton.pack(side=LEFT)
pauseButton = Button(frame0, text='pause',command=pauseGame)
pauseButton.pack(side=LEFT)
frame1=Frame(root)
frame1.pack()
rowLabel = Label(frame1,text="rows")
rowLabel.pack(side=LEFT)
entry_rows = Entry(frame1,width=5)
entry_rows.pack(side=LEFT)
colLabel = Label(frame1,text="cols")
colLabel.pack(side=LEFT)
entry_cols = Entry(frame1,width=5)
entry_cols.pack(side=LEFT)

entry_rows.insert(0,'20')
entry_cols.insert(0,'20')

canvas = Canvas(root,width=500,height=500,background='white')
canvas.pack()
root.mainloop()


    



        




