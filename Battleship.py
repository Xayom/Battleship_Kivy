#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
CURRENT_PLAYER = 1
MAIN_SOUND = SoundLoader.load('Epich.mp3')
Winner = SoundLoader.load('winner.mp3')
Lose = SoundLoader.load('proval.mp3')
CURRENT = 0
AMOUNT = 0
AMOUNT1 = 0
SOME_LIST = []
CURRENT1 = 0
SOME_LIST1 = []

winner = ModalView(size_hint=(0.75, 0.5))
victory_label = Label(text='You Lose!!!!!', font_size=50)
winner.add_widget(victory_label)

class ScreenManagment(ScreenManager):
    pass

class BoardScreen1(Screen):

    status = ListProperty([0 for i in range(100)])
    coords = ListProperty([0, 0])
    popup = ModalView(size_hint=(0.4, 0.2))
    popup.pos_hint = {'x':0.3, 'y':0.85}
    popup.add_widget(Label(text='You Turn...', font_size = 30))

    def on_enter(self):
        global ENTRY_PLAYER

        if ENTRY_PLAYER == 0:
            MAIN_SOUND.stop()
            Sound.unload('Epich.mp3')

            ENTRY_PLAYER = 1
            for i in range(NUMBER_OF_BUTTONS):
                for j in range(NUMBER_OF_BUTTONS):
                    button = Button(text = "")
                    button.size_hint = (200, 200)
                    button.coords = (i, j)
                    button.bind(on_press = self.button_pressed)
                    for ship in SHIPS_OF_PLAYER:
                        if ship[0] == (i, j):
                            button.background_color = ship[1]
                            button.name = str(ship[2])

                    self.ids.grid.add_widget(button)

            self.manager.current = 'board2'
            self.popup.open()
            Clock.schedule_once(self.callback, 1.2)

    def button_pressed(self, button):
        if button.text == 'YES':
            self.manager.current = 'main'
            self.popup1.dismiss()

    def callback(self, dt):
        self.popup.dismiss()


    def exit(self):
        self.popup1 = ModalView(size_hint=(0.75, 0.5))
        grd = GridLayout()
        grd.cols = 2
        grd.padding = 120
        flt = FloatLayout()
        lbl = Label(pos = (100, 260), text = 'Are you sure to exit game????', font_size = 35)
        flt.add_widget(lbl)
        btn1 = Button(text='YES',font_size=50)
        btn1.bind(on_press = self.button_pressed)
        btn2 = Button(text='NO', font_size=50)
        btn2.bind(on_press = self.popup1.dismiss)
        grd.add_widget(btn1)
        grd.add_widget(btn2)
        self.popup1.add_widget(flt)
        self.popup1.add_widget(grd)
        #popup.bind(on_dismiss=self.reset)
        self.popup1.open()

    def on_status(self, instance, new_value):
        status = new_value

class BoardScreen2(Screen):
    status = ListProperty([0 for i in range(100)])
    coords = ListProperty([0, 0])
    popup1 = ModalView(size_hint=(0.4, 0.2), auto_dismiss = False)
    popup1.pos_hint = {'x':0.3, 'y':0.85}
    popup1.add_widget(Label(text='Computers Turn, Please wait...', font_size = 16))
    current = 0
    sound = SoundLoader.load('target.mp3')

    def on_enter(self):
        global ENTRY_COMP, ENTRY_PLAYER

        if ENTRY_COMP == 0:
            ENTRY_COMP = 1

            for i in range(NUMBER_OF_BUTTONS):
                for j in range(NUMBER_OF_BUTTONS):
                    button = Button(text="")
                    button.coords = (i, j)
                    button.bind(on_press = self.button_pressed)
                    self.ids.grid.add_widget(button)

    def exit(self):
        self.popup = ModalView(size_hint=(0.75, 0.5))
        grd = GridLayout()
        grd.cols = 2
        grd.padding = 120
        flt = FloatLayout()
        lbl = Label(pos = (100, 260), text = 'Are you sure to exit game????', font_size = 35)
        flt.add_widget(lbl)
        btn1 = Button(text='YES',font_size=50)
        btn1.bind(on_press = self.button_pressed)
        btn2 = Button(text='NO', font_size=50)
        btn2.bind(on_press = self.popup.dismiss)
        grd.add_widget(btn1)
        grd.add_widget(btn2)
        self.popup.add_widget(flt)
        self.popup.add_widget(grd)
        self.popup.open()

    def somefunc(self, *args):
        self.manager.current = 'main'

    def button_pressed(self, button):
        if button.text == 'YES':
            self.manager.current = 'main'
            self.popup.dismiss()
        else:
            global CURRENT_PLAYER, AMOUNT, CURRENT1, SOME_LIST1
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
                        #button.text = str(ship[2])
                        self.sound.stop()
                        self.sound = SoundLoader.load('bomb2.wav')
                        self.sound.play()

                        if CURRENT1 == ship[2]:
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

                        AMOUNT += 1
                        if AMOUNT == 4 + 3 * 2 + 2 * 3 + 4:
                            Winner.play()
                            winner.children[0].text = 'You WIN!!!!!'
                            winner.bind(on_dismiss = self.somefunc)
                            winner.open()
                        break

                if button.background_color == [1, 1, 1, 1]:
                    button.text = 'X'

                    self.sound.stop()
                    self.sound = SoundLoader.load('Not_ship.wav')
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
        self.manager.current = 'main'

    def my_callback(self, dt):
        self.current += dt
        if self.current > 5:
            global CURRENT_PLAYER, LIST_OF_TARGETS1, LIST_OF_TARGETS, CURRENT, SOME_LIST, AMOUNT1
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
                        self.sound = SoundLoader.load('Not_ship.wav')
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
                        if AMOUNT1 == 4 + 3 * 2 + 2 * 3 + 4:
                            self.popup1.dismiss()
                            Clock.unschedule(self.my_callback)
                            Lose.play()
                            winner.children[0].text = 'You Lost!!!!!'
                            winner.bind(on_dismiss = self.somefunc)
                            winner.open()
                            return

                        TARGETS.remove((x, y))
                        if CURRENT == int(child.name):
                            LIST_OF_TARGETS1[:] = []
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

                        self.current = 0
                        self.sound.stop()
                        self.sound = SoundLoader.load('bomb2.wav')
                        self.sound.play()
                    return

        child = self.popup1.children[0]
        if child.text[-1:-4:-1] == '...':
            child.text = child.text[:-3]
        else:
            child.text += '.'

    def on_status(self, instance, new_value):
        status = new_value

class RandomScreen(Screen):
    def on_pre_enter(self):
        for child in self.ids.grid.children:
                child.background_color = [1, 1, 1, 1]

        def my_callback(dt):
            view.dismiss()

        view = ModalView(size=(100, 100))
        view.background = 'img.jpg'
        view.open()
        Clock.schedule_once(my_callback, 5)



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

class MainScreen(Screen):
    def on_enter(self):
        Winner.stop()
        Lose.stop()
        MAIN_SOUND.play()

presentation = Builder.load_file("My.kv")

class Myapp(App):
    def build(self):
        return presentation

if __name__ == '__main__':
    Myapp().run()