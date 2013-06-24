"""
==================================================================
                          Game of Life
==================================================================
(c) Christian J. Burnham, DT12127103, Dublin Institute of Technology, Jun 2013
------------------------------------------------------------------

This code implements the 'Game of Life' cellular automaton, using the rules 
developed by John Horton Conway.

Toroidal boundary conditions are used throughout.
"""

from Tkinter import * 
from itertools import * 
import tkMessageBox,tkFileDialog

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

        for i in xrange(self.nrows):
            column=[]
            self.board.append([0]*self.ncols)
            self.neighbors.append([0]*self.ncols)

    def randomize(self,percentage):
        """
        Fill the board according to the percentage, where 0 < percentage < 100.
        """

        self.board = []
        for i in xrange(self.nrows):
            column=[]
            for j in xrange(self.ncols):
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
            i = val/self.ncols
            j = val%self.ncols
            self.board[i][j] = 1


    def getTupleFromPattern(self):
        """
        Generates a tuple from the pattern, where the tuple encodes the 2D pattern as
        a list of 1D integers.
        """
        patternList = []
        for i in xrange(self.nrows):
            for j in xrange(self.ncols):
                if self.board[i][j]:
                    patternList.append(i*self.ncols+j)
        return tuple(patternList)

    def printBoardGraphics(self,canvas,cellWidth):
        """
        Displays a graphical representation of the board onto a tkinter canvas, which 
        it takes as input.
        """

# First draw in grid
        for i in xrange(self.ncols+1):
            canvas.create_line(cellWidth*i+5,5,cellWidth*i+5,cellWidth*(self.nrows)+5)

        for j in xrange(self.nrows+1):
            canvas.create_line(5,cellWidth*j+5,cellWidth*(self.ncols)+5,cellWidth*j+5)

# Now draw in live cells
        for i in xrange(self.ncols):
            for j in xrange(self.nrows):
                if(self.board[j][i]) == 1:
                    canvas.create_rectangle(cellWidth*i+5,cellWidth*j+5,cellWidth*(i+1)+5,cellWidth*(j+1)+5,fill='red')

    def printBoard(self):
        """
        Displays a textual representation of the board, output to the monitor window.
        """

        for i in xrange(self.nrows):
            for j in xrange(self.ncols):
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

        for i in xrange(self.nrows):
            for j in xrange(self.ncols):
                self.board[i][j]=0
                

    def clearNeighbors(self):
        """
        Clears the 2D list self.neighbors[][] containing the neighbors.
        """

        for i in xrange(self.nrows):
            for j in xrange(self.ncols):
                self.neighbors[i][j]=0

    def update(self):
        """
        Finds the pattern on the n+1 th step, from the pattern on the nth step 
        using Conway's rule-set.
        """

        self.generation += 1
        self.clearNeighbors()

        for i in range(3):
            for j in range(3):
                b = self.board[i][j]
                bnew = randint(0,1)
                if b == 0 and bnew == 1: self.ncells+=1
                if b == 1 and bnew == 0: self.ncells-=1
                self.board[i][j]=bnew


        for i in xrange(self.nrows):
            for j in xrange(self.ncols):
                if(self.board[i][j]):
# Note use of periodic (toroidal) boundary conditions
                    iplus=(i+1)%self.nrows
                    iminus=(i-1)%self.nrows
                    jplus=(j+1)%self.ncols
                    jminus=(j-1)%self.ncols
                    self.neighbors[iminus][j     ]+=1
                    self.neighbors[iminus][jminus]+=1
                    self.neighbors[iminus][jplus ]+=1
                    self.neighbors[iplus ][jminus]+=1
                    self.neighbors[iplus ][j     ]+=1
                    self.neighbors[iplus ][jplus ]+=1
                    self.neighbors[i     ][jminus]+=1
                    self.neighbors[i     ][jplus ]+=1

        for i in xrange(self.nrows):
            for j in xrange(self.ncols):
                if self.board[i][j]==0:
                    if self.neighbors[i][j]==3:
                        self.board[i][j]=1
                        self.ncells += 1
                else:
                    if self.neighbors[i][j]!=2 and self.neighbors[i][j]!=3: 
                        self.board[i][j]=0
                        self.ncells -= 1

    def countNcells(self):
        """
        sets self.ncells to the number of live cells on the board
        """

        ncells=0
        for i in xrange(self.nrows):
            for j in xrange(self.ncols):
                if self.board[i][j]: ncells+=1

        self.ncells = ncells

    def getBoard(self):
        """
        getter for board.  Note, board is mutable, so changes to board outside of this class will also cause changes inside.
        """
        return self.board

    def getGeneration(self):
        """
        getter for generation
        """
        return self.generation

    def setGeneration(self,gen):
        """
        setter for generation
        """
        self.generation = gen

    def getNcells(self):
        """
        getter for ncells
        """
        return self.ncells

    def setNcells(self,nc):
        """
        setter for ncells
        """
        self.ncells = nc
    

