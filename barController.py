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

# and some help from the capitalist pigs at O'Reilly

import time

def update(ingredient, angle):
    servoStr = "%u=%u\n" % (ingredient, angle)

    with open("/dev/servoblaster", "wb") as f:
        f.write(bytes(servoStr, 'UTF-8'))
    
def pour(instructions):
    turnTime = 1 # seconds for which servo turns either way
    assert(type(instructions) == list)
    assert(len(instructions) == 5)
    for x in range(1, 5):
        assert(type(instructions[x]) == float)
        assert(instructions[x] >= 0)
        assert(instructions[x] <= 1)
    volume = instructions[0]
    servos = [1, 2, 3, 4] # channels 17, 18, 21, 22
    for x in list(range(1, 5)):
        update(x, 90)
    flowRate = 2 # seconds per milliliter
    amounts = [(float(volume) * instructions[x]) for
               x in list(range(1, len(instructions)))]
    flowTimes = [(flowRate * amount) for amount in amounts]
    for i in list(range(len(flowTimes))):
        update(i+1, 180)
        time.sleep(turnTime)
        update(i+1, 90, pwm)
        time.sleep(flowTimes[i])
        update(i+1, 0, pwm)
        time.sleep(turnTime)
        update(i+1, 90, pwm)
