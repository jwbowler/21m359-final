# import math
# import scipy
# from scipy.ndimage import zoom
# from scipy.signal import decimate
# from common.wavegen import *
# from kivy.uix.image import Image
#
# from meshtest import make_ribbon_mesh
#
# from kivy.graphics import Color, PushMatrix, PopMatrix, Translate, Line, Mesh
# from kivy.uix.widget import Widget
#
# import numpy as np
#
#
# class Edit(object):
#     def __init__(self, edit_type, start_beat, end_beat):
#         self.edit_type = edit_type
#         self.start_beat = start_beat
#         self.end_beat = end_beat
#
#
# # pixels per beat
# HORIZ_SCALE = 2.
#
#
# class Song(Widget):
#     def __init__(self, filepath, structure, selection, bar0_beat=4, gain=1, speed=1):
#         super(Song, self).__init__(size_hint=(None, None))
#
#         self.selection = selection
#
#         self.wave_reader = WaveReader(filepath)
#         self.gain = gain
#         self.speed = speed
#
#         # get a local copy of the audio data from WaveReader
#         self.wave_reader.set_pos(0)
#         self.data = self.wave_reader.read(self.wave_reader.num_frames * 2)
#
#         self.structure = structure
#         bpm = structure['bpm']
#         self.frames_per_beat = int(44100 * 60. / bpm) ############## shouldn't be rounded...
#
#         bar0_frame = structure['bar0_frame']
#         self.beats_before_bar0 = int(bar0_frame / self.frames_per_beat) + 1
#         start_padding = int(self.frames_per_beat * self.beats_before_bar0) - bar0_frame
#         end_padding = self.frames_per_beat
#         beats_after_bar0 = int((len(self.data) - 2*bar0_frame) / (2 * self.frames_per_beat)) + 1
#         self.data = np.pad(self.data, (start_padding * 2, end_padding * 2), 'constant', constant_values=(0, 0))
#         self.beatmap = range(-self.beats_before_bar0, beats_after_bar0)
#
#         self.start_beat = bar0_beat - self.beats_before_bar0
#         self.bar0_beat = bar0_beat
#         self.num_beats = len(self.beatmap)
#
#         section_beats = [n for (n, section_label) in self.structure['sections']]
#         self.section_beats = np.cumsum(section_beats)
#         self.section_beats = np.insert(self.section_beats, 0, 0)
#
#         self.blah_width = int(HORIZ_SCALE * self.num_beats)
#         self.width = 9000
#
#         print 'start beat:', self.start_beat
#         print 'beats before bar 0:', self.beats_before_bar0
#
#         with self.canvas:
#             PushMatrix()
#             self.translate = Translate(self.start_beat * HORIZ_SCALE, 0)
#
#             mid_height = self.pos[1] + self.size[1]/2
#             # self.waveform = Line(points=(self.pos[0], mid_height, self.pos[0] + self.size[0], mid_height))
#
#             Color(0.5, 0.5, 0.5)
#             self.waveform = self._make_ribbon_mesh(self.pos[0], self.pos[1], self.blah_width, self.height)
#             self.color = Color(1, 1, 1)
#
#
#             self.section_lines = [
#                 (
#                     Color(1, 1, 1),
#                     Line(points=[self.pos[0] + HORIZ_SCALE * (beat + self.beats_before_bar0),
#                                  0,
#                                  self.pos[0] + HORIZ_SCALE * (beat + self.beats_before_bar0),
#                                  self.size[1]])
#                 )
#                 for beat in self.section_beats
#             ]
#
#             PopMatrix()
#
#     def delete(self, start_beat_idx, end_beat_idx):
#         self.duplicate(start_beat_idx, end_beat_idx, 0)
#
#     def duplicate(self, start_beat_idx, end_beat_idx, num_loops):
#         sequence = self.beatmap[start_beat_idx, end_beat_idx]
#         self.beatmap = self.beatmap[:start_beat_idx] + (sequence * num_loops) + self.beatmap[end_beat_idx:]
#
#     def restore(self, beat_idx):
#         beat = self.beatmap[beat_idx]
#         next_beat = self.beatmap[beat_idx + 1]
#
#         if next_beat <= beat:
#             return
#
#         for new_beat in range(beat, next_beat):
#             beat_idx += 1
#             self.beatmap.insert(beat_idx, new_beat)
#
#     def move(self, num_beats):
#         self.start_beat += num_beats
#
#     def set_speed(self, speed):
#         self.speed = speed
#
#     def set_gain(self, gain):
#         self.gain = gain
#
#     def generate_beat(self, global_beat):
#         # we need to grab a different # of frames, depending on speed:
#         # adj_frames = int(round(num_frames * self.speed))
#         #
#         # data = ?????
#         #
#         # # split L/R:
#         # data_l = data[0::2]
#         # data_r = data[1::2]
#         #
#         # # stretch or squash data to fit exactly into num_frames (ie 512)
#         # x = np.arange(adj_frames)
#         # x_resampled = np.linspace(0, adj_frames, num_frames)
#         # resampled_l = np.interp(x_resampled, x, data_l)
#         # resampled_r = np.interp(x_resampled, x, data_r)
#         #
#         # # convert back to stereo
#         # output = np.empty(2 * num_frames, dtype=np.float32)
#         # output[0::2] = resampled_l
#         # output[1::2] = resampled_r
#         #
#         # return (output, keep_going)
#
#         if global_beat < self.start_beat or global_beat >= self.start_beat + self.num_beats:
#             return np.zeros(self.frames_per_beat * 2)
#
#         beat = self.beatmap[global_beat - self.start_beat]
#         print global_beat - self.start_beat, beat
#
#         # grab correct chunk of data
#         start = (self.frames_per_beat * (beat + self.beats_before_bar0)) * 2
#         end = start + (self.frames_per_beat * 2)
#         output = self.data[start:end]
#
#         return output
#
#     def on_touch_down(self, touch):
#         if self.collide_point(*touch.pos):
#             touch.grab(self)
#
#             beat_num = (touch.pos[0] / HORIZ_SCALE) - self.start_beat
#             #print beat_num
#             beat_idx = np.abs(self.section_beats - beat_num).argmin()
#             #print beat_idx
#
#             if abs(self.section_beats[beat_idx] - beat_num) < 5:
#                 self.selection.toggle_select(self, beat_idx)
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
#
#     # a ribbon mesh has a matrix of vertices laid out as 2 x N+1 (rows x columns)
#     # where N is the # of segments.
#     def _make_ribbon_mesh(self, x, y, w, h):
#         signal_power = np.square(self.data)
#         frames_per_pixel = int(self.frames_per_beat / HORIZ_SCALE)
#         scale_factor = frames_per_pixel * 2
#
#         pad_size = math.ceil(float(signal_power.size)/scale_factor)*scale_factor - signal_power.size
#         signal_power = np.append(signal_power, np.zeros(pad_size)*np.NaN)
#
#         print signal_power.shape
#         signal_power = signal_power.reshape(-1, scale_factor)
#         print signal_power.shape
#
#         signal_power = scipy.nanmean(signal_power, axis=1)
#         print signal_power.shape
#
#         signal_power /= np.max(signal_power)
#
#         print 'signal power', len(signal_power)
#         print signal_power[100:200]
#         print np.max(signal_power)
#
#         segments = self.blah_width
#
#         mesh = Mesh()
#
#         # create indices
#         mesh.indices = range(segments * 2 + 2)
#
#         # create vertices with evenly spaced texture coordinates
#         span = np.linspace(0.0, 1.0, segments + 1)
#         verts = []
#
#         mid_y = y + h/2
#         y_scale = h/2
#
#         idx = 0
#         for s in span:
#             height = y_scale * signal_power[idx]
#             verts += [x + s * w, mid_y - height, s, 0, x + s * w, mid_y + height, s, 1]
#             idx += 1
#         mesh.vertices = verts
#
#         # # animate a sine wave by setting the vert positions every frame:
#         # theta = 3.0 * self.time
#         # y = 300 + 50 * np.sin(np.linspace(theta, theta + 2 * np.pi, self.segments + 1))
#         # self.mesh.vertices[5::8] = y
#
#         # seems that you have to reassign the entire verts list in order for the change
#         # to take effect.
#         mesh.vertices = mesh.vertices
#
#         # # assign texture
#         # if tex_file:
#         #     mesh.texture = Image(tex_file).texture
#
#         # standard triangle strip mode
#         mesh.mode = 'triangle_strip'
#
#         return mesh