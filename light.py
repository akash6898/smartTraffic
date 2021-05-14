import os
import pyrebase
import time
import RPi.GPIO as GPIO

config = {
    "apiKey": "AIzaSyAR91-Gy8PU2Tb7BHA-7MdVMLYlOKPXiDI",
    "authDomain": "smart-traffic-system-2f696.firebaseapp.com",
    "databaseURL": "https://smart-traffic-system-2f696-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "smart-traffic-system-2f696",
    "storageBucket": "smart-traffic-system-2f696.appspot.com",
    "messagingSenderId": "178119461351",
    "appId": "1:178119461351:web:d6fddbd516cb3b8f89d542",
    "measurementId": "G-VRPP7ZL38N"
};

lane1 = 0;
lane2 = 0;
lane3 = 0;
lane4 = 0;

firebase = pyrebase.initialize_app(config)


database = firebase.database()
def getData():
	data = database.child("Data").get().val()
	lane1 = data['lane1']
	lane2 = data['lane2']
	lane3 = data['lane3']
	lane4 = data['lane4']


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
red = [0,1,1,1]
yellow = [0,0,0,0]
green  = [1,0,0,0]


r1=15
y1=13
g1=11



r2=22
y2=18
g2=16



r3=37
y3=35
g3=33



r4=40
y4=38
g4=36

redLed = [r1,r2,r3,r4]
yellowLed = [y1,y2,y3,y4]
greenLed = [g1,g2,g3,g4]


GPIO.setup(r1,GPIO.OUT)
GPIO.setup(y1,GPIO.OUT)
GPIO.setup(g1,GPIO.OUT)
GPIO.setup(r2,GPIO.OUT)
GPIO.setup(y2,GPIO.OUT)
GPIO.setup(g2,GPIO.OUT)
GPIO.setup(r3,GPIO.OUT)
GPIO.setup(y3,GPIO.OUT)
GPIO.setup(g3,GPIO.OUT)
GPIO.setup(r4,GPIO.OUT)
GPIO.setup(y4,GPIO.OUT)
GPIO.setup(g4,GPIO.OUT)



#greenTime1= 5
#greenTime2= 10
#greenTime3 = 15
#greenTime4 = 20
Time1=0
Time2=0
Time3=0
Time4=0
def offexecpt(index,temp):
    if(temp == 1):
        red[index]=1
        yellow[index]=0
        green[index]=0
        GPIO.output(redLed[index],GPIO.HIGH)
        GPIO.output(yellowLed[index],GPIO.LOW)
        GPIO.output(greenLed[index],GPIO.LOW)
    elif(temp == 2):
        red[index]=0
        yellow[index]=1
        green[index]=0
        GPIO.output(redLed[index],GPIO.LOW)
        GPIO.output(yellowLed[index],GPIO.HIGH)
        GPIO.output(greenLed[index],GPIO.LOW)
    elif(temp == 3):
        red[index]=0
        yellow[index]=0
        green[index]=1
        GPIO.output(redLed[index],GPIO.LOW)
        GPIO.output(yellowLed[index],GPIO.LOW)
        GPIO.output(greenLed[index],GPIO.HIGH)


curr_lane =0
laneTime = [5,5,5,5]
clock=0
database.child("Data").update({'curr_Lane' : curr_lane + 1})
queue = [0,0,0,0]
while True:
    data = database.child("Data").get().val()
    lane1 = data['lane1']
    lane2 = data['lane2']
    lane3 = data['lane3']
    lane4 = data['lane4']
    lane = [lane1,lane2,lane3,lane4]
    max_index = lane.index(max(lane))
    min_index = lane.index(min(lane))
    if((max_index - min_index) != 0):
    	if(queue[max_index] == 0):
    		laneTime[max_index] = laneTime[max_index] + 3
    		laneTime[(max_index+1)%4] = laneTime[(max_index+1)%4] -1
    		laneTime[(max_index+2)%4] = laneTime[(max_index+2)%4] -1
    		laneTime[(max_index+3)%4] = laneTime[(max_index+3)%4] -1
    		queue[max_index] =1
    os.system("clear")
    clock = clock +1  
    if(curr_lane == 0):
        Time1 = laneTime[0] - clock
        Time2 = laneTime[0] - clock
        Time3 = laneTime[0] + laneTime[1] - clock
        Time4 = laneTime[0] + laneTime[2] + laneTime[3] - clock
        if(clock<laneTime[0]):
            offexecpt(0,3)
            offexecpt(1,1)
            offexecpt(2,1)
            offexecpt(3,1)
        elif(clock <= laneTime[0]):
            offexecpt(0,3)
            offexecpt(1,2)
            offexecpt(2,1)
            offexecpt(3,1)
            curr_lane = 1
            database.child("Data").update({'curr_Lane':curr_lane+1})
            clock =0        
    elif(curr_lane == 1):
        Time1 =  laneTime[1] +laneTime[2]  + laneTime[3]- clock
        Time2 = laneTime[1] - clock
        Time3 = laneTime[1] - clock
        Time4 = laneTime[1] + laneTime[2] - clock
        if(clock<laneTime[1]):
            offexecpt(0,1)
            offexecpt(1,3)
            offexecpt(2,1)
            offexecpt(3,1)
        elif(clock <= laneTime[1]):
            offexecpt(0,1)
            offexecpt(1,3)
            offexecpt(2,2)
            offexecpt(3,1)
            curr_lane = 2
            database.child("Data").update({'curr_Lane':curr_lane+1})
            clock = 0
    elif(curr_lane == 2):
        Time1 = laneTime[0] - clock +laneTime[3] 
        Time2 = laneTime[1] - clock +laneTime[2] +laneTime[3]
        Time3 = laneTime[3]  - clock
        Time4 = laneTime[3] - clock
        if(clock<laneTime[2]):
            offexecpt(0,1)
            offexecpt(1,1)
            offexecpt(2,3)
            offexecpt(3,1)
        elif(clock <= laneTime[2]):
            offexecpt(0,1)
            offexecpt(1,1)
            offexecpt(2,3)
            offexecpt(3,2)
            curr_lane = 3
            database.child("Data").update({'curr_Lane':curr_lane+1})
            clock = 0
    elif(curr_lane == 3):
        Time1 = laneTime[3] - clock
        Time2 = laneTime[0] - clock +laneTime[3]
        Time3 = laneTime[0] + laneTime[1] - clock +laneTime[3]
        Time4 = laneTime[3]  - clock
        if(clock<laneTime[3]):
            offexecpt(0,1)
            offexecpt(1,1)
            offexecpt(2,1)
            offexecpt(3,3)
        elif(clock <= laneTime[3]):
            offexecpt(0,2)
            offexecpt(1,1)
            offexecpt(2,1)
            offexecpt(3,3)
            curr_lane = 0
            database.child("Data").update({'curr_Lane':curr_lane+1})
            clock =0               


    print("\tRoad1\tRoad2\tRoad3\tRoad4")
    print("\n")
    print("\t " +str(Time1) +"\t " +str(Time2)  +"\t " +str(Time3)  +"\t " +str(Time4))
    print("\n")
    print("Red\t",end=" ")
    for i in range(len(red)):
        print(str(red[i]) +"\t", end =" ")

    print("\n\n")
    print("Yellow\t",end=" ")
    for j in range(len(yellow)):
        print(str(yellow[j])+"\t", end =" ")

    print("\n\n")
    print("Green\t",end=" ")
    for k in range(len(green)):
        print(str(green[k])+"\t", end =" ")
    print("")
    time.sleep(1.5)    
