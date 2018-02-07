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

class risingEdge(object):
	def __init__(self):
		self.signalPast=0

	def checkForEdge(self,signal):
		self.signal=signal
		
		if self.signal==1+self.signalPast:
			self.signalPast=self.signal
			return True
		else:
			self.signalPast=self.signal
			return False

GPIO.setmode(GPIO.BCM)

buttonInput=12
ledNumbers=(18,20,21,22,23,24,25)


GPIO.setup(buttonInput, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledNumbers, GPIO.OUT)

cycleLength=2

Timer1=cycleTimer(time.time(), cycleLength,len(ledNumbers))
checkEdge=risingEdge()

try:
	while True:
		whichLED=Timer1.cycleNum()

		offLEDs=[x for x in ledNumbers if x != ledNumbers[whichLED]] #List Comprehension
		GPIO.output(offLEDs, GPIO.LOW)
		GPIO.output(ledNumbers[whichLED], GPIO.HIGH)
		
		if(checkEdge.checkForEdge(GPIO.input(buttonInput)) == 1):
			print("hell ya")
			time.sleep(.01)
			if whichLED == 4:
				GPIO.output(ledNumbers, GPIO.LOW)
				break

	timer2=cycleTimer(time.time(), 12,2)
	GPIO.cleanup()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(22, GPIO.OUT)

	pwm = GPIO.PWM(22, 100)
	pwm.start(25)
	
	while timer2.cycleNum()<1:
		pass #pass does nothing, but python requirws a place holder in this instance

except:
	GPIO.cleanup()
	raise

GPIO.cleanup()





















