import time
import os


def generate_temp_folder():
    tempFolder = "tempFiles/" + str(time.time())
    os.mkdir(tempFolder)
    return tempFolder
