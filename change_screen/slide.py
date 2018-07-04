from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty

from kivy.uix.widget import Widget
from kivy.graphics import Line

class get_Info(Widget):
    def on_touch_down(self, touch):
        labeldatetime = ObjectProperty(None)
        buttoncount = ObjectProperty(None)

class Painter(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x, touch.y))

    def on_touch_move(self,touch):
        touch.ud["line"].points += [touch.x, touch.y]

class MainScreen(Screen):
    pass

class AnotherScreen(Screen):
    pass

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
        with open(name_file, 'w') as f: #書き込みモードでオープン
            f.writelines(profile)

if __name__ == '__main__':
    MainApp().run()
