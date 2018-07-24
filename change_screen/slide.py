# encoding: utf-8
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.graphics import Line

from kivy.uix.boxlayout import BoxLayout
# from kivy.garden.graph import MeshLinePlot
from graph import Graph, MeshLinePlot
from kivy.clock import Clock
from threading import Thread
import audioop
import pyaudio
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
import os
from datetime import datetime
import time
from time import sleep
import random


def get_b():
    global b_datas
    while True:
        if len(b_datas) >= 100:
            b_datas = []
        b_datas.append(random.randint(0, 10))
        sleep(0.02)

def get_gsr():
    global gsr_data
    gsr_source = 'C:\Users\HRI-Chubu\Documents\Resenv-MA-MASensors-master\\test\_E4_L_gsr_20180724_055510'
    while True:
        data_set = open(gsr_source, 'r')
        line_r = data_set.read()
        data_r = line_r.split("\n")
        pit_r = data_r[-2]
        pit_r = pit_r.split(',')
        if len(gsr_data) >= 100:
            gsr_data = []
        gsr_data.append(float(pit_r[1]))
        sleep(0.02)

def get_tmp():
    global tmp_data
    tmp_source = 'C:\Users\HRI-Chubu\Documents\Resenv-MA-MASensors-master\\test\_E4_L_tmp_20180724_055510'
    while True:
        data_set = open(tmp_source, 'r')
        line_r = data_set.read()
        data_r = line_r.split("\n")
        pit_r = data_r[-2]
        pit_r = pit_r.split(',')
        if len(tmp_data) >= 100:
            tmp_data = []
        tmp_data.append(float(pit_r[1]))
        sleep(0.02)

def get_ibi():
    global ibi_data
    ibi_source = 'C:\Users\HRI-Chubu\Documents\Resenv-MA-MASensors-master\\test\_E4_L_ibi_20180724_055510'
    while True:
        data_set = open(tmp_source, 'r')
        line_r = data_set.read()
        data_r = line_r.split("\n")
        pit_r = data_r[-2]
        pit_r = pit_r.split(',')
        if len(tmp_data) >= 100:
            tmp_data = []
        tmp_data.append(float(pit_r[1]))
        sleep(0.02)

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
        cmd = "mkdir " + fileFolder + " " + fileFolder+"\Audio " + fileFolder+"\Log "+ fileFolder+"\NAO " + fileFolder+"\Webcam " + fileFolder+"\Webcam\Frames " + fileFolder+"\NAO\Frames "
        # cmd = "mkdir " + fileFolder + " " + fileFolder + "/Audio " + fileFolder + "/Log " + fileFolder + "/Webcam " + fileFolder + "/Webcam/Frames "
        prompt = os.popen(cmd, "w")
        prompt.write("y")
        profile = [nowtime,'\n', name_,'\n', exnum_]
        name_file = nowtime + '.txt'
        text_file = fileFolder + '\\' + name_file
        # move next screen
        presentation.current = "other"
        with open(text_file, 'w') as f:
            f.writelines(profile)


class MainScreen(Screen):
    def __init__(self,**kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.b_plot = MeshLinePlot(color=[0, 1, 0, 1])
        self.c_plot = MeshLinePlot(color=[0, 0, 1, 1])

    def start(self):
        self.ids.graph.add_plot(self.plot)
        self.ids.b_graph.add_plot(self.b_plot)
        self.ids.c_graph.add_plot(self.c_plot)
        Clock.schedule_interval(self.get_value, 0.001)

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, dt):
        global fileFolder
        global frame_num
        self.dt = dt
        self.plot.points = [(i, j) for i, j in enumerate(gsr_data)]
        self.b_plot.points = [(i, j) for i, j in enumerate(tmp_data)]
        self.c_plot.points = [(i, j) for i, j in enumerate(ibi_data)]

        # Save Frame
        camera = self.ids['camera']
        camera.export_to_png(fileFolder + "\Webcam\Frames\IMG_{}.png".format(frame_num))
        frame_num += 1

class PlotGraph(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass


class ExperimentApp(App):
    def build(self):
        return presentation


if __name__ == '__main__':
    gsr_data = []
    tmp_data = []
    ibi_data = []
    b_datas = []
    frame_num = 0
    presentation = Builder.load_file("layout.kv")

    # Start Plot thread
    get_level_thread = Thread(target = get_gsr)
    get_level_thread.daemon = True
    get_level_thread.start()
    get_b_thread = Thread(target = get_b)
    get_b_thread.daemon = True
    get_b_thread.start()
    get_c_thread = Thread(target = get_tmp)
    get_c_thread.daemon = True
    get_c_thread.start()

    ExperimentApp().run()
    timestr = time.strftime("%Y%m%d_%H%M%S")
    cmd = "ffmpeg -r "+str(10)+ " -i " +fileFolder+"\Webcam\Frames\IMG_%d.png -vcodec libx264 -pix_fmt yuv420p -r 60 "+fileFolder+"\Webcam\webcam1_"+timestr+".mp4"
    print cmd
    try:
        prompt = os.popen(cmd, "w")
        prompt.write("y")
    except Exception,e:
        print "..."
        print "Error on saving video 1 file was: ",e

    # Finish apprication
    import sys
    sys.exit()
