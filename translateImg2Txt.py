import subprocess

def translate(url):
    try:
        ext = (url.split("/")[-1]).split(".")[-1]
        fileName = 'dataset/original.'+ext
        subprocess.call(["wget", "-O", fileName, url])
        subprocess.call(["tesseract", fileName, "-l", "jpn", "dataset/out"])
        return "dataset/out.txt"
    except Exception as e:
        print ("Exception Error: ", e)