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
			self.cyclePecent=1-self.cyclePercent
		self.cycleTime=self.cyclePercent*self.cycleLength
		self.cycleNumber=math.floor(self.cycleTime/self.actionTime)
		return self.cycleNumber*2



GPIO.setmode(GPIO.BCM)

buttonInput=13
ledNumbers=(19,20,21,22,23,24,25)


GPIO.setup(buttonInput, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(ledNumbers, GPIO.OUT)
cycleLength=.3

Timer1=cycleTimer(time.time(), cycleLength,len(ledNumbers))
try:
	while True:
		whichLED=Timer1.cycleNum()

		offLEDs=[x for x in ledNumbers if x != ledNumbers[whichLED]] #List Comprehension
		GPIO.output(offLEDs, GPIO.LOW)
		GPIO.output(ledNumbers[whichLED], GPIO.HIGH)
		
		if(GPIO.input(buttonInput) == 1):
			GPIO.output(ledNumbers, GPIO.LOW)
			if whichLED == math.floor(len(ledNumbers)/2):
				GPIO.output(ledNumbers[whichLED], GPIO.HIGH)
				break

	Strobe1=cycleTimer(time.time(), 3,100)
	Timer2=cycleTimer(time.time(), 12,2)

	while True:
		dutyCycle=strobe1.strobe()
		pwm = GPIO.PWM(ledNumbers[3], 1000)
		pwm.start(dutyCycle)
		if Timer2.cycleNum()==1:
			break



except KeyboardInterrupt:
	GPIO.cleanup()
	raise






#pwm = GPIO.PWM(18, 1000)
#pwm.start(50)

GPIO.cleanup()





















