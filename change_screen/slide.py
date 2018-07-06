from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.graphics import Line

import os
from datetime import datetime
from pathlib import PurePath
from time import sleep


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
    def get_Info(self):
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


class MainScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass


class ExperimentApp(App):
    def build(self):
        return presentation

if __name__ == '__main__':
    presentation = Builder.load_file("layout.kv")
    ExperimentApp().run()
    print('saved ' + os.getcwd() + '/' + fileFolder)