class Controller(object):
    """
    This object acts as the controller for the game and also 
    draws the interface using tkinter.

    self.pause = A Boolean showing whether the game is playing/paused.
    self.enumerate = A Boolean showing whether the game is searching for still-life patterns.
    self.percentage = The fill density used to create a random pattern.
    self.nrows = The initial number of rows.
    self.ncols = The initial number of columns.
    self.nevery = The graphical display is updated every nevery steps.
    self.cellWidth = The size of the individual cells when plotted on the canvas.  (Width = Height)
    """

    def __init__(self):
        self.pause=1
        self.enumerate=0
        self.percentage = 50
        self.nrows = 40
        self.ncols = 40
        self.nevery = 1

        self.root = Tk()
        self.root.title("Game of Life")
        self.root.minsize(300,300)
        self.root.geometry("1000x500")

        self.cellWidth = 8

        self.myContainer1 = Frame(self.root) 
        self.myContainer1.pack()

        self.top_frame = Frame(self.myContainer1) 
        self.top_frame.pack(side=TOP,
          fill=BOTH, 
          expand=YES,
          )  

        self.left_frame = Frame(self.top_frame, background="white",
          borderwidth=5,  relief=RIDGE,
          height=250, 
          width=200, 
          )
        self.left_frame.pack(side=LEFT,
          fill=BOTH, 
          expand=YES,
          )

        self.right_frame = Frame(self.top_frame, background="white",
          borderwidth=5,  relief=RIDGE,
          width=6000,height=6000
          )
        self.right_frame.pack(side=RIGHT,
          fill=BOTH, 
          expand=YES,
          ) 
        self.right_frame.pack_propagate(0)

        labelfont = ('Ariel', 30, 'bold')
        self.label = Label(self.left_frame,font=labelfont,text='Game of Life')
        self.label.pack(pady=30)

        self.toolFrame=Frame(self.left_frame,pady=10)
        self.toolFrame.pack()
        
        self.saveButton = Button(self.toolFrame, text='Save',command = self.saveFile)
        self.saveButton.pack(side=LEFT)
        self.openButton = Button(self.toolFrame, text='Open',command = self.openFile)
        self.openButton.pack(side=LEFT)
        self.quitButton = Button(self.toolFrame, text = 'Quit',command = self.quit)
        self.quitButton.pack(side=LEFT)

        self.frame0=Frame(self.left_frame)
        self.frame0.pack()

        self.randomButton = Button(self.frame0,text='random',width=6,command=self.random)
        self.randomButton.pack(side=LEFT)
        
        self.densLabel = Label(self.frame0,text = 'using %:')
        self.densLabel.pack(side = LEFT)

        self.densityText = Spinbox(self.frame0,width = 5, from_=0, to=100, command = self.random)
        self.densityText.pack(side=LEFT)
        self.densityText.delete(0,"end")
        self.densityText.insert(0,self.percentage)
        self.densityText.bind('<Return>',lambda event:self.random())

        self.frame1=Frame(self.left_frame)
        self.frame1.pack()

        self.clearButton = Button(self.frame1,text='clear',command=self.clear)
        self.clearButton.pack(side=LEFT)
        self.pauseButton = Button(self.frame1, text='pause',width=5, command=self.playPauseGame)
        self.pauseButton.pack(side=LEFT)
        self.stepButton = Button(self.frame1, text='step',command=self.stepAndPlot)
        self.stepButton.pack(side=LEFT)

        self.frame2=Frame(self.left_frame)
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

        self.speedFrame = Frame(self.left_frame)
        self.speedFrame.pack()
        self.speedVar = IntVar()
        self.speedLabel = Label(self.speedFrame,text = 'speed     ')
        self.speedLabel.pack(side=LEFT)
        self.speedSlider = Scale(self.speedFrame, from_=1, to = 20,orient = HORIZONTAL,variable = self.speedVar)
        self.speedSlider.set(5)
        self.speedSlider.pack(side=LEFT)

        self.canvas = Canvas(self.right_frame,width=500,height=500,background='white',cursor='pencil')
        self.canvas.bind("<Button-1>",lambda event:self.clickCell(event,1))
        self.canvas.bind("<B1-Motion>",lambda event:self.clickCell(event,1))
        self.canvas.bind("<Control-Button-1>",lambda event:self.clickCell(event,-1))
        self.canvas.bind("<Control-B1-Motion>",lambda event:self.clickCell(event,-1))
        self.canvas.pack()

        self.frame3=Frame(self.right_frame)
        self.frame3.pack()
        self.genTextLabel=Label(self.frame3,text="generation ")
        self.genLabel = Label(self.frame3,text="0")
        self.genTextLabel.pack(side=LEFT)
        self.genLabel.pack(side=LEFT)
        self.popTextLabel=Label(self.frame3,text='    population =')
        self.popLabel = Label(self.frame3,text="0")
        self.popTextLabel.pack(side=LEFT)
        self.popLabel.pack(side=LEFT)


        self.stillFrame=Frame(self.left_frame,pady=50)
        self.stillFrame.pack()

        self.enumerateButton = Button(self.stillFrame, text='Find Still Lifes',width = 13, command=self.findStillLife)
        self.enumerateButton.pack(side=LEFT)

        self.sizeLabel=Label(self.stillFrame, text = '   n:')
        self.sizeLabel.pack(side=LEFT)

        self.stillSize = Spinbox(self.stillFrame,width=5,from_=1, to = 1000)
        self.stillSize.pack(side=LEFT)
        self.stillSize.delete(0,"end")
        self.stillSize.insert(0,8)
        self.stillSize.bind('<Return>',lambda event:self.stillVerify())


        self.percentage = int(self.densityText.get())
        self.reshape()
        self.random()
        self.root.mainloop()


    def quit(self):
        """
        Quits program
        """
        self.pause = 1
        self.root.quit()

    def saveFile(self):
        """
        Saves the current pattern
        """
        file = tkFileDialog.asksaveasfile(mode='w',defaultextension = '.life')
        if file:
            tuple = self.pattern.getTupleFromPattern()
            
            file.write("%s %s\n" %(self.nrows,self.ncols))
            gen = self.pattern.getGeneration()
            file.write("%s\n" %gen)
            file.write(str(tuple))

    def openFile(self):
        """
        Opens a pattern from a file
        """
        file = tkFileDialog.askopenfile(mode='r',defaultextension = '.life',filetypes=[('Life patterns','.life')])
        if file:
            rowsCols=file.readline().split(" ")
            self.nrows = int(rowsCols[0])
            self.ncols = int(rowsCols[1])

            self.rowsText.delete(0,"end")
            self.rowsText.insert(0,self.nrows)

            self.colsText.delete(0,"end")
            self.colsText.insert(0,self.ncols)
            self.reshape()

            gen=int(file.readline())
            self.genLabel.config(text = str(gen))
            self.pattern.setGeneration(gen)

            tuple = eval(file.read())
            self.pattern.setPatternFromTuple(tuple)

            ncells = int(self.stillSize.get())
            self.pattern.countNcells()
            ncells = self.pattern.getNcells()
            self.popLabel.config(text=str(ncells))

            self.canvas.delete(ALL)
            self.pattern.printBoardGraphics(self.canvas,self.cellWidth)
            self.canvas.update()


    def abandonSearch(self):
        """
        Called when a search for still lifes is abandoned halfway through
        """

        self.enumerate=0
        self.enumerateButton.config(text='Find Still Lifes',command = self.findStillLife)

