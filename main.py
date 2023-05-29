import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.label import Label
from kivy.lang import Builder
import webbrowser
import cv2
import numpy as np
from pyzbar.pyzbar import Decoded, decode
import keyboard
Builder.load_file("test.kv")

class Gerenciar(ScreenManager):
    pass

class Menu(Screen):
    def site(self):
        webbrowser.open("https://www.youtube.com/shorts/MYGUq-0tAXY")

    def scan(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        while True:
            success, img = cap.read()
            for barcode in decode(img):
                # print(barcode.data)
                myData = barcode.data.decode('utf-8')
                print(myData, flush=True)
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, (255,0,255), 5)
                pts2 = barcode.rect
                cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 165,0), 2)
         
            cv2.imshow('Scan QR Code - https://laptrinhvb.net', img)
            cv2.waitKey(1)
            if keyboard.is_pressed('q'): 
                break


class Botao(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super(Botao, self).__init__(**kwargs)
        self.atualizar()
    
    def on_pos(self,*args):
        self.atualizar()

    def on_size(self, *args):
        self.atualizar()

    def atualizar(self, *args):
        self.canvas.before.clear()

        with self.canvas.before:
            Color(rgba = (0.1,0.5,0.7,1))
            Ellipse(size = (self.height,self.height), 
                    pos = self.pos)
            Ellipse(size = (self.height,self.height),
                    pos = (self.x+self.width-self.height,self.y))
            Rectangle(size = (self.width-self.height,self.height),
                      pos = (self.x+self.height/2.0,self.y))
            
class Tarefas(Screen):
    def __init__(self,tarefas = [], **kwargs):
        super(Tarefas, self).__init__(**kwargs)
        for tarefa in tarefas:
            self.ids.box.add_widget(Tarefa(text= tarefa))
    

    def on_pre_enter(self):
        Window.bind(on_keyboard = self.voltar)

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard = self.voltar)

    def addWidget(self):
        texto = self.ids.texto.text
        self.ids.box.add_widget(Tarefa(text=texto))
        self.ids.texto.text = ''

class Tarefa(BoxLayout):
    def __init__(self, text = '', **kwargs):
        super(Tarefa, self).__init__(**kwargs)
        self.ids.label.text = text

class Test(App):
    def build(self):
        return Gerenciar()
    
Test().run()
