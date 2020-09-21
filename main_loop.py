
import time
from threading import Thread


#initialisation
global liste

#test stream
liste =[0,0,2,2,2,2,0,0,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,0,2,2,2,2,1,2,0,0,1,1,1,0,0,2,2,2,2,1,2,0,0,0,0,2,2,2,2,1,2,0,0,0,0]

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

        #start application
        self.main_loop()
        
        
        

    def main_loop(self):
        while True:
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
                    print("###  Current Score: ", self.counter,"###")

                if self.state==2 or self.state==0:
                    self.last_detected_state=self.state
                    self.stopwatch=time.time()

            #Resting the counter if nobody is in the frame
            if (time.time()-self.stopwatch) > 2:
                if self.state==1:  # if nobody is in the frame reset counter
                    print("###  Reset Score   ###")
                    self.counter=0
                    self.stopwatch=time.time()

            #Checking of the finish
            if self.counter>=10:
                self.completed=True


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

if __name__ == '__main__':
    
    
    start=States()
    











