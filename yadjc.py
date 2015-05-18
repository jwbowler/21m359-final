from beatgen import BeatwiseGenerator
from common.audio import Audio
from common.clock import Clock as ClassClock, Conductor, Scheduler
from common.core import BaseWidget, run
from kivy.core.window import Window
from kivy.graphics import Color, PushMatrix, Translate, PopMatrix, Rectangle
from kivy.graphics import Line
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from nowline import Nowline
#from selection import Selection
from song import Song
from song_structures import structures


kRowHeight = 100
kRowWidth = 10000
kGridPadding = 10
kGridUpperGap = 30
kGridLeftGap = 40


class Desktop(Widget):
    def __init__(self, nowline, **kwargs):
        super(Desktop, self).__init__(**kwargs)

        with self.canvas:
            PushMatrix()
            self.trans_y = Translate(0, self.pos[1])
            self.trans_y.y -= kGridUpperGap

            self.delete_buttons = DeleteButtons()
            #self.add_widget(self.delete_buttons)

            PushMatrix()
            self.trans_x = Translate(self.pos[0], 0)
            self.trans_x.x += kGridLeftGap

            self.grid = Grid(self.delete_buttons)
            self.add_widget(self.grid)

            self.add_widget(nowline)

            PopMatrix()
            PopMatrix()

            # Color(0, 0, 0)
            # Rectangle(pos=(0, Window.size[1] - 70), size=(Window.size[0], 70))

        self.down_pos = None
        self.active_drag = False

    def on_touch_down(self, touch):
        self.active_drag = False

        self.down_pos = touch.pos

        # touch.push()
        # touch.apply_transform_2d(lambda x, y: (x, y - self.trans_y.y))
        # ret1 = self.delete_buttons.on_touch_down(touch)
        # touch.pop()
        #
        # if ret1:
        #     return True

        touch.push()
        touch.apply_transform_2d(lambda x, y: (x - self.trans_x.x, y - self.trans_y.y))
        ret2 = self.grid.on_touch_down(touch)
        touch.pop()

        if ret2:
            return True

        self.active_drag = True
        return True

    def on_touch_move(self, touch):
        if self.active_drag:
            mov_x = touch.pos[0] - self.down_pos[0]
            mov_y = touch.pos[1] - self.down_pos[1]
            self.trans_x.x += mov_x
            self.trans_y.y += mov_y
            self.down_pos = touch.pos

            return True

        else:
            touch.push()
            touch.apply_transform_2d(lambda x, y: (x - self.trans_x.x, y - self.trans_y.y))
            ret = super(Desktop, self).on_touch_move(touch)
            touch.pop()

            return ret

    def on_touch_up(self, touch):
        self.active_drag = False

    def on_key_down(self, char, modifiers):
        self.grid.on_key_down(char, modifiers)

    def on_window_resize(self):
        self.grid.on_window_resize()
        self.delete_buttons.on_window_resize()


class DeleteButtons(Widget):
    def __init__(self, **kwargs):
        super(DeleteButtons, self).__init__(**kwargs)
        self.buttons = []

    def add_button(self, grid, row, row_trans):
        with self.canvas.after:
            num_row = grid.num_next_row
            num_removed = grid.num_removed_rows

            # button = Button(text='X')
            # button.size = (40, 40)
            # button.pos = (Window.size[0] - 70, -(num_row - num_removed + 1) * (kRowHeight + kGridPadding) + 30)
            # button.bind(on_release=lambda event: self.remove_button(button, row, row_trans, num_row))
            #
            # self.buttons.append(button)
            # self.add_widget(button)

        self.grid = grid

    def remove_button(self, button, row, row_trans, num_row):
        button.pos[0] = -9001 #yolo
        self.remove_widget(button)
        # del self.buttons[num_row]

        for btn in self.buttons:
            if btn.pos[1] < button.pos[1]:
                btn.pos[1] += (kRowHeight + kGridPadding)

        self.grid.remove_row(row, row_trans)

    def on_window_resize(self):
        for button in self.buttons:
            button.pos[0] = Window.size[0] - 70

    def on_touch_down(self, touch):
        return super(DeleteButtons, self).on_touch_down(touch)


