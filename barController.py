# barController.py module
# made by rajat mehndiratta (github/rajatmehndiratta) @ HackIllinois s'15
# as part of project Dr. Dre's Mix Machine

# USES SERVOBLASTER

# (https://github.com/richardghirst/PiBits/tree/master/ServoBlaster)

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

# LED mode now

import time
import RPi.GPIO as GPIO

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(9, GPIO.OUT)
    GPIO.setup(10.GPIO.OUT)

def update(ingredient, angle):
    servoStr = "%u=%u\n" % (ingredient, angle)

    with open("/dev/servoblaster", "wb") as f:
        f.write(bytes(servoStr, 'UTF-8'))
    
def pour(instructions):
    setup()
    turnTime = 1 # seconds for which servo turns either way
    assert(type(instructions) == list)
    assert(len(instructions) == 5)
    for x in range(1, 5):
        assert(type(instructions[x]) == float)
        assert(instructions[x] >= 0)
        assert(instructions[x] <= 1)
    volume = instructions[0]
    servos = [1, 2, 3, 4] # channels 17, 18, 21, 22
    ledPins = [7,8,9,10]
    # for x in list(range(1, 5)):
        # update(x, 150)
    flowRate = 2 # seconds per milliliter
    amounts = [(float(volume) * instructions[x]) for
               x in list(range(1, len(instructions)))]
    flowTimes = [(flowRate * amount) for amount in amounts]
    for i in list(range(len(flowTimes))):
        GPIO.output(ledPins[i], True)
        time.sleep(flowTimes[i])
        GPIO.output(ledPins[i], False)
