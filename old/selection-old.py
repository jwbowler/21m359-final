from song import HORIZ_SCALE


class Selection(object):
    def __init__(self):
        self.selected_clip = None
        self.selected_line_idx = None

        self.beatgen = None

        self.state = 'NORMAL'

    def set_state(self, state):
        self.state = state
        print state

    def select(self, clip, line):
        if self.state == 'CUT' and self.selected_clip == clip:
            clip.cut(self.selected_line_idx, line)
            self.unselect()
            self.state = 'NORMAL'

        elif self.state == 'LINK' and self.selected_clip and self.selected_clip != clip:
            top_beat = self.selected_clip.section_beats[self.selected_line_idx] + self.selected_clip.bar0_beat
            bottom_beat = clip.section_beats[line] + clip.bar0_beat

            clip_movement = top_beat - bottom_beat
            clip.start_beat += clip_movement
            clip.bar0_beat += clip_movement
            clip.translate.x = clip.start_beat * HORIZ_SCALE

            print 'LINKED'

            self.unselect()
            self.state = 'NORMAL'

        elif self.state == 'GO':
            if not self.beatgen:
                return

            beat = clip.section_beats[line]
            self.beatgen.next_beat = clip.bar0_beat + beat

            self.unselect()
            self.state = 'NORMAL'

        else:
            self.unselect()

            self.selected_clip = clip
            self.selected_line_idx = line

            line_color = clip.section_lines[line][0]
            line_color.rgb = [1, 0, 0]

    def unselect(self):
        if self.selected_clip:
            line_color = self.selected_clip.section_lines[self.selected_line_idx][0]
            line_color.rgb = [1, 1, 1]

        self.selected_clip = None
        self.selected_line_idx = None

    def toggle_select(self, clip, line):
        if self.selected_clip == clip and self.selected_line_idx == line:
            self.unselect()
        else:
            self.select(clip, line)

