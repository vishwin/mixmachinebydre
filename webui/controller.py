from webui import app
from flask import request, render_template
try:
	import RPi.GPIO as GPIO
except:
	print("Error importing RPi.GPIO")

@app.route("/")
def sup():
	return "Dr Dre's Mix Machine. No, it has nothing to do with music."

#@app.route("/ingredients", methods=['POST'])

#@app.route("/mix", methods=['POST'])

#@app.route("/lucky")

#@app.route("/rate", methods=['GET'])

#@app.route("/firehose")
#def configureGPIO():
	
