
import time
from threading import Thread
from aiy.leds import (Leds, Pattern, PrivacyLed, RgbLeds, Color)
from aiy.board import Board, Led


from picamera import PiCamera
from aiy.vision.inference import CameraInference
from aiy.vision.models import face_detection
from aiy.vision.annotator import Annotator



#initialisation
global liste
global currentState

#test stream
liste =[2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,2,2,2,2,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,0,2,2,2,2,0,0,2,2,2,2,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,0,2,2,2,2,1,2,0,0,1,1,1,0,0,2,2,2,2,1,2,0,0,0,0,2,2,2,2,1,2,0,0,0,0]
currentState=0


#test prediction Function
def update_input_stream():
    global liste
    time.sleep(0.15)
    return liste.pop()


def facedetector():
    """Face detection camera inference example."""
    global currentState
    # Forced sensor mode, 1640x1232, full FoV. See:
    # https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes
    # This is the resolution inference run on.
    with PiCamera(sensor_mode=4, resolution=(1640, 1232), framerate=30) as camera:
        #camera.start_preview()
        # Annotator renders in software so use a smaller size and scale results
        # for increased performace.
        #annotator = Annotator(camera, dimensions=(320, 240))
        scale_x = 320 / 1640
        scale_y = 240 / 1232

        # Incoming boxes are of the form (x, y, width, height). Scale and
        # transform to the form (x1, y1, x2, y2).
        def transform(bounding_box):
            x, y, width, height = bounding_box
            return (scale_x * x, scale_y * y, scale_x * (x + width),
                    scale_y * (y + height))
            
        def checkSquat(bounding_box):
            x, y, width, height = bounding_box
            #calc average y position
            avgHeight=  y+height/2
            
            if avgHeight>120:
                return 2;
            else:
                return 1;
            
            
            
            
        
        
        
        
        with CameraInference(face_detection.model()) as inference:
            for result in inference.run(None):
                faces = face_detection.get_faces(result)
                checkedFaces=[]
                for face in faces:
                    checkedFaces.append(checkSquat(transform(face.bounding_box)))
                
                if len(checkedFaces)==0:
                    currentState=0
                elif (2 in checkedFaces):
                    currentState=2
                else:
                    currentState=1  
                    
                print("CurrentState: ", currentState)
                print('#%05d (%5.2f fps): num_faces=%d' %
                    (inference.count, inference.rate, len(faces)))

        #camera.stop_preview()
    
    
    
    



states_names=["standing","empty","squat"]
class States():
    def __init__(self):
        pass

        self.state=0
        self.last_detected_state=0
        self.counter=0
        self.completed=False
        self.stopwatch=time.time()
        self.start=False
        #start application
        self.main_loop()
        
        

    def main_loop(self):
        
        with Board() as board:
            
            board.button.wait_for_press()
            print('ON')
            board.led.state = Led.ON
            self.start=True
            board.button.wait_for_release()
            print('OFF')
            board.led.state = Led.OFF




        while self.start:
            classes=currentState

            if classes ==0 and self.state!=0:
                self.standing()
            elif classes == 1 and self.state!=1:
                self.empty()
            elif classes == 2 and self.state!=2 and self.last_detected_state==0:
                self.squat()

            #Selecting a State
            if (time.time()-self.stopwatch) > 0.25:
                print("State:\t ",states_names[self.state] , "\t| [selected]")

                if self.state==2 and self.last_detected_state==0: #Squat detected
                    self.counter+=1
                    self._newSqaut(self.counter)
                    print("###  Current Score: ", self.counter,"###")

                if self.state==2 or self.state==0:
                    self.last_detected_state=self.state
                    self.stopwatch=time.time()

            #Resting the counter if nobody is in the frame
            if (time.time()-self.stopwatch) > 2:
                if self.state==1:  # if nobody is in the frame reset counter
                    print("###  Reset Score   ###")
                    self.counter=0
                    with Leds() as leds:
                        leds.pattern = Pattern.blink(500)
                        leds.update(Leds.rgb_pattern(Color.RED))
                        time.sleep(2)
                    self.stopwatch=time.time()

            #Checking of the finish
            if self.counter>=5:
                self.completed=True

                self.counter=0

                print("Completed Workout")
                with Leds() as leds:
                    leds.pattern = Pattern.blink(500)
                    leds.update(Leds.rgb_pattern(Color.GREEN))
                    time.sleep(2)


    def standing(self):
        print("State:\t ",states_names[self.state], "\t| [trying]")
        self.stopwatch=time.time()
        self.state=0
        
    def empty(self):
        print("State:\t ", states_names[self.state], "\t| [trying]")
        self.stopwatch=time.time()
        self.state=1

    def squat(self):
        print("State:\t ",states_names[self.state], "\t| [trying]")
        self.stopwatch=time.time()
        self.state=2

    def _newSqaut(self,count):
        with Leds() as leds:
            print('RGB: Solid GREEN for 1 second')
            #leds.update(Leds.rgb_on(Color.GREEN))
            #time.sleep(0.1)
            leds.update(Leds.privacy_off())
            leds.update(Leds.rgb_on((0,0,count*50)))
            time.sleep(1)


if __name__ == '__main__':
    #face_detection()
    Thread(target=facedetector).start()
    Thread(target=States).start()
    
    









