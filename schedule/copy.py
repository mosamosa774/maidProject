import subprocess
import os
os.chdir("/home/pi/maidProj/schedule/")

subprocess.call(("cp", "schedulemon.txt", "scheduletue.txt"))
subprocess.call(("cp", "schedulemon.txt", "schedulewed.txt"))
subprocess.call(("cp", "schedulemon.txt", "schedulethu.txt"))
subprocess.call(("cp", "schedulemon.txt", "schedulefri.txt"))
subprocess.call(("cp", "schedulemon.txt", "schedulesat.txt"))
subprocess.call(("cp", "schedulemon.txt", "schedulesun.txt"))