#Enable all the buttons that were greyed out during the enumeration

        self.pauseButton.config(state=NORMAL)
        self.randomButton.config(state=NORMAL)
        self.clearButton.config(state=NORMAL)
        self.stepButton.config(state=NORMAL)
        self.rowsText.config(state=NORMAL)
        self.colsText.config(state=NORMAL)
        self.densityText.config(state=NORMAL)
        self.stillSize.config(state=NORMAL)
        self.saveButton.config(state=NORMAL)
        self.openButton.config(state=NORMAL)
        self.quitButton.config(state=NORMAL)

        self.updateDisplay()

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

        self.canvas.config(width=self.cellWidth*self.ncols+5,height=self.cellWidth*self.nrows+5)
        w=max(self.cellWidth*self.ncols+300,480)
        h=max(self.cellWidth*self.nrows+35,410)

        self.root.geometry("%dx%d" %(w,h))
        self.root.update()

        self.pattern=Life(self.nrows,self.ncols,self.percentage)

        gen = 1
        self.pattern.setGeneration(gen)
        self.updateDisplay()

    def clickCell(self,event,draw):
        """
        Called when the user clicks on the canvas, which makes the cell under the mouse go live.
        """
#  draw parameter:
#  +1 draws a live cell on click
#  -1 erases a live cell on click

        i = int((event.x-5)/self.cellWidth)
        j = int((event.y-5)/self.cellWidth)

        board =self.pattern.getBoard()

        self.pattern.countNcells()
        ncells = self.pattern.getNcells()
        if -1<i<self.ncols  and -1<j<self.nrows:

            redraw = 0
            if board[j][i]==0 and draw == 1:
                board[j][i]=1
                ncells += 1
                redraw = 1
            elif board[j][i]==1 and draw == -1:
                board[j][i]=0
                ncells += -1
                redraw = 1

            if redraw:
                self.canvas.delete(ALL)
                self.pattern.printBoardGraphics(self.canvas,self.cellWidth)
                self.canvas.update()

                self.pattern.setNcells(ncells)
                self.popLabel.config(text=str(ncells))

    def pauseButtonConfigure(self):
        """
        Used to configure the pause button and to make sure its text reflects the value of 
        the Boolean self.pause.
        """

        if self.pause == 0:
            self.pauseButton.config(text='pause')
        else:
            self.pauseButton.config(text='play')
        self.updateDisplay()

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

        self.percentage = int(self.densityText.get())
        self.pattern=Life(self.nrows,self.ncols,self.percentage)

        gen = 1
        self.pattern.setGeneration(gen)

        self.pattern.randomize(self.percentage)
        self.updateDisplay()

    def stillVerify(self):
        """
        Called to verify that text entry of the number of still lifes is integer
        """
        if not self.stillSize.get().isdigit():
            tkMessageBox.showinfo("Alert","Not an integer")
            self.stillSize.delete(0,"end")
            self.stillSize.insert(0,'8')


    def findStillLife(self):
        """
        Called when the 'Find Still Lifes' button is pressed. 
        Enumerates all still-lifes of a given size.  
        Note- toroidal boundary conditions are 
        *not* used when finding still lifes.  Instead, the algorithm searches all possible 
        patterns inside a 1 cell 'safety-margin' about the perimeter, in order to remove 
        any boundary effects.
        """
        self.enumerate=1
        gen = 1
        self.pattern.setGeneration(gen)

