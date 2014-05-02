import RPI.software.recognition.main as imp
import picamera

path = "/home/pi/zep2/output/path.jpg"
res = 250

with picamera.PiCamera() as camera:
        camera.resolution = (res,res)
        camera.capture(path, "jpeg")

c = imp.main()

c.setImage(path)

c.calibrate()

print str(c.shape.blue)
print str(c.shape.green)
print str(c.shape.red)
print str(c.shape.white)
print str(c.shape.yellow)