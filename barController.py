# barController.py module
# made by rajat mehndiratta (github/rajatmehndiratta) @ HackIllinois s'15
# as part of project Dr. Dre's Mix Machine

###########################################


#@TODO:

# TEST ON PI TO MAKE SURE IT WORKS

##########################################

# U S A U S A U USAUSAUSAUSAUSAUSAUSAUSAUSA
#  U S A U S U 
# U S A U S A U USAUSAUSAUSAUSAUSAUSAUSAUSA
#  U S A U S U
# U S A U S A U USAUSAUSAUSAUSAUSAUSAUSAUSA
#  U S A U S U
# U S A U S A U USAUSAUSAUSAUSAUSAUSAUSAUSA
#  
# USAUSAUSAUSAUSAUSAUSAUSAUSAUSAUSAUSAUSAUS
#
# USAUSAUSAUSAUSAUSAUSAUSAUSAUSAUSAUSAUSAUS
#
# USAUSAUSAUSAUSAUSAUSAUSAUSAUSAUSAUSAUSAUS

# M A D E    W I T H
# CAFFEINE + FREEDOM

# and some help from the capitalist pigs at O'Reilly

import RPi.GPIO as GPIO
import time

def setup(servos):
    pwm = [] * len(servos)
    GPIO.setmode(GPIO.BCM)
    for x in range(len(servos)):
        GPIO.setup(servos[x], GPIO.OUT)
        pwm[x] = GPIO.PWM(servos[x], 100)
        pwm[x].start(5)

def update(ingredient, angle):
    duty = float(angle) / 10.0 + 2.5
    pwm[index-1].ChangeDutyCycle(duty)

def pour(instructions):
    openPos = 0
    closedPos = 90
    assert(type(instructions) == list)
    assert(len(instructions) == 5)
    for x in range(1, 5):
        assert(type(instructions[x]) == float)
        assert(instructions[x] >= 0)
        assert(instructions[x] <= 1)
    volume = instructions[0]
    servos = [18, 19, 20, 21]
    setup(servos)
    for x in range(1, 5):
        update(x, 90)
    flowRate = 2 # seconds per milliliter
    amounts = [(float(volume) * instructions[x]) for
               x in range(1, len(instructions))]
    flowTimes = [flowRate * amount for amount in amounts]
    for i in len(flowTimes):
        update(i+1, 0)
        time.sleep(flowTimes[i])
        update(i+1, 90)





