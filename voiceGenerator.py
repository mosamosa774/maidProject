import subprocess

def callVoice(str):
    with open('dataset/inp.txt',mode='w') as f:
        f.write(str)
    args = ["open_jtalk","-x","/var/lib/mecab/dic/open-jtalk/naist-jdic","-m","/usr/share/hts-voice/mei/mei_normal.htsvoice","-r","1.0","-ow","dataset/voice.wav","dataset/inp.txt"]
    subprocess.call(args)
    subprocess.call(["aplay","dataset/voice.wav"])