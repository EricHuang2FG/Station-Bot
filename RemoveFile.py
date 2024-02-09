import os, time, threading

def removeFile():
    filePath = "stations.txt"
    while True:
        if os.path.exists(filePath):
            os.remove("stations.txt")
            print("\nTLE sets removed.")
        time.sleep(3600)

def periodicRemoval():
    period = threading.Thread(target = removeFile)
    period.start()