"""
==================================================================
                          Game of Life
==================================================================
(c) Christian J. Burnham, Dublin Institute of Technology, Jun 2013
------------------------------------------------------------------

This code implements the 'Game of Life' cellular automaton, using the rules 
developed by John Horton Conway.

Toroidal boundary conditions are used throughout.
"""

from Tkinter import * 
from itertools import * 
import tkMessageBox

from random import randint
class Life(object):
    """
    This object implements the game board and also holds the pattern.
    
    self.nrows = number of rows
    self.ncols = number of columns
    self.board = 2D list (nrows x ncols) containing the pattern
    self.neighbors = 2D List (nrows x ncols) containing the number of neighbors of each cell (in toroidal boundary conditions)
    self.generation = the generation number of the pattern
    self.ncells = the number of live cells currently in the pattern
    """
    def __init__(self,nrows,ncols,percentage):
        self.nrows = nrows
        self.ncols = ncols
        self.board = []
        self.neighbors = []
        self.generation = 1

        self.ncells=0

        for i in range(self.nrows):
            column=[]
            self.board.append([0]*self.ncols)
            self.neighbors.append([0]*self.ncols)

    def randomize(self,percentage):
        """
        Fill the board according to the percentage, where 0 < percentage < 100.
        """

        self.board = []
        for i in range(self.nrows):
            column=[]
            for j in range(self.ncols):
                rint=0
                if randint(1,100)<=percentage:  
                    rint=1
                    self.ncells += 1
                column.append(rint)
            self.board.append(column)

    def setPatternFromTuple(self,tuple):
        """
        Creates a board pattern from a tuple, where the tuple encodes the 2D pattern as
        a list of 1D integers.
        """

        self.clear()
# Use modular arithmetic to code 2D pattern as 1D values.
        for val in tuple:
            i = val%self.nrows
            j = val/self.nrows
            self.board[i][j] = 1

    def getTupleFromPattern(self):
        """
        Generates a tuple from the pattern, where the tuple encodes the 2D pattern as
        a list of 1D integers.
        """
        patternList = []
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.board[i][j]:
                    patternList.append(i+j*self.ncols)
        return tuple(patternList)

    def printBoardGraphics(self,canvas):
        """
        Displays a graphical representation of the board onto a tkinter canvas, which 
        it takes as input.
        """

        for i in range(self.ncols):
            for j in range(self.nrows):
                if(self.board[j][i]) == 1:
                    canvas.create_rectangle(10*i+5,10*j+5,10*(i+1)+5,10*(j+1)+5,fill='red')
                else:
                    canvas.create_rectangle(10*i+5,10*j+5,10*(i+1)+5,10*(j+1)+5,fill='white')

    def printBoard(self):
        """
        Displays a textual representation of the board, output to the monitor window.
        """

        for i in range(self.nrows):
            for j in range(self.ncols):
                if(self.board[i][j]) == 1:
                    print("*"),
                else:
                    print("-"),
            print("")


    def clear(self):
        """
        Clears all cells on board.
        """

        self.ncells = 0
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.board[i][j]=0
                

    def clearNeighbors(self):
        """
        Clears the 2D list self.neighbors[][] containing the neighbors.
        """

        for i in range(self.nrows):
            for j in range(self.ncols):
                self.neighbors[i][j]=0

    def update(self):
        """
        Finds the pattern on the n+1 th step, from the pattern on the nth step 
        using Conway's rule-set.
        """

        self.generation += 1
        self.clearNeighbors()

        for i in range(self.nrows):
            for j in range(self.ncols):
                if(self.board[i][j]):
# Note use of toroidal boundary conditions
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
                    if self.neighbors[i][j]==3 : 
                        self.board[i][j]=1
                        self.ncells += 1
                else:
                    if self.neighbors[i][j]!=2 and self.neighbors[i][j]!=3: 
                        self.board[i][j]=0
                        self.ncells -= 1

