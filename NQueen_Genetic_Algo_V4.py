import random

class GeneticChess:

    def __init__(self,n):
        self.size = n
        self.board = self.createBoard(self.size)
        self.env = []
        self.goal = None
        self.goalIndex = -1
        self.totalClash = None
        self.maxFitness = (self.size*(self.size-1))/2

    #def getFitness(self):
    #    return(int(self.maxFitness - self.totalClash))

    ##Below function will generate the board
    def generateBoard(self):
        #print("{}".format(self.Board))
        for i in range(self.N):
            tempBoard=[]
            for j in range(self.N):
                tempBoard.append(0)
                #print(tempBoard)
            self.Board.append(tempBoard)
        #pprint.pprint(self.Board)
        ##return Board

    def createBoard(self,n):
        board = [[0 for i in range(n)] for j in range(n)]
        print(board)
        return board

    def setBoard(self,board,gen):
        for i in range(self.size):
            print("i : {} gen[i] : {}".format(i,gen))
            board[gen[i]][i] = 1
    
    def genereteDNA(self):
        #genereates random list of length n
        DNA = list(range(self.size))
        random.shuffle(DNA)
        while DNA in self.env:
            random.shuffle(DNA)
        return DNA

    #Generate initial selections of random 1000 boards
    def initializeFirstGenereation(self):
        for i in range(1000):
            self.env.append(self.genereteDNA())

    #Score of the sample
    #Score 0 means no clash. That means this sample is perfect i.e. this is the result
    def calculateClashes(self,gen):
        clash = 0
        board = self.createBoard(self.size)
        self.setBoard(board,gen)
        col = 0

        for dna in gen:

            # Check for all columns of this row
            for i in range(col-1,-1,-1):
                if board[dna][i] == 1:
                    clash+=1

            # Check diagonal above the cell
            for i,j in zip(range(dna-1,-1,-1),range(col-1,-1,-1)):
                if board[i][j] == 1:
                    clash+=1

            # Check the diagonal below the cell
            for i,j in zip(range(dna+1,self.size,1),range(col-1,-1,-1)):
                if board[i][j] == 1:
                    clash+=1
            col+=1

        self.totalClash = clash
        #print("Selection score : {}".format(clash))
        return clash

    def isResult(self,gen):
        if self.calculateClashes(gen) == 0:
            return True
        return False

    #Cross over logic:
    #The first section are interchanged
    def crossOverGens(self,firstGen,secondGen):
        bound = self.size/2
        for i in range(bound):
            firstGen[i],secondGen[i] = secondGen[i],firstGen[i]

    #Mulation logic:
    #Make random selection of the list swap them
    def MutantGen(self,gen):
        bound = self.size/2
        leftSideIndex = random.randint(0,bound)
        RightSideIndex = random.randint(bound+1,self.size-1)
        gen[leftSideIndex],gen[RightSideIndex] = gen[RightSideIndex],gen[leftSideIndex]

    #Generate two children
    def crossOverAndMutant(self):
        for i in range(1,len(self.env),2):
            firstGen = self.env[i-1][:]
            secondGen = self.env[i][:]
            self.crossOverGens(firstGen,secondGen)
            firstGen = self.MutantGen(firstGen)
            secondGen = self.MutantGen(secondGen)
            self.env.append(firstGen)
            self.env.append(secondGen)

    def makeSelection(self):
        genUtilities = []
        newEnv = []

        print("genUtilities : {}".format(genUtilities))

        for gen in self.env:
            genUtilities.append(self.calculateClashes(gen))
        if min(genUtilities) == 0:
            self.goalIndex = genUtilities.index(min(genUtilities))
            self.goal = self.env[self.goalIndex]
            return self.env
        minUtil=None
        while len(newEnv)<self.size:
            minUtil = min(genUtilities)
            minIndex = genUtilities.index(minUtil)
            newEnv.append(self.env[minIndex])
            genUtilities.remove(minUtil)
            self.env.remove(self.env[minIndex])

        return newEnv

    def generateNQueen(self):
        self.initializeFirstGenereation()
        for gen in self.env:
            if self.isResult(gen):
                return gen
        count = 0
        while True:
            print("I am here")
            self.crossOverAndMutant()
            self.env = self.makeSelection()
            count +=1
            if self.goalIndex >= 0 :
                try:
                    print(count)
                    return self.goal
                except IndexError:
                    print(self.goalIndex)
            else:
                continue

chess = GeneticChess(8)
solution = chess.generateNQueen()
print("Dimension 8 completed")
#print("Fitness : ".format(chess.currentSampleFitness))
print(solution)
