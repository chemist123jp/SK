#-*- coding: utf-8 -*-
import sys
import os
from win32api import GetSystemMetrics

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.core.window import Window  # フルスクリーン、あるいは途中でサイズを変更する
from kivy.app import App  # コアファイル
from kivy.core.text import LabelBase, DEFAULT_FONT # フリーフォントファイルを使用
from kivy.resources import resource_add_path  # フリーフォントファイルの呼び出し
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from datetime import datetime
import multiprocessing as mp
from multiprocessing import Process, Manager, freeze_support, Queue
from time import sleep

import Extreme
from cv_cap import VideoClass


sys.path.append("../.")

# デフォルトに使用するフォントを変更する
resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'mplus-2c-regular.ttf')

#画面の解像度を変数に代入
Disp_width = GetSystemMetrics(0)
Disp_height = GetSystemMetrics(1)

q = Queue()
end_flag = Queue()
SK = Extreme.SuperK(q, end_flag)

def cap_video(q, end_flag):
    VideoClass(q, end_flag)

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MainClass(Screen):

    # kvファイルとデータを受け渡しする場合はここでインスタンス化しておく
    tv = ObjectProperty(None)
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    file_name = ObjectProperty(None)
    is_checked1 = BooleanProperty(False)
    is_checked2 = BooleanProperty(False)
    is_checked3 = BooleanProperty(False)
    is_checked4 = BooleanProperty(False)
    is_checked5 = BooleanProperty(False)
    is_checked6 = BooleanProperty(False)
    is_checked7 = BooleanProperty(False)
    is_checked8 = BooleanProperty(False)

    p1 = mp.Process(target=cap_video, args=(q, end_flag,))

    def __init__(self, **kwargs):
        super(MainClass, self).__init__(**kwargs)

    # ポップアップでファイルを読み込む場合の関数
    def show_load(self, button_type):
        self.file_name = button_type
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="読み込み中", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.file_name.text = filename[0]
        # with open (os.path.join(path, filename[0])) as stream:
        #    self.text_input.text = stream.read()
        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()


    # ボタンクリック等で何かをする場合はこの下に関数を記載する
    def rasor_onoff(self):
        rasor_status = self.ids.rasor_status
        if rasor_status.text == 'OFF':
            rasor_status.text = 'ON'
            # SK.rasor_on()
            rasor_status.background_color = (0, 0.0, 1.0, 1)
        else:
            rasor_status.text = 'OFF'
            rasor_status.background_color = (1.0, 0.0, 0, 1)
            # SK.rasor_off()

    def rec_onoff(self):
        rec_status = self.ids.rec_status
        if rec_status.text == 'OFF':
            rec_status.text = 'ON'
            rec_status.background_color = (0, 0.0, 1.0, 1)
            self.p1 = mp.Process(target=cap_video, args=(q, end_flag,))
            self.p1.start()
        else:
            rec_status.text = 'OFF'
            rec_status.background_color = (1.0, 0.0, 0, 1)
            #end_flag.put("end") #  endflagいらないかも
            self.p1.terminate()

    def take_pic(self):
        time_stamp = "{0:%Y%m%d_%H_%M_%S}".format(datetime.now())
        q.put(time_stamp)

    def main_power(self):
        main_power_status = self.ids.main_power
        print(main_power_status.text)
        #SK.change_power_value(main_power_status.text)

    def take_all(self):
        self.wave_length_all = []
        self.rasor_power_all = []

        for i in range(8):
            self.wave_length_all.append(eval("self.ids.ch" + str(i+1) + "_wavelength.text"))
            self.rasor_power_all.append(eval("self.ids.ch" + str(i+1) + "_power.text"))

        print(self.wave_length_all)
        print(self.rasor_power_all)

        #main_power_status = self.ids.main_power
        #print(main_power_status.text)
        #SK.change_power_value(main_power_status.text)





    def power_down(self):
        print(q.get())

    def update_gaisen(self):
        q.put("aaa")

    def execute(self):
        p1 = mp.Process(target=cap_video, args=(self.q, self.end_flag,))
        p1.start()

    def rasor(self, q, end_flug):
        #"""

         # 操作モジュールをインスタンス化

        SK.rasor_on()  # レーザーの初期化、起動



        SK.change_power_value(100)
        sleep(3)

        SK.change_wave(640)
        SK.change_wave(650, 1)
        SK.change_power_value(100, 1)
        sleep(3)
        SK.change_wave(660, 2)
        SK.change_power_value(100, 2)
        sleep(3)
        SK.change_wave(670, 3)
        SK.change_power_value(100, 3)
        sleep(3)

        SK.rasor_off()


        SK.rasor_off()

class GuiEditApp(App):

    def __init__(self, **kwargs):
        super(GuiEditApp, self).__init__(**kwargs)
        # デフォルトの画面サイズを指定　Disp_widthは上でスクリーンサイズを取得している
        Window.top = 20
        Window.left = Disp_width-(Disp_width/5)
        Window.size = (Disp_width/5, Disp_height-50)
        # フルスクリーンにするか
        Window.fullscreen = False

    def build(self):
        self.title = 'SuperK Controller'  # windowのタイトル
        self.icon = 'icon.png'  # windowのアイコン 指定しなければデフォルトのやつ
        sm.add_widget(MainClass(name='main'))
        return sm

if __name__ == '__main__':
    sm = ScreenManager(transition=NoTransition())
    GuiEditApp().run()
