
#!/usr/bin/env python
import modules.hardware.distSensor as Ids
import modules.lowLevelController as llcp
import os
import thread
import time

#Zeppelin class.
class Zeppelin:
    def __init__(self, simMode = "RPi", dist = None):
        dsr = Ids.DistanceReader(location = dist)
        self.llc = llcp.LowLevelController(simMode, dists = dsr)

#Check to see whether we're running on the RaspberryPi. store result in simMode
simMode = "RPi"
try:
    import RPi.GPIO as GPIO
except ImportError:
    simMode = "sim"
    print "running in simulation mode."
    
    
os.system("rm data/ds/data")
print "1"
#os.system("cat > data/ds/data")
print "2"
filelocation = "data/ds/data"
print "3"
pid = os.fork()
if pid == 0:
    #This is the child process
    os.nice(-1)
    print "Distsens on: " + str(os.getpid()) + " | priority: " + str(os.nice(0))
    dist = Ids.PriorityDistanceSensor(location = filelocation)
    #safety lock
    while(True):
        print "Line 33 passed by child = fatal!!!!!"
        time.sleep(1000)

#else this is the parent
else:
    print "main on: " + str(os.getpid()) + " | priority: " + str(os.nice(0))
    zeppelin = Zeppelin(simMode, dist = filelocation)
    #########################
    ####Initiate zeppelin####
    #########################
    
    
    ######################
    ####Server-methods####
    ######################
    
    #import Bottle: allows explicit linking of a URL request (GET, POST, ...) to python methods (see below)
    from modules.srv.bottle import *
    
    #Homepage.
    @route('/')
    def home():
        return static_file("index.html",root="modules/srv/")
    
    #HTML must be loaded explicitly from the root folder.
    @route('/<filename:re:.*\.html>')
    def send_html(filename):
        return static_file(filename, root='modules/srv/')
    
    #Images must be loaded explicitly from the images folder.
    @route('/images/<filename:re:.*\.png>')
    def send_image(filename):
        return static_file(filename, root='modules/srv/images/', mimetype='image/png')
    
    @route('/stream')
    def stream():
        return static_file("cam.png", "/data/cam/", mimetype='image/png')
    
    #CSS, must be loaded from the css folder.
    @route('/css/<filename:re:.*\.css>')
    def send_css(filename):
        return static_file(filename, root='modules/srv/css/', mimetype='text/css')
    
    @route('/scripts/<filename:re:.*\.js>')
    def send_javascript(filename):
        return static_file(filename, root='modules/srv/scripts/', mimetype='text/javascript')
    
    """
    @route('/height')
    def send_height():
        global zeppelin
        return str(zeppelin.llc.altimeter.getHeight())
    """
    
    @route('/lift')
    def send_lift():
        global zeppelin
        return str(zeppelin.llc.lift.thrust)
    
    @route('/info')
    def send_info():
        global zeppelin
        global simMode
        if simMode == "sim":
            Xlift = str(zeppelin.llc.lift.thrust)
            Xheight = str(zeppelin.llc.altimeter.getHeight())
            return {'lift':Xlift,'height':Xheight}
        else:  #Rpi mode
            Xlift = str(zeppelin.llc.lift.thrust)
            Xthrust = str(zeppelin.llc.thrust.thrust)
            Xrudder = str(zeppelin.llc.rudder.thrust)
            Xheight = str(zeppelin.llc.altimeter.getHeight())
            return {'lift': Xlift,'thrust': Xthrust, 'rudder': Xrudder, 'height': Xheight}
        
    @get('/cam')
    def send_camimg():
        global simMode
        global zeppelin
        if simMode == "RPi":
            pass
            return str(zeppelin.llc.camera.click())
        else:
            pass
            return "images/test.png"
        
    @post('/setheight')
    def set_height():
        global zeppelin
        try: 
            nheight = float(request.forms.get('dHeight'))
        except ValueError:
            return
        zeppelin.llc.setDesiredHeight(nheight)
        
    @post('/setmotors')
    def set_motors():
        global zeppelin
        try:
            nLift = float(request.forms.get('lift'))
            nThrust = float(request.forms.get('thrust'))
            nRudder = float(request.forms.get('rudder'))
        except ValueError:
            pass
        zeppelin.llc.lift.setThrust(nLift)
        zeppelin.llc.thrust.setThrust(nThrust)
        zeppelin.llc.rudder.setThrust(nRudder)
        
        
        
    mode = raw_input("Type 'auto' for automatic mode\n Type anything else for controlled mode\n> ")
    #start zeppelin background tasks. Otherwise mode stays RPi or sim.
    if mode == "auto":
        zeppelin.llc.start()
    #Start the server
    run(host='localhost', port=54322, debug=True)



