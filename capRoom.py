import subprocess

def takeCapture():
    subprocess.call(["fswebcam","-r","640x480","dataset/cap.jpg"])
    return "dataset/cap.jpg"