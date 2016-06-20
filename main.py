import random
from kivy.app import App
from kivy.core.audio import SoundLoader, Sound
from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.clock import mainthread
from kivy.graphics import Canvas
from kivy.uix.image import Image
from kivy.uix.carousel import Carousel

import Placingships

DEFAULT = [[(i, j), [1, 1, 1, 1]] for i in range(10) for j in range(10)]

BATTLESHIP = (4, 1, [1, 2, 3, 4])
CRUISER = (3, 2, [2, 5, 1, 2])
DESTROYER = (2, 3, [1, 1, 4, 3])
SUBMARINE = (1, 4, [1, 3, 2, 4])
LIST_OF_SHIPS = [BATTLESHIP, CRUISER, DESTROYER, SUBMARINE]
LIST_OF_COORDS = [(i, j) for i in range(10) for j in range(10)]
LIST_OF_TARGETS = LIST_OF_COORDS[::]
LIST_OF_TARGETS1 = []

NUMBER_OF_BUTTONS = 10
ENTRY_PLAYER = 0
ENTRY_COMP = 0
ENTRY_RANDOM = 0
CURRENT_PLAYER = 1
MAIN_SOUND = SoundLoader.load('files/Epich.mp3')
finish = ''
CURRENT = 0
AMOUNT = 0
AMOUNT1 = 0
SOME_LIST = []
CURRENT1 = 0
SOME_LIST1 = []

# This is how you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MainScreen>:
    name: 'main'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: "files/background2.jpg"
    FloatLayout:
        cols:1
        Button:
            background_normal: 'files/button.png'
            on_press:root.manager.current = 'randomize'
            size_hint:(0.3, 0.2)
            font_size:20
            pos_hint:{'center_x':0.5, 'center_y':0.5}
        Button:
            background_normal: 'files/exit0.png'
            on_press:app.stop()
            size_hint:(0.3, 0.2)
            font_size:20
            pos_hint:{'center_x':0.5, 'center_y':0.3}
<RandomScreen>:
    name: 'randomize'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: "files/background1.jpg"
    GridLayout:
        id: grid
        padding: 100
        cols: 10
    FloatLayout:
        id: float
        cols: 2
        Button:
            text: 'Start Battle'
            font_size: 30
            pos_hint: {'right':0.4, 'y':0}
            size_hint:(0.3, 0.15)
            on_press: root.check()
        Button:
            text: 'Press to randomize Ships'
            font_size: 30
            id: btn
            pos_hint: {'right':0.8, 'y':0}
            size_hint:(0.4, 0.15)
            on_press: root.randomize()

<BoardScreen1>:
    name: 'board1'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: "files/background1.jpg"
    GridLayout:
        id: grid
        padding: 100
        cols: 10
    FloatLayout:
        id: float
        cols: 2
        Button:
            text: 'Press to view computer grid'
            font_size: 30
            pos_hint: {'right':0.63, 'y':0.05}
            size_hint:(0.3, 0.1)
            on_press: root.manager.current = 'board2'
        Button:
            background_normal: 'files/exit0.png'
            pos_hint:{'right':1, 'y':0}
            size_hint:(0.2, 0.2)
            on_press: root.exit()

<BoardScreen2>:
    name: 'board2'
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: "files/background1.jpg"
    GridLayout:
        id: grid
        padding: 100
        cols: 10

    FloatLayout:
        id: float
        cols: 10
        padding: 100
        Button:
            text: 'Press to view your grid'
            font_size: 30
            pos_hint: {'right':0.63, 'y':0.05}
            size_hint:(0.3, 0.1)
            on_press: root.manager.current = 'board1'
        Button:
            background_normal: 'files/exit0.png'
            pos_hint:{'right':1, 'y':0}
            size_hint:(0.2, 0.2)
            on_press: root.exit()
