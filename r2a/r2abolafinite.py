# -*- coding: utf-8 -*-
"""

"""

from player.parser import *
from r2a.ir2a import IR2A
import time
import re


class R2ABolaFinite(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.request_time = 0
        self.qi = []

        # r(n,t,b) table (maximum utility possible)
        # N - Segments of video
        # n - segment/frame/msg [0...N]
        # b - buffer level
        # t - time
        # p - seconds of video per segment
        # M - different bitrates
        # m - bitrate [0...M]
        # Qmax - max size of the buffer
        # V - parameter control (if V > 0 allow a tradeoff between the buffer size and the performance objectives)
        # vm - 
        # y - is an input weight parameter for prioritizing playback utility versus the playback smoothness

    def handle_xml_request(self, msg):
        self.request_time = time.perf_counter()
        self.send_down(msg)

    def handle_xml_response(self, msg):
        parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = parsed_mpd.get_qi()
        
        duration = parsed_mpd.get_period_info()['duration'].split()[0]
        hours, minutes, seconds = re.findall(r"[-+]?\d*\.\d+|\d+", duration)
        self.video_duration_in_seconds = float(hours)*60*60 + float(minutes)*60 + float(seconds)

        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        msg.add_quality_id(self.qi[10])
        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        if not self.whiteboard.get_playback_qi():
            current_playtime = 0
        else:
            current_playtime = self.whiteboard.get_playback_qi()[0][0]

        time = min(current_playtime, self.video_duration_in_seconds - current_playtime)
        new_time = max(time/2, 3*msg.get_segment_size())

        Q_D_max = min(self.whiteboard.get_max_buffer_size(), new_time/self.video_duration_in_seconds)
        V_D = (Q_D_max - 1)/()

        selected_qi = argmax(V_D*vm + V_D*yp - Q)/Sm



        # print(self.whiteboard.get_playback_buffer_size())
        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass

    def argmax(self, array):
        index, value = 0, array[0]

        for i,v in enumerate(array):
            if v > value:
                index, value = i,v
        return array[index]