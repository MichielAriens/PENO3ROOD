import GUI.gridTest as gridTest
import RPI.software.main as main
import numpy

class GridLoader:
    def __init__(self):
        pass

    def loadGrid(self, path="C:\Users\Babyburger\PycharmProjects\PENOROODpy\OTHER\grid25-04.csv"):
        import csv
        with open(path) as f:
            data=[tuple(line) for line in csv.reader(f)]
        list = []
        emptyrow = []
        for i in range(len(data)):
            list.append(emptyrow)
            row = data[i]
            for j in range(len(row)):
                oldstr = row[j]
                newstr = oldstr.replace("'", " ")
                list[i].append(newstr)
        list[0] = str(list[0]).replace("'", "")
        list[0] = str(list[0]).replace(" ", "")
        list[0] = str(list[0]).replace(",", "=")
        list[0] = str(list[0]).lower()
        number_of_rows = len(data);
        number_of_columns = len(data[0])
        init_string = list[0]
        # print 's: ' + str(init_string)
        self.grid = gridTest.GRID(number_of_columns, number_of_rows)
        self.grid.initiate(init_string);

class FindPosition:
    def __init__(self,grid):
        self.grid = grid
        self.p = (0,0)

    def findPosition(self,shapes):
        #iterate through matrix rows and perform triangle/reverseTriangle to add to possiblePositions
        #possiblePositions = []
        possiblePositions = None
        a = 0
        while(a<3):
            i = 0
            while(i<14):
                j = 0
                while(j<12):
                    self.triangle((i,j),shapes,possiblePositions)
                    self.reverseTriangle((i,j),shapes,possiblePositions)
                    j = j+1
                i = i+1
            b = shapes.pop()
            shapes.insert(0,b)
            a = a+1
        #return possiblePositions
        return self.p

    def triangle(self,position,shapes,possiblePositions = []):
        (x,y) = position
        try:
            if self.grid.item((x,y)) == shapes[0]:
                if (x%2) == 0:
                    if (self.grid.item((x+1,y-1)) == shapes[1] and self.grid.item((x+1,y)) == shapes[2]) or (self.grid.item((x+1,y-1)) == shapes[2] and self.grid.item((x+1,y)) == shapes[1]):
                        pos = self.getPosition(x+0.5,y)
                        print position
                        self.p = pos
                        #possiblePositions.append(pos)
                else:
                    if (self.grid.item((x+1,y)) == shapes[1] and self.grid.item((x+1,y+1)) == shapes[2]) or (self.grid.item((x+1,y)) == shapes[2] and self.grid.item((x+1,y+1)) == shapes[1]):
                        pos = self.getPosition(x+0.5,y+0.5)
                        print position
                        self.p = pos
                        #possiblePositions.append(pos)
        except ValueError, e:
            pass

    def reverseTriangle(self,position,shapes,possiblePositions = []):
        (x,y) = position
        try:
            if self.grid.item((x,y)) == shapes[0]:
                if (x%2) == 0:
                    if (self.grid.item((x-1,y-1)) == shapes[1] and self.grid.item((x-1,y)) == shapes[2]) or (self.grid.item((x-1,y-1)) == shapes[2] and self.grid.item((x-1,y)) == shapes[1]):
                        pos = self.getPosition(x-0.5,y)
                        print position
                        self.p = pos
                        #possiblePositions.append(pos)
                else:
                    if (self.grid.item((x-1,y)) == shapes[1] and self.grid.item((x-1,y+1)) == shapes[2]) or (self.grid.item((x-1,y)) == shapes[2] and self.grid.item((x-1,y+1)) == shapes[1]):
                        pos = self.getPosition(x-0.5,y+0.5)
                        print position
                        self.p = pos
                        #possiblePositions.append(pos)
        except ValueError, e:
            pass

    def getPosition(self,x,y):
        xx = x*36
        yy = y*40
        pos = (xx,yy)
        return pos

class Main:
    def __init__(self):
        self.g = GridLoader()
        self.g.loadGrid()

    def getPosition(self,path="C:/Users/Babyburger/PycharmProjects/PENOROODpy/output/5.jpg"):
        shapes = main.userInterface().findZeppelinLocation(path)

        #print self.g.grid.table
        table = self.g.grid.table
        m = numpy.matrix(table)
        m2 = m.transpose()
        #print m2

        newshapes = []
        #g.grid.getPosAlternative([('blue','rectangle'),('green','rectangle'),('yellow','heart')])
        for (color,shape) in shapes:
            c = color[0]
            s = shape[0]
            id = self.g.grid.getShapeID(c+s)
            newshapes.append(id)

        # print newshapes
        fPosition = FindPosition(m2)

        pos = fPosition.findPosition(newshapes)
        print pos
        return pos

ma = Main()
ma.getPosition()