""")


# MAINSCREEN
class MainScreen(Screen):
    def on_enter(self):
        MAIN_SOUND.play()

# RANDOMSCREEN
class RandomScreen(Screen):
    def on_pre_enter(self):
        global ENTRY_RANDOM
        for child in self.ids.grid.children:
            child.background_color = [1, 1, 1, 1]

        ENTRY_RANDOM += 1

    def on_enter(self):
        global SHIPS_OF_COMP, SHIPS_OF_PLAYER, ENTRY_PLAYER, ENTRY_COMP, CURRENT_PLAYER, AMOUNT
        SHIPS_OF_COMP = Placingships.randomization(LIST_OF_SHIPS[::], LIST_OF_COORDS[::])
        SHIPS_OF_PLAYER = DEFAULT
        ENTRY_PLAYER = 0
        ENTRY_COMP = 0
        AMOUNT = 0
        CURRENT_PLAYER = 1
        self.manager.get_screen('board1').ids.grid.clear_widgets()
        self.manager.get_screen('board2').ids.grid.clear_widgets()

        if not len(self.ids.grid.children):
            self.ids.grid.top += 80
            self.ids.grid.right -= 15

            for i in range(NUMBER_OF_BUTTONS):
                for j in range(NUMBER_OF_BUTTONS):
                    button = Button(text="")
                    button.coords = (i, j)
                    button.background_color = [1, 1, 1, 1]
                    self.ids.grid.add_widget(button)

    def check(self):
        if SHIPS_OF_PLAYER != DEFAULT:
            self.manager.current = 'board1'

    def randomize(self):
        for child in self.ids.grid.children:
            child.background_color = [1, 1, 1, 1]
        global SHIPS_OF_PLAYER
        SHIPS_OF_PLAYER = Placingships.randomization(LIST_OF_SHIPS[::], LIST_OF_COORDS[::])

        for child in self.ids.grid.children:
            for ship in SHIPS_OF_PLAYER:
                if ship[0] == child.coords:
                    child.background_color = ship[1]


# THE PLAYER'S SCREEN
class BoardScreen1(Screen):
    status = ListProperty([0 for i in range(100)])
    coords = ListProperty([0, 0])
    popup = ModalView(size_hint=(0.3, 0))
    popup.pos_hint = {'x': 0.35, 'y': 0.9}
    popup.add_widget(Label(text='You Turn...', font_size=30))

    def on_enter(self):
        global ENTRY_PLAYER

        if ENTRY_PLAYER == 0:
            MAIN_SOUND.stop()
            ENTRY_PLAYER = 1
            self.ids.grid.top = 760
            self.ids.grid.right = 1350

            for i in range(NUMBER_OF_BUTTONS):
                for j in range(NUMBER_OF_BUTTONS):
                    button = Button(text="")
                    button.size_hint = (100, 100)
                    button.coords = (i, j)
                    button.bind(on_press=self.button_pressed)
                    for ship in SHIPS_OF_PLAYER:
                        if ship[0] == (i, j):
                            button.background_color = ship[1]
                            button.name = str(ship[2])

                    self.ids.grid.add_widget(button)

            self.manager.current = 'board2'
            self.popup.open()
            Clock.schedule_once(self.callback, 1.5)

    def button_pressed(self, button):
        if button.text == 'YES':
            self.manager.current = 'main'
            self.popup1.dismiss()

    def callback(self, dt):
        self.popup.dismiss()

    def exit(self):
        self.popup1 = ModalView(size_hint=(0.5, 0.4))
        grd = GridLayout()
        grd.cols = 2
        grd.padding = 120
        flt = FloatLayout()
        lbl = Label(pos=(320, 340), text='Are you sure to exit game????', font_size=35)
        flt.add_widget(lbl)
        btn1 = Button(text='YES', font_size=50)
        btn1.bind(on_press=self.button_pressed)
        btn2 = Button(text='NO', font_size=50)
        btn2.bind(on_press=self.popup1.dismiss)
        grd.add_widget(btn1)
        grd.add_widget(btn2)
        self.popup1.add_widget(flt)
        self.popup1.add_widget(grd)
        # popup.bind(on_dismiss=self.reset)
        self.popup1.open()

    def on_status(self, instance, new_value):
        status = new_value


# THE COMPUTER'S SCREEN
class BoardScreen2(Screen):
    status = ListProperty([0 for i in range(100)])
    coords = ListProperty([0, 0])
    popup1 = ModalView(size_hint=(0.3, 0.0), auto_dismiss=False)
    popup1.pos_hint = {'x': 0.35, 'y': 0.9}
    popup1.add_widget(Label(text='Computers Turn, Please wait...', font_size=26))
    current = 0
    sound = ''

    def on_enter(self):
        global ENTRY_COMP

        if ENTRY_COMP == 0:
            ENTRY_COMP = 1
            self.ids.grid.top = 760
            self.ids.grid.right = 1350

            for i in range(NUMBER_OF_BUTTONS):
                for j in range(NUMBER_OF_BUTTONS):
                    button = Button(text="")
                    button.coords = (i, j)
                    button.bind(on_press=self.button_pressed)
                    self.ids.grid.add_widget(button)

    def exit(self):
        self.popup = ModalView(size_hint=(0.5, 0.4))
        grd = GridLayout()
        grd.cols = 2
        grd.padding = 120
        flt = FloatLayout()
        lbl = Label(pos=(320, 340), text='Are you sure to exit game????', font_size=35)
        flt.add_widget(lbl)
        btn1 = Button(text='YES', font_size=50)
        btn1.bind(on_press=self.button_pressed)
        btn2 = Button(text='NO', font_size=50)
        btn2.bind(on_press=self.popup.dismiss)
        grd.add_widget(btn1)
        grd.add_widget(btn2)
        self.popup.add_widget(flt)
        self.popup.add_widget(grd)
        self.popup.open()

    # def somefunc(self, *args):
    #     self.manager.current = 'main'
    #
    def button_pressed(self, button):
        if button.text == 'YES':
            self.manager.current = 'main'
            self.popup.dismiss()
        else:
            global CURRENT_PLAYER, AMOUNT, CURRENT1, SOME_LIST1, finish
            row, column = button.coords
            status_index = row * 10 + column
            already_played = self.status[status_index]
            if not already_played and CURRENT_PLAYER == 1:
                self.status[status_index] = CURRENT_PLAYER

                for ship in SHIPS_OF_COMP:
                    if ship[0] == (row, column):
                        CURRENT1 += 1
                        SOME_LIST1.append((row, column))
                        button.background_color = ship[1]
                        # button.text = str(ship[2])
                        if CURRENT1 == ship[2]:
                            if self.sound != '':
                                self.sound.stop()
                            self.sound = SoundLoader.load('files/boom.mp3')
                            self.sound.play()

                            for ship in SOME_LIST1:
                                x, y = ship
                                s = [1, 0, -1]
                                t = [1, 0, -1]
                                for xx in s:
                                    for yy in t:
                                        for child in self.ids.grid.children:
                                            if child.coords == (x + xx, y + yy) and (x + xx, y + yy) not in SOME_LIST1:
                                                child.text = 'X'
                                                child.background_color = [1, 0, 0, 1]
                            SOME_LIST1 = []
                            CURRENT1 = 0
                        else:
                            if self.sound != '':
                                self.sound.stop()
                            self.sound = SoundLoader.load('files/bomb2.wav')
                            self.sound.play()

                        AMOUNT += 1
                        AMOUNT = 4 + 3 * 2 + 2 * 3 + 4
                        if AMOUNT == 4 + 3 * 2 + 2 * 3 + 4:
                            finish = SoundLoader.load('files/winner.mp3')
                            finish.play()
                            winner = ModalView(size_hint=(0.75, 0.5))
                            winner.background = 'files/youWin.png'
                            # victory_label = Label(text='You WIN!!!!!', font_size=50)
                            # winner.add_widget(victory_label)
                            winner.bind(on_dismiss=self.somefunc)
                            winner.open()
                        break

                if button.background_color == [1, 1, 1, 1]:
                    button.text = 'X'
                    if self.sound != '':
                        self.sound.stop()
                    self.sound = SoundLoader.load('files/Not_ship.wav')
                    self.sound.play()

                    button.background_color = [1, 0, 0, 1]
                    Clock.schedule_once(self.callback, 1)
                    CURRENT_PLAYER *= -1

    def callback(self, dt):
        self.manager.current = 'board1'
        self.popup1.open()
        self.current = 0
        Clock.schedule_interval(self.my_callback, 1.0)

    def callback1(self, dt):
        if dt >= 0.9:
            self.manager.get_screen('board1').popup.dismiss()
            self.manager.current = 'board2'
        else:
            self.manager.get_screen('board1').popup.open()
            Clock.schedule_once(self.callback1, 1)

    def somefunc(self, *args):
        finish.stop()
        self.manager.current = 'main'

    def my_callback(self, dt):
        self.current += dt
        if self.current > 2:
            global CURRENT_PLAYER, LIST_OF_TARGETS1, LIST_OF_TARGETS, CURRENT, SOME_LIST, AMOUNT1, finish
            grid = self.manager.get_screen('board1').ids.grid
            rand = random.randint(0, len(LIST_OF_TARGETS) - 1)
            TARGETS = LIST_OF_TARGETS
            if len(LIST_OF_TARGETS1):
                rand = random.randint(0, len(LIST_OF_TARGETS1) - 1)
                TARGETS = LIST_OF_TARGETS1

            for child in grid.children:
                if child.coords == TARGETS[rand]:
                    if child.background_color == [1, 1, 1, 1]:
                        child.text = 'X'
                        child.background_color = [1, 0, 0, 1]
                        self.popup1.dismiss()
                        Clock.unschedule(self.my_callback)
                        CURRENT_PLAYER *= -1
                        self.sound.stop()
                        self.sound = SoundLoader.load('files/Not_ship.wav')
                        self.sound.play()
                        Clock.schedule_once(self.callback1, 0.7)
                        TARGETS.remove(child.coords)
                    else:
                        x, y = child.coords
                        CURRENT += 1
                        AMOUNT1 += 1
                        SOME_LIST.append((x, y))

                        if (x + 1, y + 1) in TARGETS:
                            TARGETS.remove((x + 1, y + 1))
                        if (x - 1, y - 1) in TARGETS:
                            TARGETS.remove((x - 1, y - 1))
                        if (x + 1, y - 1) in TARGETS:
                            TARGETS.remove((x + 1, y - 1))
                        if (x - 1, y + 1) in TARGETS:
                            TARGETS.remove((x - 1, y + 1))

                        if (x + 1, y + 1) in LIST_OF_TARGETS:
                            LIST_OF_TARGETS.remove((x + 1, y + 1))
                        if (x - 1, y - 1) in LIST_OF_TARGETS:
                            LIST_OF_TARGETS.remove((x - 1, y - 1))
                        if (x + 1, y - 1) in LIST_OF_TARGETS:
                            LIST_OF_TARGETS.remove((x + 1, y - 1))
                        if (x - 1, y + 1) in LIST_OF_TARGETS:
                            LIST_OF_TARGETS.remove((x - 1, y + 1))

                        if (x + 1, y) not in LIST_OF_TARGETS1 and (x + 1, y) in LIST_OF_TARGETS:
                            LIST_OF_TARGETS1.append((x + 1, y))
                            LIST_OF_TARGETS.remove((x + 1, y))
                        if (x - 1, y) not in LIST_OF_TARGETS1 and (x - 1, y) in LIST_OF_TARGETS:
                            LIST_OF_TARGETS1.append((x - 1, y))
                            LIST_OF_TARGETS.remove((x - 1, y))
                        if (x, y - 1) not in LIST_OF_TARGETS1 and (x, y - 1) in LIST_OF_TARGETS:
                            LIST_OF_TARGETS1.append((x, y - 1))
                            LIST_OF_TARGETS.remove((x, y - 1))
                        if (x, y + 1) not in LIST_OF_TARGETS1 and (x, y + 1) in LIST_OF_TARGETS:
                            LIST_OF_TARGETS1.append((x, y + 1))
                            LIST_OF_TARGETS.remove((x, y + 1))

                        child.background_color = [0, 1, 0, 1]
                        AMOUNT1 = 4 + 3 * 2 + 2 * 3 + 4
                        if AMOUNT1 == 4 + 3 * 2 + 2 * 3 + 4:
                            self.popup1.dismiss()
                            Clock.unschedule(self.my_callback)
                            finish = SoundLoader.load('files/proval.mp3')
                            finish.play()
                            winner = ModalView(size_hint=(0.75, 0.5))
                            winner.background = 'files/You_Lost.png'
                            # victory_label = Label(text='You Lost!!!!!', font_size=50)
                            # winner.add_widget(victory_label)
                            winner.bind(on_dismiss=self.somefunc)
                            winner.open()
                            return

                        TARGETS.remove((x, y))
                        if CURRENT == int(child.name):
                            LIST_OF_TARGETS1[:] = []
                            if self.sound != '':
                                self.sound.stop()
                            self.sound = SoundLoader.load('files/boom.mp3')
                            self.sound.play()

                            for ship in SOME_LIST:
                                x, y = ship
                                s = [1, 0, -1]
                                t = [1, 0, -1]
                                for xx in s:
                                    for yy in t:
                                        for child in grid.children:
                                            if child.coords == (x + xx, y + yy) and (x + xx, y + yy) not in SOME_LIST:
                                                child.text = 'X'
                                                child.background_color = [1, 0, 0, 1]
                            SOME_LIST = []
                            CURRENT = 0
                        else:
                            if self.sound != '':
                                self.sound.stop()
                            self.sound = SoundLoader.load('files/bomb2.wav')
                            self.sound.play()
                        self.current = 0
                    return

        child = self.popup1.children[0]
        if child.text[-1:-4:-1] == '...':
            child.text = child.text[:-3]
        else:
            child.text += '.'

    def on_status(self, instance, new_value):
        status = new_value


# Create the screen manager and add screens
sm = ScreenManager()
sm.add_widget(MainScreen())
sm.add_widget(RandomScreen())
sm.add_widget(BoardScreen1())
sm.add_widget(BoardScreen2())


class TestApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    TestApp().run()
