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
Config.set('graphics', 'height', 550)

XSIZE = 50
YSIZE = 50

dimCW = 500 / XSIZE
dimCH = 500 / YSIZE

F = 0


class Cell(Widget):
    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.ig = InstructionGroup()
        self.rect = Rectangle(size=(1, 1))
        self.color = Color(0, 1, 0)
        self.ig.add(self.color)
        self.ig.add(self.rect)

    def live_color(self):
        self.ig.clear()
        self.color = Color(1, 0, 0)
        self.ig.add(self.color)
        self.ig.add(self.rect)

    def death_color(self):
        self.ig.clear()
        self.color = Color(0, 0, 1)
        self.ig.add(self.color)
        self.ig.add(self.rect)


class MyGrid(GridLayout):
    game_state = np.zeros((XSIZE, YSIZE))
    new_game_state = np.zeros((XSIZE, YSIZE))
    pause = True

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = XSIZE
        self.rows = YSIZE
        self.space = [1, 1]
        self.col_force_default = True
        self.row_force_default = True
        self.col_default_width = 10
        self.row_default_height = 10

        self.pause = True

        Clock.schedule_once(self.init_page)

    def init_page(self, dt):

        cel = 0

        for y in range(YSIZE):
            for x in range(XSIZE):
                self.add_widget(Cell())
                if not self.game_state[x, y]:

                    self.children[0].death_color()

                    self.canvas.add(self.children[0].ig)
                else:

                    self.children[0].live_color()

                    self.canvas.add(self.children[0].ig)

                cel += 1

        Clock.schedule_once(self.set_attributes)
        Clock.schedule_interval(self.init_game, 0.5)

    def init_game(self, dt):

        self.canvas.clear()

        celg = 0

        self.new_game_state = np.copy(self.game_state)

        for y in range(YSIZE):
            for x in range(XSIZE):

                if not self.game_state[x, y]:
                    self.children[celg].death_color()
                    self.canvas.add(self.children[celg].ig)
                else:

                    self.children[celg].live_color()

                    self.canvas.add(self.children[celg].ig)

                if not self.pause:

                    n_neigh = (
                            self.game_state[(x - 1) % XSIZE, (y - 1) % YSIZE]
                            + self.game_state[x % XSIZE, (y - 1) % YSIZE]
                            + self.game_state[(x + 1) % XSIZE, (y - 1) % YSIZE]
                            + self.game_state[(x - 1) % XSIZE, y % YSIZE]
                            + self.game_state[(x + 1) % XSIZE, y % YSIZE]
                            + self.game_state[(x - 1) % XSIZE, (y + 1) % YSIZE]
                            + self.game_state[x % XSIZE, (y + 1) % YSIZE]
                            + self.game_state[(x + 1) % XSIZE, (y + 1) % YSIZE]

                    )

                    if self.game_state[x, y] == 0 and n_neigh == 3:
                        self.new_game_state[x, y] = 1

                    elif self.game_state[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                        self.new_game_state[x, y] = 0

                celg += 1

        self.game_state = np.copy(self.new_game_state)

    def set_attributes(self, dt):
        for i in self.children:
            i.rect.pos = i.pos
            i.rect.size = i.size

        print("rune")

    def on_touch_down(self, touch):
        posx, posy = touch.pos

        if posy > 500:
            return

        posx, posy = (49 - int(np.floor(posx / dimCW))), int(np.floor(posy / dimCH))
        self.game_state[posx, posy] = not self.new_game_state[posx, posy]

        print(posx, posy)


class BoxButtons(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxButtons, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.start_button = Button(text='Start')

        self.stop_button = Button(text='Stop')

        self.clear_button = Button(text='Clear')

        self.add_widget(self.start_button)
        self.add_widget(self.stop_button)
        self.add_widget(self.clear_button)
        self.size_hint = (1, 0.10)
        print("button class active")


class MainBox(BoxLayout):
    def __init__(self, **kwargs):
        super(MainBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.box_buttons = BoxButtons()
        self.grid_main = MyGrid()
        self.add_widget(self.box_buttons)
        self.add_widget(self.grid_main)
        print("main class active")


class Primitive(MainBox):

    def __init__(self, **kwargs):
        super(Primitive, self).__init__(**kwargs)
        self.box_buttons.start_button.bind(on_press=self.start_game)
        self.box_buttons.stop_button.bind(on_press=self.stop_game)
        self.box_buttons.clear_button.bind(on_press=self.clear_game)

        print("game init")

    def start_game(self, event):
        self.grid_main.pause = False

    def stop_game(self, event):
        self.grid_main.pause = True

    def clear_game(self, event):
        self.grid_main.game_state = np.zeros((XSIZE, YSIZE))
        self.grid_main.new_game_state = np.zeros((XSIZE, YSIZE))

        self.grid_main.pause = True
        print("m")


class GameApp(App):
    def build(self):
        return Primitive()


if __name__ == '__main__':
    GameApp().run()
