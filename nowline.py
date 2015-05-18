from common.clock import kTicksPerQuarter
from kivy.graphics import PushMatrix, Translate, Color, Line, PopMatrix
from kivy.uix.widget import Widget
from song import HORIZ_SCALE


class Nowline(Widget):
    def __init__(self, scheduler):
        super(Nowline, self).__init__(size_hint=(None, None))

        self.scheduler = scheduler
        scheduler.post_at_tick(kTicksPerQuarter, self.increment)

        with self.canvas:
            PushMatrix()
            self.translate = Translate(0, 0)
            Color(0, 1, 1)
            Line(points=[self.pos[0], 1000, self.pos[0], -9001])
            PopMatrix()

    def increment(self, tick, args):
        # print tick
        self.translate.x += HORIZ_SCALE
        self.scheduler.post_at_tick(tick + kTicksPerQuarter, self.increment)

    def set_to_beat(self, beat):
        self.translate.x = HORIZ_SCALE * beat
        pass

    # approximate!
    def get_display_beat(self):
        return int(self.translate.x / HORIZ_SCALE)

    def refresh(self):
        self.scheduler.commands = []
        tick = self.scheduler.cond.get_tick()
        self.translate.x = (tick / kTicksPerQuarter) * HORIZ_SCALE
        self.scheduler.post_at_tick(tick + kTicksPerQuarter, self.increment)
