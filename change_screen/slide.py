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


class MainScreen(Screen):
    pass

class AnotherScreen(Screen):
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


class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("layout.kv")

class MainApp(App):
    def build(self):
        return presentation
    def buttoncount_clicked(self, src):
        now = datetime.now()
        self.root.now_ = now.strftime('%Y,%m,%d  %H:%M:%S')
        self.root.labeldatetime.text = str(self.root.now_)
        nowtime = self.root.labeldatetime.text
        name_ = self.root.nametext.text
        age_ = self.root.agetext.text
        profile = [nowtime,'\n', name_,'\n', age_]
        name_file = nowtime + '.txt'
        with open(name_file, 'w') as f:
            f.writelines(profile)

if __name__ == '__main__':
    levels = []  # store levels of microphone
    get_level_thread = Thread(target = get_microphone_level)
    get_level_thread.daemon = True
    get_level_thread.start()
    MainApp().run()
