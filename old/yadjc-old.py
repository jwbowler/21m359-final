from beatgen import BeatwiseGenerator
from common.audiotrack import *
# from common.clock import *
from common.clock import Clock as ClassClock
from common.core import *
from common.graphics import *
# from common.song import *
from common.wavegen import *

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, PushMatrix, PopMatrix, Translate
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from selection import Selection

from song import Song, HORIZ_SCALE

import numpy as np

# pixels per bar
# HORIZ_SCALE = 1.5


# class Clip(Widget):
#     def __init__(self, songgen, song_structure, start_bar, selection):
#         super(Clip, self).__init__(size_hint=(None, None))
#
#         self.selection = selection
#         self.translate = None
#
#         self.songgen = songgen
#         self.song_structure = song_structure
#
#         self.song_bpm = self.song_structure['bpm']
#         self.bar0_frame = self.song_structure['bar0_frame']
#         self.set_start_bar(start_bar)
#
#         section_lengths = [n for (n, section_label) in self.song_structure['sections']]
#         self.num_bars = sum(section_lengths)
#         self.section_bars = np.cumsum(section_lengths)
#
#         self.width = HORIZ_SCALE * self.num_bars
#
#         with self.canvas:
#             PushMatrix()
#             self.translate = Translate(self.start_bar * HORIZ_SCALE, 0)
#
#             self.color = Color(1, 1, 1)
#             self.rect = Line(rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1]))
#
#             self.section_lines = [
#                 (
#                     Color(1, 1, 1),
#                     Line(points=[self.pos[0] + HORIZ_SCALE * bar,
#                                  0,
#                                  self.pos[0] + HORIZ_SCALE * bar,
#                                  self.size[1]])
#                 )
#                 for bar in self.section_bars
#             ]
#
#             PopMatrix()
#
#             #self.scheduler = scheduler
#             #self.conductor = scheduler.cond
#             #self.set_start_beat(start_beat)
#
#     def set_start_bar(self, start_bar):
#         self.start_bar = start_bar
#         frame_of_start_bar = int(start_bar * 4 * (60. / self.song_bpm) * 44100)
#         self.songgen.set_start_frame(frame_of_start_bar - self.bar0_frame)
#
#         if self.translate:
#             self.translate.x = self.start_bar * HORIZ_SCALE
#
#     def cut(self, bar1_idx, bar2_idx):
#         print 'CUTTTTTT', bar1_idx, bar2_idx
#
#     def on_touch_down(self, touch):
#         if self.collide_point(*touch.pos):
#             touch.grab(self)
#
#             bar_num = (touch.pos[0] / HORIZ_SCALE) - self.start_bar
#             #print bar_num
#             bar_idx = np.abs(self.section_bars - bar_num).argmin()
#             #print bar_idx
#
#             if abs(self.section_bars[bar_idx] - bar_num) < 5:
#                 self.selection.toggle_select(self, bar_idx)
#
#             #with self.canvas:
#             #    print self.color.rgb
#             #    if self.color.rgb == [1, 1, 1]:
#             #        self.color.rgb = [1, 0, 0]
#             #    else:
#             #        self.color.rgb = [1, 1, 1]
#
#             #print 'HI'
#             return True
#
#     def on_touch_up(self, touch):
#         if touch.grab_current is self:
#             touch.ungrab(self)
#             return True


class Nowline(Widget):
    def __init__(self, scheduler):
        super(Nowline, self).__init__(size_hint=(None, None))

        self.scheduler = scheduler
        scheduler.post_at_tick(kTicksPerQuarter, self.increment)

        with self.canvas:
            PushMatrix()
            self.translate = Translate(0, 0)
            Color(0, 1, 1)
            Line(points=[50 + self.pos[0], 1000, 50 + self.pos[0], -9001])
            PopMatrix()

    def increment(self, tick, args):
        # print tick
        self.translate.x += HORIZ_SCALE
        self.scheduler.post_at_tick(tick + kTicksPerQuarter, self.increment)

    def set_to_beat(self, beat):
        self.translate.x = HORIZ_SCALE * beat
        pass

    def refresh(self):
        self.scheduler.commands = []
        tick = self.scheduler.cond.get_tick()
        self.translate.x = (tick / kTicksPerQuarter) * HORIZ_SCALE
        self.scheduler.post_at_tick(tick + kTicksPerQuarter, self.increment)


