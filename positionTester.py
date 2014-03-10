import picamera
import time
import RPI.software.shapeRecognition as sr

sf = sr.Analyzer()
path = "/home/pi/zep2/output/path.jpg"
res = 250

#f = open('/home/pi/zep2/output/results.csv','w')
#f.write('hi there\n') # python will convert \n to os.linesep

def analyze():
    global sf,path,red
    i = 0
    while i < 20:
        print str(i)
        with picamera.PiCamera() as camera:
            camera.resolution = (res,res)
            camera.capture(path, "jpeg")
            
        starttime = time.time()
        found = sf.analyze(path)
        print str(time.time() - starttime)
        print str(found)
        i += 1
    return found


def takePics():
    global res
    path = "/home/pi/zep2/output/"
    i = 0
    while i < 20:
        print str(i)
        with picamera.PiCamera() as camera:
            camera.resolution = (res,res)
            camera.capture(path + str(i) + ".jpg", "jpeg")
            
        raw_input("go?")
        print "gone!"
        i += 1
    return found

takePics()
#analyze()
    
#import RPI.grid
#grid =  RPI.grid.Grid()
    
#while(True):
#    listOfShapes = analyze()
#    for (shape,colour,x,y) in listOfShapes:
        
