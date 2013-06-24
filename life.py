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

    def printBoard(self):
        print ("="*100)
        for i in range(self.nrows):
            for j in range(self.ncols):
                if(self.board[i][j]) == 1:
                    print("*"),
                else:
                    print(" "),
            print("")


    def printNeighbors(self):
        print("===========neighbors==========")
        for i in range(self.nrows):
            for j in range(self.ncols):
                print(self.neighbors[i][j]),
            print("")


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
                    
        


pattern=Life(20,20)
for i in range(20):
    pattern.printBoard()
    pattern.update()
    



        




