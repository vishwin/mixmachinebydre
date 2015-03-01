#!/usr/bin/python3.4
import threading
import atexit
from flask import Flask
from barController import pour

POOL_TIME = 2 #Seconds

jobs = []
jobsLock = threading.Lock()
jobRunner = threading.Thread()

def create_app():
    app = Flask(__name__)

    def interrupt():
        global jobRunner
        jobRunner.cancel()

    def processJobs():
        global jobs
        global jobRunner
        with jobsLock:
            if len(jobs) > 0:
                for job in jobs:
                    pour([job[0]] + job[1])
                    jobs.remove(job)

        jobRunner = threading.Timer(POOL_TIME, processJobs, ())
        jobRunner.start()

    def startProcessingJobs():
        global jobRunner
        jobRunner = threading.Timer(POOL_TIME, processJobs, ())
        jobRunner.start()

    startProcessingJobs()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app

app = create_app()

import webui.controller
