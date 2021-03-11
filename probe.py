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

dimCW = 500 / XSIZE
dimCH = 400 / YSIZE


class Cell(Widget):
    def __init__(self, position, color, **kwargs):
        super(Cell, self).__init__(**kwargs)
        self.ig = InstructionGroup()
        self.rect = Rectangle()
        self.color = color
        self.ig.add(self.color)
        self.ig.add(self.rect)

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
        self.state = True
        self.init_game()

        self.new_game_state = np.zeros((XSIZE, YSIZE))

    def init_game(self):

        posInitX = int((XSIZE / 2) - 3)
        posInitY = int((YSIZE / 2) - 5)
        self.game_state[posInitX, posInitY] = 1

        self.new_game_state = self.game_state
        self.update_grid()

    def update_grid(self):

        i = 0

        for y in range(50):
            for x in range(50):

                i += 1
                print(i)

                if not self.game_state[x, y]:

                    self.add_widget(Cell(position=(x, y), color=Color(0, 1, 0)))
                    self.canvas.add(self.children[0].ig)
                else:
                    self.add_widget(Cell(position=(x, y), color=Color(1, 0, 0)))
                    self.canvas.add(self.children[0].ig)

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

        Clock.schedule_once(self.set_attributes)

    def set_attributes(self, dt):
        for i in self.children:
            i.rect.pos = i.pos
            i.rect.size = i.size

    def on_touch_down(self, touch):
        posx, posy = touch.pos

        if posy > 400:
            return

        posx, posy = int(np.floor(posx / dimCW)), int(np.floor(posy / dimCH))

        self.new_game_state[posx, posy] = not self.game_state[posx, posy]

        print(posx, posy)


class BoxButtons(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxButtons, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.start_button = Button(text='Start')
        self.start_button.bind(on_press=self.start_game)
        self.stop_button = Button(text='Stop')
        self.stop_button.bind(on_press=self.stop_game)
        self.clear_button = Button(text='Clear')
        self.stop_button.bind(on_press=self.clear_game)
        self.add_widget(self.start_button)
        self.add_widget(self.stop_button)
        self.add_widget(self.clear_button)
        self.size_hint = (1, 0.25)

    def start_game(self, event):

        Clock.schedule_interval(MainBox.grid_main.update_grid, 1)

    def stop_game(self, event):
        Clock.unschedule(MainBox.grid_main.update_grid)

    def clear_game(self, event):
        Clock.unschedule(MainBox.grid_main.update_grid)

        MyGrid.game_state = np.zeros((XSIZE, YSIZE))

        MyGrid.new_game_state = np.zeros((XSIZE, YSIZE))

        Clock.schedule_once(MainBox.grid_main.set_attributes)



class MainBox(BoxLayout):
    def __init__(self, **kwargs):
        super(MainBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.top_buttons = BoxButtons()
        self.grid_main = MyGrid()
        self.add_widget(self.top_buttons)
        self.add_widget(self.grid_main)


class GameApp(App):
    def build(self):
        return MainBox()


if __name__ == '__main__':
    GameApp().run()