class Controller(object):
    """
    This object acts as the controller for the game and also 
    draws the interface using tkinter.

    self.pause = A Boolean showing whether the game is playing/paused.
    self.enumerate = A Boolean showing whether the game is searching for still-life patterns.
    self.percentage = The fill density used to create a random pattern.
    self.nrows = The initial number of rows.
    self.ncols = The initial number of columns.
    self.pauseTime = The pause time between frames when the game is running.  
    """

    def __init__(self):
        self.pause=1
        self.enumerate=0
        self.percentage = 50
        self.nrows = 40
        self.ncols = 40
        self.pauseTime=50


        self.root = Tk()
        self.root.title("Game of Life")
        self.root.minsize(300,300)
        self.root.geometry("500x700")

        labelfont = ('times', 30, 'bold')
        self.label = Label(self.root,font=labelfont,text='Game of Life')

        self.label.pack()

        self.frame0=Frame(self.root)
        self.frame0.pack()

        self.randomButton = Button(self.frame0,text='random',width=10,command=self.random)
        self.randomButton.pack(side=LEFT)
        
        self.densLabel = Label(self.frame0,text = 'using %:')
        self.densLabel.pack(side = LEFT)

        self.densityText = Spinbox(self.frame0,width = 5, from_=0, to=100, command = self.random)
        self.densityText.pack(side=LEFT)
        self.densityText.delete(0,"end")
        self.densityText.insert(0,self.percentage)
        self.densityText.bind('<Return>',lambda event:self.random())

        self.frame1=Frame(self.root)
        self.frame1.pack()

        self.clearButton = Button(self.frame1,text='clear',width=10,command=self.clear)
        self.clearButton.pack(side=LEFT)
        self.pauseButton = Button(self.frame1, text='pause',width=10,command=self.playPauseGame)
        self.pauseButton.pack(side=LEFT)
        self.stepButton = Button(self.frame1, text='step',width=10,command=self.step)
        self.stepButton.pack(side=LEFT)

        self.frame2=Frame(self.root)
        self.frame2.pack()
        self.rowLabel = Label(self.frame2,text="rows")
        self.rowLabel.pack(side=LEFT)
        self.rowsText = Spinbox(self.frame2,width=5,from_=1, to = 100,command=self.reshape)
        self.rowsText.pack(side=LEFT)
        self.rowsText.bind('<Return>',lambda event:self.reshape())

        self.colLabel = Label(self.frame2,text="cols")
        self.colLabel.pack(side=LEFT)
        self.colsText = Spinbox(self.frame2,width=5,from_=1, to = 100,command=self.reshape)
        self.colsText.pack(side=LEFT)
        self.colsText.bind('<Return>',lambda event:self.reshape())

        self.rowsText.delete(0,"end")
        self.rowsText.insert(0,self.nrows)

        self.colsText.delete(0,"end")
        self.colsText.insert(0,self.ncols)

        self.frame3=Frame(self.root)
        self.frame3.pack()
        self.genTextLabel=Label(self.frame3,text="generation ")
        self.genLabel = Label(self.frame3,text="0")
        self.genTextLabel.pack(side=LEFT)
        self.genLabel.pack(side=LEFT)
        self.popTextLabel=Label(self.frame3,text='    population =')
        self.popLabel = Label(self.frame3,text="0")
        self.popTextLabel.pack(side=LEFT)
        self.popLabel.pack(side=LEFT)

        self.canvas = Canvas(self.root,width=500,height=500,background='white')
        self.canvas.bind("<Button-1>",lambda event:self.clickCell(event))
        self.canvas.bind("<B1-Motion>",lambda event:self.clickCell(event))
        self.canvas.pack()

        self.frame4=Frame(self.root)
        self.frame4.pack()

        self.enumerateButton = Button(self.frame4, text='Find Still Lives',command=self.findStillLife)
        self.enumerateButton.pack(side=LEFT)

        self.sizeLabel=Label(self.frame4, text = '   n:')
        self.sizeLabel.pack(side=LEFT)

        self.stillSize = Spinbox(self.frame4,width=5,from_=1, to = 1000)
        self.stillSize.pack(side=LEFT)
        self.stillSize.delete(0,"end")
        self.stillSize.insert(0,20)
        self.stillSize.bind('<Return>',lambda event:self.stillVerify())

        self.percentage = int(self.densityText.get())
        self.random()
        self.root.mainloop()

    def abandonSearch(self):
        """
        Called when a search for still lives is abandoned halfway through
        """

        self.enumerate=0
        self.enumerateButton.config(text='Find Still Lives',command = self.findStillLife)

