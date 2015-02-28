from webui import app
try:
	import RPi.GPIO as GPIO
except:
	print("Error importing RPi.GPIO")

@app.route("/")
def sup():
	return "Dr Dre's Mix Machine. No, it has nothing to do with music."
