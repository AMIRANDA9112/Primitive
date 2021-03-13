from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.clock import Clock
import random


class RootWidget(GridLayout):
    pass

class MainApp(App):

    def build(self):


        parent = GridLayout(cols=50)
        Colour=[0,0,0,0]
        self.create_button(parent,Colour,1,1)
        Clock.schedule_interval(lambda a:self.update(parent), 0)
        return parent

    def update(self,obj):
        print ("I am update function")
        obj.clear_widgets()
        print ("random value is ",random.random())
        for i in range(50):
            for j in range(50):
                c=[random.random(),random.random(),random.random(),random.random()]
                d=[i,j]
                self.create_button(obj,c,i,j)

    def create_button(self,obj,color,i,j):

        a=Button(background_color=color,text='Hello World %s%s'%(i,j), on_press=self.press)
        obj.add_widget(a)
        print(a)

    def press(self, event):
        print("nalga")




if __name__ == '__main__':
    MainApp().run()
