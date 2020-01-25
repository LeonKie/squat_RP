
import time
from aiy.leds import (Leds, Pattern, PrivacyLed, RgbLeds, Color)
from aiy.board import Board, Led

#initialisation

global liste

#test stream
liste =[2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,2,2,2,2,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,0,2,2,2,2,0,0,2,2,2,2,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,0,2,2,2,2,1,2,0,0,1,1,1,0,0,2,2,2,2,1,2,0,0,0,0,2,2,2,2,1,2,0,0,0,0]

#test prediction Function
def update_input_stream():
    global liste
    time.sleep(0.15)
    return liste.pop()

    

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
            classes=update_input_stream()

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
                    self.stopwatch=time.time()

            #Checking of the finish
            if self.counter>=5:
                self.completed=True

                print("Completed Workout")
                with Leds() as leds:
                    leds.pattern = Pattern.blink(500)
                    leds.update(Leds.rgb_pattern(Color.GREEN))






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
            leds.update(Leds.rgb_on((0,0,count*45)))
            time.sleep(1)




start=States()









