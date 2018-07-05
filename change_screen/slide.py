from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty

from kivy.uix.widget import Widget
from kivy.graphics import Line
from datetime import datetime



class Painter(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x, touch.y))

    def on_touch_move(self,touch):
        touch.ud["line"].points += [touch.x, touch.y]

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
    # def on_touch_down(self, touch):
    #     labeldatetime = ObjectProperty(None)
    #     buttoncount = ObjectProperty(None)
    def buttoncount_clicked(self):
        now = datetime.now()
        self.now_ = now.strftime('%Y,%m,%d  %H:%M:%S')
        # self.labeldatetime.text = s1tr(self.root.now_)
        nowtime = self.now_
        name_ = self.nametext.text
        age_ = self.agetext.text
        profile = [nowtime,'\n', name_,'\n', age_]
        name_file = nowtime + '.txt'
        with open(name_file, 'w') as f:
            f.writelines(profile)


class AnotherScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("layout.kv")

class ExperimentApp(App):
    def build(self):
        return presentation

if __name__ == '__main__':
    ExperimentApp().run()