# Disable all the buttons that shouldn't be clicked during the enumeration
        self.pauseButton.config(state=DISABLED)
        self.randomButton.config(state=DISABLED)
        self.clearButton.config(state=DISABLED)
        self.stepButton.config(state=DISABLED)
        self.rowsText.config(state=DISABLED)
        self.colsText.config(state=DISABLED)
        self.densityText.config(state=DISABLED)
        self.stillSize.config(state=DISABLED)
        self.saveButton.config(state=DISABLED)
        self.openButton.config(state=DISABLED)
        self.quitButton.config(state=DISABLED)

        self.enumerateButton.config(text='Abandon Search',command = self.abandonSearch)

# Iterate over all patterns in a board of dimension (nrows-2)*(ncols-2), 
# the size of the board within a 1 square safety margin around the perimeter.

        ncols_reduced = self.ncols-2
        nrows_reduced = self.nrows-2

        n = nrows_reduced*ncols_reduced
        i = int(self.stillSize.get())
        for tuplej in combinations(xrange(n),i):
            if not self.enumerate: break

# reflected1, reflected2 and reflected3 hold representations of the pattern reflected horizontally, vertically and 
# horizontally + vertically.
# For square patterns, reflected4 swaps rows and columns, then reflected5, reflected6 and reflected7 are representations 
# of reflected4 reflected horizontally, vertically and horizontally + vertically.

            reflected1=[]
            reflected2=[]
            reflected3=[]
            reflected4=[]
            reflected5=[]
            reflected6=[]
            reflected7=[]

# iflag indicates whether the pattern has at least one live cell in the top-most row (within the margin)
# jflag indicates whether the pattern has at least one live cell in the left-most column (within the margin)

            iflag = 0
            jflag = 0