song1_structure = {
    'bpm': 128,
    'bar0_frame': 2430,
    'sections': (
        (4 * 32, 'Intro'),
        (4 * 4, 'Pre-verse'),

        (4 * 16, 'Verse 1'),
        (4 * 4, 'Build 1'),
        (4 * 24, 'Drop 1'),

        (4 * 4, 'Pre-breakdown'),
        (4 * 24, 'Breakdown'),

        (4 * 8, 'Verse 2'),
        (4 * 8, 'Build 2'),
        (4 * 24, 'Drop 2'),

        (4 * 32, 'Outro'),
        (4 * 8, 'Trail')
    )
}

song2_structure = {
    'bpm': 128,
    'bar0_frame': 10900,
    'sections': (
        (4 * 16, 'Verse 1a'),
        (4 * 16, 'Verse 1b'),
        (4 * 8, 'Build 1'),
        (4 * 16, 'Drop 1'),

        (4 * 16, 'Verse 2a'),
        (4 * 16, 'Verse 2b'),
        (4 * 8, 'Build 2'),
        (4 * 16, 'Drop 2'),

        (4 * 4, 'Trail')
    )
}


class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        songpath1 = 'together-we-are.wav'
        songpath2 = 'lionhearted.wav'

        self.selection = Selection()

        song1 = Song(songpath1, song1_structure, self.selection)
        song2 = Song(songpath2, song2_structure, self.selection)

        self.beatgen = BeatwiseGenerator()
        self.beatgen.add_song(song1)
        self.beatgen.add_song(song2)

        audio = Audio()
        audio.add_generator(self.beatgen)

        self.selection.beatgen = self.beatgen

        self.clock = ClassClock()
        self.conductor = Conductor(self.clock)
        self.scheduler = Scheduler(self.conductor)

        self.conductor.set_bpm(128)

        #info = Label(text = "text", pos=(0, 500), text_size=(100,100), valign='top')
        #self.add_widget(info)

        # root = ScrollView(size_hint=(None, None), size=(800, 600),
        #                   pos_hint={'center_x': .5, 'center_y': .5})
        # self.add_widget(root)

        #self.rel = AnchorLayout(size_hint=(None, None), width=9000, pos_hint={'center_x': .5, 'center_y': .5},
        #                        anchor_x='left', anchor_y='top')
        self.rel = RelativeLayout(size_hint=(None, None), width=9000, pos_hint={'center_x': .5, 'center_y': .5})
        self.add_widget(self.rel)

        # anchor = AnchorLayout(anchor_x='left', anchor_y='top')
        # self.rel.add_widget(anchor)

        layout = GridLayout(cols=1, padding=50, spacing=50, size_hint=(None, None), width=9000, row_force_default=True,
                            row_default_height=100)
        self.rel.add_widget(layout)

        for song in self.beatgen.get_songs():
            container = RelativeLayout()
            layout.add_widget(container)
            container.add_widget(song)

        self.nowline = Nowline(self.scheduler)
        self.rel.add_widget(self.nowline)

        self.beatgen.nowline = self.nowline

    def on_update(self):
        self.scheduler.on_update()

    def on_touch_down(self, touch):
        return super(MainWidget, self).on_touch_down(touch)

    def on_key_down(self, keycode, modifiers):
        (idx, char) = keycode
        if char == 'backspace':
            self.selection.set_state('NORMAL')
        elif char == 'c':
            self.selection.set_state('CUT')
        elif char == 'l':
            self.selection.set_state('LINK')
        elif char == 'g':
            self.selection.set_state('GO')

        # elif char == 'q':
        #     pass

        elif char == 'w':
            self.beatgen.next_beat -= 32

        elif char == 'e':
            self.beatgen.next_beat += 32

        elif char == 'spacebar':
            #self.clock.toggle()
            # print self.scheduler.cond.get_tick()
            self.beatgen.toggle()

        elif char == 'right':
            self.rel.x -= 100

        elif char == 'left':
            self.rel.x += 100

        elif char == 'up':
            self.rel.y -= 100

        elif char == 'down':
            self.rel.y += 100

# run(MainWidget)
