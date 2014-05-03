from COMMON.enum import Enum
from pi.grid import GRID

import GUI.gridTest as gridTest
class Axis(Enum):
  x = 1
  y = 2
  z = 3
    
################################################

import RPI.hardware.motor as motor

   #//TODO PID's for all axis. 
class Vector3:
    
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
    def add(self,other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def inverse(self):
        return Vector3(-self.x, -self.y, -self.z)
    
    def toString(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z) 
    
    def scale(self,i):
        return Vector3(i * self.x , i * self.y, i * self.z)
    
    #Get a specific axis.
    def getAxis(self,axis):
        if axis == Axis.x:
            return self.x
        elif axis == Axis.y:
            return self.y
        elif axis == Axis.z:
            return self.z
        else:
            return None
        
    #Set a specific axis.
    def setAxis(self,axis, val):
        if axis == Axis.x:
            self.x = val
        elif axis == Axis.y:
            self.y = val
        elif axis == Axis.z:
            self.z = val
        else:
            pass
        
            
    
    def fst(self):
        return self.x
    
    def snd(self):
        return self.y
    
    def thrd(self):
        return self.z
    
    def asArray(self):
        return [self.x,self.y,self.z]
           
           
import time

class FakeEnvironment:
    
    def __init__(self):
        self.pos = Vector3(0,0,0)
        self.speed = Vector3(0,0,0)
        self.force = Vector3(0,0,0)
        #pull of gravity somewhere around 1 m/s^2.
        import random
        self.mass = random.gauss(1,0.05)
        print("mass of the fake zeppelin is " + str(self.mass))
        self.gravity = Vector3(0,0,self.mass * 9.81)
        self.lift = Vector3(0,0,self.mass * 8)
    
    
    def update(self):
        lastTime = time.time()
        while True:
            #print(self.pos.toString() + " | " + self.force.toString())
            timeNow = time.time()
            scale = timeNow - lastTime
            lastTime = timeNow
            
            #simon
            actuatedForce = self.force.add(self.gravity.inverse()).add(self.lift)
            self.speed = self.speed.add(actuatedForce.scale(scale))
            self.pos = self.pos.add(self.speed)
            
            #if(self.pos.thrd() < 0):
             #   self.pos = 0
              #  self.vSpeed = 0
            #else:
            #    self.vSpeed += force/self.mass
            #    self.height += self.vSpeed
            time.sleep(0.033)
            

import thread
import pi.ZepListener as zeplistener
 
class FakeZeppelin:
    
    def __init__(self):
        self.height = 0
        self.zepListener = zeplistener.zepListener(self)
        thread.start_new(self.zepListener.start, ())
        time.sleep(1)
        self.motorOffset = 50
        self.fe = FakeEnvironment()
        self.motorX = motor.FakeMotor(self.fe,Axis.x)
        self.motorY = motor.FakeMotor(self.fe,Axis.y)
        self.motorZ = motor.FakeMotor(self.fe,Axis.z)
        #self.altimeter = ds.FakeDistanceSensor2(self.fe)
        self.loadGrid("C:\Users\simon\Documents\GitHub\PENOROOD\OTHER\grid25-04.csv")
        #old self.fe.force = Vector3(0.1,0.2,0)
        #new SimonOveride
        self.setMovementZeppelin((2,3));
        #print(self.fe.force.toString())
        thread.start_new_thread(self.fe.update, ())
        #print(self.fe.force.toString())
        #self.pid = PID(0.2,0.1,5)
        self.camera = None
        self.goal = (250,150)
        self.targets = [] # tuple = (x,y,boolean)
        while True:
            print("here")
            self.updateGoal()
            self.setMovementZeppelin(self.updateGoalDirection())
            self.zepListener.pushPosition(self.getPositionXY())
            time.sleep(0.5)

    def setPosition(self,x,y,z):
        self.fe.pos = Vector3(x,y,z)
        
    def getPosition(self):
        return self.fe.pos

    def getPositionXY(self):
        return (int(self.fe.pos.x),int(self.fe.pos.y))
    
    def getSpeed(self):
        return self.fe.speed
        
    def getZeppelinPositionFromShapes(self):
        pos = self.grid.calculatePositionFromShapes()
        return pos

    #not used atm
    def updateTargets(self):
        for i in range(len(self.targets)):
            tup = self.targets[i]
            if(tup[2] == True):
                self.goal = (tup[0], tup[1])

    def updateGoal(self):
        currentpos = (self.fe.pos.x, self.fe.pos.y)
        goals = [ (250, 150), (0,0)]
        if( (((currentpos[0] > (self.goal[0]-2))) and ((currentpos[0] < (self.goal[0]+2)))) and (((currentpos[1] > (self.goal[1]-2))) and ((currentpos[1] < (self.goal[1]+2))))):
            if(self.goal == goals[0]):
                self.goal = goals[1]
            else:
                self.goal = goals[0]


    def updateGoalDirection(self):
        currentpos = (self.fe.pos.x, self.fe.pos.y)
        if(currentpos[0] == self.goal):
            self.goal = (-1,-1)
            return(0,0)
        else:
            direction_x = self.goal[0] - currentpos[0];
            direction_y = self.goal[1] - currentpos[1];
            return(direction_x, direction_y)

    def setMovementZeppelin(self,direction):
        if(direction == (-1,-1)):
            self.fe.force = Vector3(0,0,0)
            self.fe.speed = Vector3(0,0,0)
        else:
            if(abs(direction[0])>abs(direction[1])):
                xf = direction[0]/abs(direction[0])
                yf = direction[1]/abs(direction[0])
            elif(direction == (0,0)):
                xf = 0
                yf = 0
            else:
                xf = direction[0]/abs(direction[1])
                yf = direction[1]/abs(direction[1])
            #self.fe.force = Vector3(xf/5,yf/5,0)
            self.fe.speed = Vector3(xf*abs(direction[0])/300,yf*abs(direction[1])/300,0)
        
        
    def acceptMovementFromListener(self,movement):
        if(movement == 1):
            self.goForward()
        elif(movement == 2):
            self.goRight()
        elif(movement == 3):
            self.goBackward()
        else:
            self.goLeft()
        
    def goRight(self):
        self.fe.force = Vector3(1,0,0)
        
    def goLeft(self):
        self.fe.force = Vector3(-1,0,0)
        
    def goForward(self):
        self.fe.force = Vector3(0,-1,0)
        
    def goBackward(self):
        self.fe.force = Vector3(0,1,0)
        
    def stop(self):
        self.fe.speed = Vector3(0,0,0)

    def loadGrid(self, path):
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
        self.grid = gridTest.GRID(number_of_columns, number_of_rows)
        self.grid.initiate(init_string);