class Grid(Widget):
    def __init__(self, delete_buttons, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.delete_buttons = delete_buttons

        self.rows_and_trans = []

        self.num_next_row = 0
        self.num_removed_rows = 0
        # self.add_row()

    def add_row(self, song):
        with self.canvas:
            PushMatrix()
            row_trans = Translate(0, -(self.num_next_row - self.num_removed_rows + 1) * (kRowHeight + kGridPadding))

            row = Row(self.num_next_row, self.num_removed_rows, song)
            self.add_widget(row)

            self.rows_and_trans.append((row, row_trans))

            PopMatrix()

        self.delete_buttons.add_button(self, row, row_trans)

        self.num_next_row += 1
        return row

    def remove_row(self, row, row_trans):
        print 'HI'

        print row
        row_trans.x = 90001

        self.remove_widget(row)
        self.rows_and_trans.remove((row, row_trans))
        self.num_removed_rows += 1

        for (other_row, other_row_trans) in self.rows_and_trans:
            if other_row_trans.y < row_trans.y:
                other_row_trans.y += (kRowHeight + kGridPadding)
                other_row.move_up()

    def on_key_down(self, char, modifiers):
        pass

    def on_touch_down(self, touch):
        return super(Grid, self).on_touch_down(touch)

    def on_window_resize(self):
        for widget in self.children:
            widget.on_window_resize()


class Row(Widget):
    def __init__(self, idx, num_deleted_above, song, **kwargs):
        super(Row, self).__init__(**kwargs)

        self.idx = idx
        self.num_deleted_above = num_deleted_above
        self.song = song

        self.size = (kRowWidth, kRowHeight)

        with self.canvas:
            self.color = Color(1, 1, 1)
            #self.frame = Line(rectangle=(-kRowWidth, 0, kRowWidth*2, kRowHeight))

            # self.clip = Clip()
            # self.add_widget(self.clip)
            self.add_widget(self.song)

    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(lambda x, y: (x, y + (self.idx - self.num_deleted_above + 1) * (kRowHeight + kGridPadding)))
        ret = super(Row, self).on_touch_down(touch)
        touch.pop()
        return ret

    def on_touch_move(self, touch):
        touch.push()
        touch.apply_transform_2d(lambda x, y: (x, y + (self.idx - self.num_deleted_above + 1) * (kRowHeight + kGridPadding)))
        ret = super(Row, self).on_touch_move(touch)
        touch.pop()
        return ret

    def move_up(self):
        self.num_deleted_above += 1

    def on_window_resize(self):
        pass


# class StateMachine(object):
#     def __init__(self):
#         self.state = 'NORMAL'
#
#     def _set_state(self, state):
#         self.state = state
#         print state
#
#     def on_cut_button_state_change(self, button, down):
#         if down:
#             self._set_state('CUT')
#         else:
#             self._set_state('NORMAL')
#
#     def on_link_button_state_change(self, button, down):
#         if down:
#             self._set_state('LINK')
#         else:
#             self._set_state('NORMAL')




class MainWidget(BaseWidget):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        self.clock = ClassClock()
        self.conductor = Conductor(self.clock)
        self.scheduler = Scheduler(self.conductor)
        self.conductor.set_bpm(90)

        #self.selection = Selection()

        self.beatgen = BeatwiseGenerator()
        audio = Audio()
        audio.add_generator(self.beatgen)

        #self.selection.beatgen = self.beatgen

        self.root = BoxLayout(size=Window.size, orientation='vertical')
        self.add_widget(self.root)

        self.nowline = Nowline(self.scheduler)
        self.beatgen.nowline = self.nowline

        self.desktop = Desktop(self.nowline, pos=(0, Window.size[1]))
        # self.root.add_widget(self.desktop)

        # self.button_tray_anchor = AnchorLayout(anchor_x='right', anchor_y='top')
        # self.root.add_widget(self.button_tray_anchor)

        # self.button_tray = StackLayout(size_hint=(1, None), orientation='lr-tb', padding=10, spacing=5)
        # self.button_tray_anchor.add_widget(self.button_tray)

        def redraw(self, args):
            self.bg_rect.size = self.size
            self.bg_rect.pos = self.pos

        self.button_tray = StackLayout(size_hint=(1, None), orientation='lr-tb', padding=10, spacing=5)
        # with self.button_tray.canvas.before:
        #     Color(0, 0, 0)
        #     self.button_tray.bg_rect = Rectangle(pos=self.pos, size=self.size)
        # self.button_tray.bind(pos=redraw, size=redraw)

        user_path = '/Users/jbowler/mit/21M.359/final/songs/headnod'
        self.browser = FileChooserListView(path=user_path, size_hint=(1, 0.4))
        with self.browser.canvas.before:
            Color(0, 0, 0)
            self.browser.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.browser.bind(pos=redraw, size=redraw)
        self.browser.bind(on_submit=self.on_file_select)

        # self.root.add_widget(self.button_tray)
        self.root.add_widget(self.desktop)
        self.root.add_widget(self.browser)

        # self.sm = StateMachine()
        #
        # btn_cut = ToggleButton(text='Cut', group='operations', size_hint=(None, None), size=(50, 50))
        # btn_cut.bind(state=self.sm.on_cut_button_state_change)
        # self.button_tray.add_widget(btn_cut)
        #
        # btn_link = ToggleButton(text='Link', group='operations', size_hint=(None, None), size=(50, 50))
        # btn_link.bind(state=self.sm.on_link_button_state_change)
        # self.button_tray.add_widget(btn_link)

        Window.bind(on_resize=self._on_window_resize)

    def _on_window_resize(self, window, width, height):
        self.root.size = Window.size
        self.desktop.on_window_resize()

    def on_touch_down(self, touch):
        if self.browser.on_touch_down(touch):
            return True
        if self.button_tray.on_touch_down(touch):
            return True
        if self.desktop.on_touch_down(touch):
            return True

        # return super(MainWidget, self).on_touch_down(touch)
        return False

    def on_touch_move(self, touch):
        return super(MainWidget, self).on_touch_move(touch)

    def on_key_down(self, keycode, modifiers):
        (idx, char) = keycode
        # if char == 'r':
        #     song = Song('together-we-are.wav', song1_structure, self.selection)
        #     self.desktop.grid.add_row(song)
        # self.desktop.on_key_down(char, modifiers)

        if char == 'spacebar':
            self.beatgen.toggle()

        elif char == 'left':
            self.beatgen.next_beat -= 16
            if self.beatgen.paused:
                self.nowline.set_to_beat(self.nowline.get_display_beat() - 16)

        elif char == 'right':
            self.beatgen.next_beat += 16
            if self.beatgen.paused:
                self.nowline.set_to_beat(self.nowline.get_display_beat() + 16)

    def on_file_select(self, *args):
        path = args[1][0]
        print path
        songname = path.split('/')[-1][:-4]
        print songname

        bar0_beat = self.nowline.get_display_beat() + 16
        bar0_beat -= (bar0_beat % 4)
        #song = Song(path, structures[songname], self.selection, bar0_beat=bar0_beat)
        song = Song(path, structures[songname], None)
        print structures[songname]
        self.desktop.grid.add_row(song)
        self.beatgen.add_song(song)




run(MainWidget)
