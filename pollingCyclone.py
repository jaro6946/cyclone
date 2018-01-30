import RPi.GPIO as GPIO
import time
import math

GPIO.cleanup()

class cycleTimer(object):
	
	def __init__(self, initTime, cycleLength,actionsPerCycle):
		self.actionTime=cycleLength/actionsPerCycle
		self.cycleLength=cycleLength
		self.initTime=initTime
		self.actionsPerCycle=actionsPerCycle
		
		
	def cycleNum(self):

		self.currentTime=time.time()
		self.cyclePer=(self.currentTime-self.initTime)/self.cycleLength
		self.cycleTime=(self.cyclePer-math.floor(self.cyclePer))*self.cycleLength
		self.cycleNumber=math.floor(self.cycleTime/self.actionTime)
		return self.cycleNumber




GPIO.setmode(GPIO.BCM)

buttonInput=13
ledNumbers=(19,20,21,22,23,24,25)


GPIO.setup(buttonInput, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(ledNumbers, GPIO.OUT)
cycleLength=.3

Timer1=cycleTimer(time.time(), cycleLength,len(ledNumbers))

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
		





#pwm = GPIO.PWM(18, 1000)
#pwm.start(50)

GPIO.cleanup()





















