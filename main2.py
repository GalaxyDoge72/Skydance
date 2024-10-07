import tkinter as tk
from tkinter import filedialog
from just_playback import Playback
from tkinter import *
import math


root = tk.Tk()
root.title("Skydance Media Player")
root.geometry("640x480")
playback = Playback()

class ButtonCreator:
    def __init__(self, text, command, x, y):
        self.text = text
        self.command = command
        self.x = x
        self.y = y
    def create_button(self):
        button = tk.Button(root, text=self.text, command=self.command)
        button.place(x=self.x, y=self.y)
        return button

class LabelCreator:
    def __init__(self, content, x, y):
        self.content = content
        self.x = x
        self.y = y
    def createLabel(self):
        label = tk.Label(root, text=self.content)
        label.place(x=self.x, y=self.y)
        return label
class SliderCreator:
    def __init__(self, minVal, maxVal, orientation, x, y):
        self.minVal = minVal
        self.maxVal = maxVal
        self.orientation = orientation
        self.x = x
        self.y = y
    def createSlider(self):
        try:
            slider = tk.Scale(root, from_=self.minVal, to=self.maxVal, orient=self.orientation)
            slider.place(x=self.x, y=self.y)
            return slider
        except tk.TclError:
            print(f"Slider returned INCORRECT_ORIENTATION; {self.orientation} is not valid!")
            exit(1)

fileList = []
paused = False

def addFile():
    input = filedialog.askopenfilename()
    fileList.append(input)
    print(f"Appended file: {input}")

def getPlaylistItem(value):
    if value is None:
        mostrecent = fileList[0]
        return mostrecent
    elif type(value) != int:
        print(f"GetPlaylistItem returned INCORRECT_TYPE; expected Integer, got {type(value)}!")


def startPlayback():
    global scrubhead, paused
    if paused is True:
        playback.resume()
    else:
        track = getPlaylistItem(None)
        playback.load_file(track)
        tracklength = playback.duration
        scrubhead = SliderCreator(minVal=0, maxVal=tracklength, orientation="horizontal", x=250, y=250).createSlider()
        playback.play()

def pausePlayback():
    playback.pause()
    global paused
    paused = True



## Buttons ##
file_button = ButtonCreator("Load file...", addFile, x=50, y=50).create_button()
playButton = ButtonCreator("Play", startPlayback, x=50, y=75).create_button()
pauseButton = ButtonCreator("Pause", pausePlayback, x=85, y=75).create_button()

def updateScrubhead():
    try:
        playbackvalue = math.floor(playback.curr_pos)
        scrubhead.set(playbackvalue)
        root.update()
        root.after(10, updateScrubhead)
    except NameError:
        root.after(10, updateScrubhead)
        pass

root.after(10, updateScrubhead)
tk.mainloop()
