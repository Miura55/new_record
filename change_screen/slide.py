from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.graphics import Line

from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import MeshLinePlot
from kivy.clock import Clock
from threading import Thread
import audioop
import pyaudio

import os
from datetime import datetime
from pathlib import PurePath
from time import sleep

def get_microphone_level():
    """
    source: http://stackoverflow.com/questions/26478315/getting-volume-levels-from-pyaudio-for-use-in-arduino
    audioop.max alternative to audioop.rms
    """
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()

    s = p.open(format=FORMAT,
               channels=CHANNELS,
               rate=RATE,
               input=True,
               frames_per_buffer=chunk)
    global levels
    while True:
        data = s.read(chunk)
        mx = audioop.rms(data, 2)
        if len(levels) >= 100:
            levels = []
        levels.append(mx)

class get_Info(Widget):
    def on_touch_down(self, touch):
        labeldatetime = ObjectProperty(None)
        buttoncount = ObjectProperty(None)


class StartScreen(Screen):
    def get_Info(self):
        global presentation
        global fileFolder
        now = datetime.now()
        nowtime = now.strftime('%Y%m%d%M%M%S')
        name_ = self.nametext.text
        exnum_ = self.agetext.text
        fileFolder = name_ +'_'+ exnum_
        # make directory
        # cmd = "mkdir " + fileFolder + " " + fileFolder+"\Audio " + fileFolder+"\Log "+ fileFolder+"\NAO " + fileFolder+"\Webcam " + fileFolder+"\Webcam\Frames " + fileFolder+"\NAO\Frames "
        cmd = "mkdir " + fileFolder + " " + fileFolder + "/Audio " + fileFolder + "/Log " + fileFolder + "/Webcam " + fileFolder + "/Webcam/Frames "
        prompt = os.popen(cmd, "w")
        prompt.write("y")
        sleep(1)
        profile = [nowtime,'\n', name_,'\n', exnum_]
        name_file = nowtime + '.txt'
        text_file = PurePath(os.getcwd()) / fileFolder / name_file
        with open(text_file, 'a') as f:
            f.writelines(profile)
        # move next screen
        presentation.current = "other"



class PlotGraph(Screen):
    def __init__(self,):
        super(Logic, self).__init__()
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])

    def start(self):
        self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value, 0.001)

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, dt):
        self.plot.points = [(i, j/5) for i, j in enumerate(levels)]

class MainScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class ExperimentApp(App):
    def build(self):
        return presentation


if __name__ == '__main__':
    levels = []  # store levels of microphone
    get_level_thread = Thread(target = get_microphone_level)
    get_level_thread.daemon = True
    get_level_thread.start()
    MainApp().run()
