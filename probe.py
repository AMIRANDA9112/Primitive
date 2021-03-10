from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color, InstructionGroup
from kivy.clock import Clock
import numpy as np
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout


Config.set('graphics', 'width', 500)
Config.set('graphics', 'height', 500)




XSIZE = 50
YSIZE = 50


class Cell(Widget):
    def __init__(self, position, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.ig = InstructionGroup()
        self.rect = Rectangle()
        self.color = Color(1, 0, 0)
        self.ig.add(self.color)
        self.ig.add(self.rect)
        self.state = False
        self.position = position


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.rows = YSIZE
        self.cols = XSIZE
        self.space = [1, 1]
        self.game_state = np.zeros((XSIZE, YSIZE))
        self.col_force_default = True
        self.row_force_default = True
        self.col_default_width = 10
        self.row_default_height = 10

        i = 0

        for y in range(50):
            for x in range(50):
                self.add_widget(Cell((x, y)))
                self.canvas.add(self.children[0].ig)
                i += 1
                print(i)

        Clock.schedule_once(self.set_attributes)

    def set_attributes(self, dt):
        for i in self.children:
            i.rect.pos = i.pos
            i.rect.size = i.size

    def on_touch_down(self, touch):
        ton = touch.pos
        print(ton)


class BoxButtons(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxButtons, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        startButton = Button(text='Start')
        stopButton = Button(text='Stop')
        clearButon = Button(text='Clear')
        self.add_widget(startButton)
        self.add_widget(stopButton)
        self.add_widget(clearButon)
        self.size_hint = (1, 0.25)


class MainBox(BoxLayout):
    def __init__(self, **kwargs):
        super(MainBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        top_buttons = BoxButtons()
        grid_main = MyGrid()
        self.add_widget(top_buttons)
        self.add_widget(grid_main)


class GameApp(App):
    def build(self):
        return MainBox()


if __name__ == '__main__':
    GameApp().run()