#Enable all the buttons that were greyed out during the enumeration

        self.pauseButton.config(state=NORMAL)
        self.randomButton.config(state=NORMAL)
        self.clearButton.config(state=NORMAL)
        self.stepButton.config(state=NORMAL)
        self.rowsText.config(state=NORMAL)
        self.colsText.config(state=NORMAL)
        self.densityText.config(state=NORMAL)
        self.stillSize.config(state=NORMAL)

    def reshape(self):
        """
        Used to reshape the board when either the number of rows or number of columns changes.
        """
        if not self.rowsText.get().isdigit():
            tkMessageBox.showinfo("Alert","Not an integer")
            self.rowsText.delete(0,"end")
            self.rowsText.insert(0,'5')
        if not self.colsText.get().isdigit():
            tkMessageBox.showinfo("Alert","Not an integer")
            self.colsText.delete(0,"end")
            self.colsText.insert(0,'5')


        self.nrows = int(self.rowsText.get())
        self.ncols = int(self.colsText.get())

        self.canvas.config(width=11*self.ncols,height=11*self.nrows)

        self.pattern=Life(self.nrows,self.ncols,self.percentage)
        self.canvas.delete(ALL)
        self.pattern.printBoardGraphics(self.canvas)

        self.pattern.generation=1
        self.genLabel.config(text=str(self.pattern.generation))


    def clickCell(self,event):
        """
        Called when the user clicks on the canvas, which makes the cell under the mouse go live.
        """
        i = int((event.x-5)/10)
        j = int((event.y-5)/10)

        if -1<i<self.ncols  and -1<j<self.nrows:
            if self.pattern.board[j][i]==0:
                self.pattern.board[j][i]=1
                self.pattern.ncells+=1
            self.canvas.delete(ALL)
            self.pattern.printBoardGraphics(self.canvas)
            self.canvas.update()
            self.popLabel.config(text=str(self.pattern.ncells))

    def pauseButtonConfigure(self):
        """
        Used to configure the pause button and to make sure its text reflects the value of 
        the Boolean self.pause.
        """

        if self.pause ==0:
            self.pauseButton.config(text='pause')
        else:
            self.pauseButton.config(text='play')

    def clear(self):
        """
        Called when the 'clear' button is pressed.  Note the actual clearing of the board 
        takes place in self.reshape.
        """
        self.pause=1
        self.pauseButtonConfigure()
        self.reshape()

    def random(self):
        """
        Called when the 'random' button is pressed.  Creates a new random pattern.
        """

        if not self.densityText.get().isdigit():
            tkMessageBox.showinfo("Alert","Not an integer")
            self.densityText.delete(0,"end")
            self.densityText.insert(0,'50')

        self.pause=1
        self.pauseButtonConfigure()

        self.nrows = int(self.rowsText.get())
        self.ncols = int(self.colsText.get())

        self.canvas.config(width=11*self.ncols,height=11*self.nrows)

        self.percentage = int(self.densityText.get())
        self.pattern=Life(self.nrows,self.ncols,self.percentage)

        self.pattern.randomize(self.percentage)
        self.canvas.delete(ALL)
        self.pattern.printBoardGraphics(self.canvas)
        self.popLabel.config(text=str(self.pattern.ncells))

        self.pattern.generation=1
        self.genLabel.config(text=str(self.pattern.generation))

    def stillVerify(self):
        """
        Called to verify that text entry of the number of still lives is integer
        """
        if not self.stillSize.get().isdigit():
            tkMessageBox.showinfo("Alert","Not an integer")
            self.stillSize.delete(0,"end")
            self.stillSize.insert(0,'20')


    def findStillLife(self):
        """
        Called when the 'Find Still Lives' button is pressed. Enumerates all still-lives of 
        a given size.
        """
        self.enumerate=1

#Disable all the buttons that shouldn't be clicked during the enumeration
        self.pauseButton.config(state=DISABLED)
        self.randomButton.config(state=DISABLED)
        self.clearButton.config(state=DISABLED)
        self.stepButton.config(state=DISABLED)
        self.rowsText.config(state=DISABLED)
        self.colsText.config(state=DISABLED)
        self.densityText.config(state=DISABLED)
        self.stillSize.config(state=DISABLED)

        self.enumerateButton.config(text='Abandon Search',command = self.abandonSearch)

        n = self.nrows*self.ncols
        i = int(self.stillSize.get())
        for j in combinations(range(n),i):
            if not self.enumerate: break
            self.pattern.setPatternFromTuple(j)
            self.pattern.ncells = int(self.stillSize.get())
            self.canvas.delete(ALL)
            self.pattern.printBoardGraphics(self.canvas)
            self.canvas.update()
            self.popLabel.config(text=str(self.pattern.ncells))

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
        """
        Called when the pause or play button is pressed.
        The game loop is contained in the while-loop in this method.
        """

        self.pause=1-self.pause
        self.pauseButtonConfigure()

        if not self.enumerate:
            while not self.pause:
                self.canvas.after(self.pauseTime)
                self.step()

    def step(self):
        """
        Steps the game by one generation.
        """

        if self.pattern.ncells:
            self.pattern.update()
        else:
            self.pause=1
            self.pauseButtonConfigure()
        self.canvas.update()
        self.genLabel.config(text=str(self.pattern.generation))
        self.canvas.delete(ALL)
        self.pattern.printBoardGraphics(self.canvas)
        self.popLabel.config(text=str(self.pattern.ncells))

if __name__=="__main__": a = Controller()