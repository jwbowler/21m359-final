from collections import deque
import numpy as np

class BeatwiseGenerator(object):
    def __init__(self):
        self.buf = deque()
        self.songs = []
        self.paused = True
        self.next_beat = 0

    def add_song(self, song):
        self.songs.append(song)

    def get_songs(self):
        return self.songs

    def play(self):
        self.paused = False

    def pause(self):
        self.paused = True

    def toggle(self):
        self.paused = not self.paused

    def generate(self, num_frames):
        # print len(self.buf)

        if self.paused:
            output = np.zeros(num_frames * 2)

        else:
            while len(self.buf) < num_frames * 2:
                self._add_beat_to_buf()

            output = np.array([self.buf.popleft() for i in range(num_frames * 2)])

        return (output, True)

    def _add_beat_to_buf(self):
        # print self.next_beat
        # print self.songs[0].generate_beat(0)
        print 'adding', self.next_beat
        # new_beat_data = np.add(*[song.generate_beat(self.next_beat) for song in self.songs])
        new_beat_data = self.songs[0].generate_beat(self.next_beat)

        for i in range(1, len(self.songs)):
            new_beat_data = np.add(new_beat_data, self.songs[i].generate_beat(self.next_beat))

        print len(new_beat_data)
        self.buf.extend(new_beat_data)

        self.nowline.set_to_beat(self.next_beat)

        self.next_beat += 1
