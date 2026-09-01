import json
import time


def readTasks():
    tasks = []
    timeSinceLastInstance = 0

    timeIntervals = {}

    try:
        with open("tasks", "r") as f:
            data = json.load(f)
            timeLoaded = data["TimeLoaded"]
            
            timeNow = int(time.time())
            timeSinceLastInstance = timeNow - timeLoaded

            for item in data["Tasks"]:
                t = item["Time"] - timeSinceLastInstance
                taskEntry = [item["Subject"], item["Topic"], t, item["Stage"]]

                tasks.append(taskEntry)

            timeIntervals = data["TimeIntervals"]

    except FileNotFoundError:
        print("!")
        tasks = []
        timeIntervals = {
                "1" : 600,
                "2" : 10800,
                "3" : 86400,
                "4" : 172800,
                "5" : 604800
        }

    
    return tasks, timeIntervals

tasks, timeIntervals = readTasks()

def setTimeIntervals(times):
    global timeIntervals
    timeIntervals = times

def updateTimeIntervals():
    return timeIntervals    

def saveTasks(tasks, timeIntervals):
    with open("tasks", "w") as f:

        data = {
            "TimeLoaded" : int(time.time()),
            "Tasks" : [],
            "TimeIntervals" : timeIntervals
        }

        for task in tasks:
            taskData = {
                "Subject" : task.subject,
                "Topic" : task.topic,
                "Time" : task.timePassed,
                "Stage" : task.stage
            }

            data["Tasks"].append(taskData)

        json.dump(data, f)