# Halt enumeration if the first live cell in the tuple is in a column more than half-way accross the width of the board.
# All subsequent patterns are translations and rotations of patterns encountered so far.
# Proof:  If the first cell is in row 0, then the reflection j -> ncols-1-j results in a pattern where j is less than half-way across the 
# width of the board and so will already have been enumerated.  
# If the first cell is not in row 0, then a translation can take the pattern to one which has its first cell in row 0.

            j0 = tuplej[0]%ncols_reduced
            if j0 > ncols_reduced-1-j0: break

            for m in tuplej:
                i = m/ncols_reduced
                j = m%ncols_reduced

                if i==0: iflag = 1
                if j==0: jflag = 1

                i2 = nrows_reduced-1-i
                j2 = j
                reflected1.append(i2*ncols_reduced+j2)

                i3 = i
                j3 = ncols_reduced-1-j
                reflected2.append(i3*ncols_reduced+j3)

                i4 = nrows_reduced-1-i
                j4 = ncols_reduced-1-j
                reflected3.append(i4*ncols_reduced+j4)

# For square boards
                if(self.nrows==self.ncols):
                    reflected4.append(j*ncols_reduced+i)
                    reflected5.append(j2*ncols_reduced+i2)
                    reflected6.append(j3*ncols_reduced+i3)
                    reflected7.append(j4*ncols_reduced+i4)


    # Check the pattern is not a tranlation.  Only count patterns which have a live cell in row 0 and a live cell in column 0.  All other 
    # patterns may be considered translations.

            if iflag and jflag:

    # Only step pattern if it is not a reflection along either 4 of the symmetries of a rectangle or 8 symmetries of the square.

                if          tuplej <= tuple(sorted(reflected1)) and tuplej <= tuple(sorted(reflected2))\
                        and tuplej <= tuple(sorted(reflected3)):

    # For square boards
                    if self.nrows!=self.ncols or (tuplej <= tuple(sorted(reflected4))\
                        and tuplej <= tuple(sorted(reflected5)) and tuplej <= tuple(sorted(reflected6))\
                        and tuplej <= tuple(sorted(reflected7))):

            #Convert pattern tuple to format for board of dimension nrows*ncols
                        list=[]
                        for val in tuplej:
                            i = 1 + val/ncols_reduced
                            j = 1 + val%ncols_reduced
                            list.append(i*self.ncols+j)

            # Set the pattern from the tuple and plot it

                        tuplej2=tuple(list)
                        self.pattern.setPatternFromTuple(tuplej2)
                        ncells = int(self.stillSize.get())
                        self.pattern.setNcells(ncells)

                        self.setPatternSpeed()
                        gen = self.pattern.getGeneration()
                        if gen % int(self.nevery)==0:
                            self.updateDisplay()

            # Evolve the pattern for 1 generation
                        self.pattern.update()
                        tuplek = self.pattern.getTupleFromPattern()

            # If it's a still life, the pattern before and after will be identical.  
            # Print out the still lifes to the terminal.
                        if set(tuplej2) == set(tuplek): 
                            print('='*30)
                            print tuplej2
                            self.pattern.printBoard()
        self.enumerate=0
        self.pause = 1
        self.pauseButton.config(text='play')

        self.abandonSearch()

    def playPauseGame(self):
        """
        Called when the pause or play button is pressed.
        The game loop is contained in the while-loop in this method.
        """

        self.pause=1-self.pause
        self.pauseButtonConfigure()

        if not self.enumerate:
            while not self.pause:
                self.setPatternSpeed()
                self.step()

    def setPatternSpeed(self):
        """
        Determines the speed at which the pattern is run.
        If speedVar < 10 then a pause is used (using canvas.after)
        if speedVar = 10 then no pause is used
        if speedVar > 10 then frames are dropped from the draw
        """

        if self.speedVar.get()<=10:
            self.canvas.after((10-self.speedVar.get())*10)
            self.nevery = 1
        else:
            self.nevery = 1+pow(2,self.speedVar.get()-10)
        
    def stepAndPlot(self):
        """
        Steps the game by one generation and plots the result.
        """
        self.nevery=1
        self.step()


    def step(self):
        """
        Steps the game by one generation.
        """
        ncells = self.pattern.getNcells()
        if ncells:
            self.pattern.update()
        else:
            self.pause=1
            self.pauseButtonConfigure()
            self.updateDisplay()

        gen = self.pattern.getGeneration()
        if gen % int(self.nevery) == 0:
            self.updateDisplay()

    def updateDisplay(self):
        """
        updates the graphics and the labels
        """
        self.canvas.update()
        self.canvas.delete(ALL)
        self.pattern.printBoardGraphics(self.canvas,self.cellWidth)
        ncells = self.pattern.getNcells()
        self.popLabel.config(text=str(ncells))
        gen = self.pattern.getGeneration()
        self.genLabel.config(text=str(gen))

if __name__=="__main__": a = Controller()
