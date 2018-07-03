# -*- coding: utf-8 -*-

import kivy
import cv2
import numpy as np
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from datetime import datetime
from os import path
import pyaudio
import wave
import subprocess

class timerWidget(Widget):
    labeldatetime = ObjectProperty(None)
    buttoncount = ObjectProperty(None)

class MyApp(App):

    #ボタンを押したときのアクション
    def buttoncount_clicked(self, src):
        now = datetime.now()
        self.root.now_ = now.strftime('%Y,%m,%d  %H:%M:%S')
        self.root.labeldatetime.text = str(self.root.now_)
        nowtime = self.root.labeldatetime.text
        name_ = self.root.nametext.text
        age_ = self.root.agetext.text
        profile = [nowtime,'\n', name_,'\n', age_]
        name_file = nowtime + '.txt'
        file = open(path.join('text', name_file), 'w')  #書き込みモードでオープン
        file.writelines(profile)
        self.sound_rec('start')
        self.rec_video()

    def buttonquit_clicked(self, src):
        print('done:', self.root.now_)

    def build(self):
        self.root = timerWidget()
        self.root.username = TextInput(multiline=False)
        self.root.buttoncount.bind(on_press=self.buttoncount_clicked)
        self.root.buttonquit.bind(on_press=self.buttonquit_clicked)
        return self.root

    def sound_rec(self, rec_sta):
        if rec_sta == 'start':
            file_name = self.root.now_ + '.wav'
            self.root.p = subprocess.Popen(("rec", "-q",path.join('sound', file_name) ))
        elif rec_sta == 'quit':
            self.root.p.terminate()
            try:
                self.root.p.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.root.p.kill()

    def rec_video(self):
        #カメラから入力を得る
        self.cap = cv2.VideoCapture(0)

        #動画書き出し用のオブジェクト
        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        fps = 20.0
        size = 20.0
        size = (640, 480)
        file_name = self.root.now_ + '.m4v'
        self.out = cv2.VideoWriter(path.join ('video', file_name), fmt, fps, size)

        while True:
            #フレームを読む
            _, frame = self.cap.read()
            frame = cv2.resize(frame, size)
            #画面を出力
            self.out.write(frame)
            #ディスプレイに画面を表示
            cv2.imshow('frame', frame)
            #ESCキーが押されたらループを抜ける
            k = cv2.waitKey(1)
            if k == 27:
                self.sound_rec('quit')
                break
        self.out.release()
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    MyApp().run()
