import RPi.GPIO as GPIO
import time
import math


class cycleTimer(object):
	
	def __init__(self, initTime, cycleLength,actionsPerCycle):

		self.actionTime=cycleLength/actionsPerCycle
		self.cycleLength=cycleLength
		self.initTime=initTime
		self.actionsPerCycle=actionsPerCycle
		
		
	def cycleNum(self):

		self.currentTime=time.time()
		self.cyclePercent=(self.currentTime-self.initTime)/self.cycleLength
		self.cyclePercent=self.cyclePercent-math.floor(self.cyclePercent)
		self.cycleTime=self.cyclePercent*self.cycleLength
		self.cycleNumber=math.floor(self.cycleTime/self.actionTime)
		return self.cycleNumber

	def strobe(self):

		self.currentTime=time.time()
		self.cyclePercent=(self.currentTime-self.initTime)/self.cycleLength
		self.cyclePercent=self.cyclePercent-math.floor(self.cyclePercent)
                
		if self.cyclePercent > .5:
			#print(self.cyclePercent)
			self.cyclePercentMod=(100-self.cyclePercent*100)/100
			#print(self.cyclePercentMod)
			#print((100-self.cyclePercent*100)/100)
		else:
			self.cyclePercentMod=self.cyclePercent
		#print(self.cyclePercent)
		self.cycleTime=self.cyclePercentMod*self.cycleLength
		#print(self.cyclePercent)
		self.cycleNumber=math.floor(self.cycleTime/self.actionTime)
		return self.cycleNumber*2

class callMeBack(object):

	def __init__(self):
		self.flag=0

	def myCallBack(self,other):
		self.flag=1
		print(other)
	def checkFlag(self):
		return flag

CMB=callMeBack()
GPIO.setmode(GPIO.BCM)

buttonInput=12
ledNumbers=(18,20,21,22,23,24,25)


GPIO.setup(buttonInput, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(ledNumbers, GPIO.OUT)
cycleLength=.3

Timer1=cycleTimer(time.time(), cycleLength,len(ledNumbers))

GPIO.add_event_detect(buttonInput, GPIO.RISING, callback=CMB.myCallBack, bouncetime=300)

try:
	while True:
		whichLED=Timer1.cycleNum()

		offLEDs=[x for x in ledNumbers if x != ledNumbers[whichLED]] #List Comprehension
		GPIO.output(offLEDs, GPIO.LOW)
		GPIO.output(ledNumbers[whichLED], GPIO.HIGH)
		
		if(CMB.checkFlag == 1):
			GPIO.output(ledNumbers, GPIO.LOW)
			if whichLED == math.floor(len(ledNumbers)/2):
				GPIO.output(ledNumbers[whichLED], GPIO.HIGH)
				break

	strobe1=cycleTimer(time.time(), 3,100)
	timer2=cycleTimer(time.time(), 12,2)
	GPIO.cleanup()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(22, GPIO.OUT)
	dutyCyclePast=-1

	pwm = GPIO.PWM(22, 100)
	pwm.start(25)
	while True:
		if timer2.cycleNum()==1:
			break



except:
	GPIO.cleanup()
	raise






#pwm = GPIO.PWM(18, 1000)
#pwm.start(50)

GPIO.cleanup()





















