# -*- coding: utf-8 -*-
"""

"""

from player.parser import *
from r2a.ir2a import IR2A
import time
import math
import re


class R2ABolaFinite(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.request_time = 0
        self.qi = []
        self.gamma = 5
        self.last_selected_qi = 0
        self.bandwidth_of_last_segment = 0

        # r(n,t,b) table (maximum utility possible)
        # N - Segments of video
        # n - segment/frame/msg [0...N]
        # b - buffer level
        # t - time
        # p - seconds of video per segment
        # M - different bitrates
        # m - bitrate [0...M]
        # Sm - size of m
        # Qmax - max size of the buffer
        # Q - buffer level (available buffer)
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

        self.vm = [math.log(bitrate/self.qi[0]) for bitrate in self.qi]

        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        if not self.whiteboard.get_playback_qi():
            current_playtime = 0
        else:
            current_playtime = self.whiteboard.get_playback_qi()[0][0]

        segment_size = msg.get_segment_size()

        time = min(current_playtime, self.video_duration_in_seconds - current_playtime)
        new_time = max(time/2, 3*segment_size)

        Q_D_max = min(self.whiteboard.get_max_buffer_size(), new_time/segment_size)
        V_D = (Q_D_max - 1)/(self.vm[self.last_selected_qi] * self.gamma*segment_size)

        # TODO: Implementar vm e alterar o array de self.qi[0]
        estimated_qi = self.argmax((V_D*self.vm[self.last_selected_qi] + V_D*self.gamma*segment_size - self.whiteboard.get_playback_buffer_size())/self.qi[self.last_selected_qi])

        if estimated_qi > self.last_selected_qi:
            new_qi_array = [s/segment_size for s in self.qi]
            
            print(new_qi_array)
            
            bandwidth = max[self.bandwidth_of_last_segment, self.qi[0]/segment_size]

            for i in new_qi_array:
                if bandwidth > i:
                    selected_qi = new_qi_array[i]
            
            print(selected_qi)

            if selected_qi >= estimated_qi:
                selected_qi = estimated_qi
            elif selected_qi < self.last_selected_qi:
                selected_qi = self.last_selected_qi
            else:
                selected_qi = selected_qi + 1 # BOLA-U

            self.last_selected_qi = selected_qi


        time.sleep(max((self.segment_time * (self.whiteboard.get_playback_buffer_size() - Q_D_max)), 0))
        msg.add_quality_id(self.qi_array[selected_qi])
        self.request_time = time.perf_counter()

        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        segment_download_time = time.perf_counter() - self.request_time
        self.bandwidth_of_last_segment = msg.get_bit_length()/segment_download_time
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