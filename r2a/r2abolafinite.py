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
        self.throughputs = []
        self.qi = []

        # r(n,t,b) table (maximum utility possible)
        # n - segment/frame/msg
        # b - buffer level
        # t - time
        # N - Segments of video
        # p - seconds of the video
        # M - bitrate
        # Qmax - max size of the buffer

    def handle_xml_request(self, msg):
        self.request_time = time.perf_counter()
        self.send_down(msg)

    def handle_xml_response(self, msg):
        parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = parsed_mpd.get_qi()
        
        duration = parsed_mpd.get_period_info()['duration'].split()[0]
        hours, minutes, seconds = re.findall(r"[-+]?\d*\.\d+|\d+", duration)
        self.seconds_of_video = float(hours)*60*60 + float(minutes)*60 + float(seconds)

        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        msg.add_quality_id(self.qi[1])
        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        some_fucking_time = min(self.whiteboard.get_playback_qi())
        new_time = max(some_fucking_time/2, 3*self.seconds_of_video)

        min(self.whiteboard.get_max_buffer_size(), new_time/self.seconds_of_video)

        # print(self.whiteboard.get_playback_buffer_size())
        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass