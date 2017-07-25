import speech_recognition as sr
import subprocess
import os
import os.path
from urllib import quote_plus
from PIL import Image, ImageTk
import Tkinter as tk
import threading
from multiprocessing import Process

from picamera import PiCamera
from time import sleep

# set up IBM account
IBM_USERNAME = "Your IBM USER NAME"
IBM_PASSWORD = "Your IBM USER PASSWORD"

# build speeck recognition model and obtain audio from the microphone
r = sr.Recognizer()

def show(f):
    '''
    Display image on screen center
    '''
    f=f[0]
    img = Image.open(f)
    w,h = img.size
    if w == 1920:
        w = w/3*2
        h = w/3*2

    root = tk.Tk()
    canvas = tk.Canvas(root, width=w, height=h)
    canvas.pack()
    tk_img = ImageTk.PhotoImage(img)
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = ws/2 - w/2
    y = hs/2 - h/2
    root.geometry("+{}+{}".format(x,y))
    canvas.create_image(w/2, h/2, image=tk_img)
    root.mainloop()

def t2s(t):
    '''
    Use IBM Watson text to speech to read out any text
    '''
    t = quote_plus(t)
    if os.path.exists("./{}.wav".format(t)):
        subprocess.call("aplay {}.wav".format(t),shell=True)
        return
    curl = 'curl -X GET -u "IBM USER NAME":"IBM PASSWORD" --output {}.wav "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize?accept=audio/wav&text={}&voice=en-US_AllisonVoice"'.format(t,t)
    subprocess.call(curl,shell=True)
    subprocess.call("aplay {}.wav".format(t),shell=True)

FNULL = open(os.devnull,'w')
with sr.Microphone(device_index=2) as source:
    t = "Hello world, I am text imager. How can I help you?"
    t2s(t)
    
    print("I am ready to paint")
    audio = r.listen(source)
try:
    #Use IBM watson to understand speech
    message_0 = "IBM Watson heard _" + r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
    t = message_0
    t2s(t)    
    keyword = ["see","sea","c","what","do","you","draw","this","image","can"]
    for key in keyword:
      if key in message_0: #or True:
        t = "Let me take a look"
        t2s(t)       
        with PiCamera() as cam:
            cam.start_preview(fullscreen=False, window = (200, 150, 1440, 960))
            sleep(3)
            with open('img.jpg', 'wb') as f:
                cam.capture(f)

        s = ["./img.jpg"]
        t1 = Process(target=show, args=(s,))
        t1.start()    
        waitmsg = "OK, I am painting now"
        t = waitmsg
        t2s(t)
        # calling server to obtain generated images and recognized text                 
        subprocess.call("curl -X POST -F 'file=@./img.jpg' -F 'type=1' http://9.41.71.147:5000/post/666 > output.jpg" , shell=True)
        subprocess.call("curl -X POST -F 'type=1' http://9.41.71.147:5000/getimg/ > text.txt", shell=True)
        textfile=open("text.txt","r")
        introread="This is what I just painted"
        t2s(introread)       
        textread=textfile.read()
        t2s(textread)        
        break 
except sr.UnknownValueError:
    message_2 = "IBM Speech to Text could not understand audio"
    t2s(message_2)
    print(message_2)
    exit(0)
except sr.RequestError as e:
    message_3 = "Could not request results from IBM Speech to Text service; {0}".format(e)
    subprocess.call(["espeak","-s 120 -v en ", message_3], stdout=FNULL, stderr=subprocess.STDOUT)
    print("Could not request results from IBM Speech to Text service; {0}".format(e))
    exit(0)
try:
    s = ["./output.jpg"]
    t2 = Process(target=show, args=(s,))
    t2.start()
    t = "How do you like it?"
    t2s(t)
except:
    t = "I am having problem getting things from image"
    t2s(t)
