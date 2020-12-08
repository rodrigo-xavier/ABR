# -*- coding: utf-8 -*-
"""

"""

from r2a.ir2a import IR2A
from player.parser import *
from player import *
from base.whiteboard import Whiteboard
import time
from statistics import mean
import numpy as np

whiteboard = Whiteboard

class R2ABola(IR2A):
    def __init__(self, id):
        IR2A.__init__(self, id)
        self.throughputs = []
        self.request_time = 0
        self.qi = []
        
        self.video_duration = 0
        self.max_buffer_size = 0

        self.gama = 5
        self.vm = 0

        self.last_throughput = 0

    def handle_xml_request(self, msg):
        self.request_time = time.perf_counter()
        self.send_down(msg)

    def handle_xml_response(self, msg):

        t = time.perf_counter() - self.request_time

        parsed_mpd = parse_mpd(msg.get_payload())

        '''
        print("get_mpd_info: " + str(parsed_mpd.get_mpd_info()))
        print("get_period_info: " + str(parsed_mpd.get_period_info()))
        print("get_program_info: " + str(parsed_mpd.get_program_info()))
        print("get_adaptation_set_info: " + str(parsed_mpd.get_adaptation_set_info()))
        print("get_title: " + str(parsed_mpd.get_title()))
        print("get_segment_template: " + str(parsed_mpd.get_segment_template()))
        print("get_first_level_adp_set: " + str(parsed_mpd.get_first_level_adp_set()))
        print("get_qi: " + str(parsed_mpd.get_qi()))
        '''

        self.qi = parsed_mpd.get_qi()

        # self.max_buffer_size = parsed_mpd.get_max_buffer_size()

        # total duration of video
        self.video_duration = int(parsed_mpd.get_period_info()['duration'][2:].split('H')[0]) * 3600
        self.video_duration += int(parsed_mpd.get_period_info()['duration'][2:].split('H')[1].split('M')[0]) * 60
        self.video_duration += float(parsed_mpd.get_period_info()['duration'][2:].split('H')[1].split('M')[1].split('S')[0])
        print("seconds: " + str(self.video_duration))

        self.vm = np.array([np.log(bitrate/self.qi[0]) for bitrate in self.qi])

        self.last_throughput = msg.get_bit_length() / t

        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        
        '''
        print(msg.get_payload())
        print(msg.get_kind())
        print(msg.get_bit_length())
        print(msg.get_host_name())
        print(msg.get_segment_id())
        print(msg.get_segment_size())
        print(msg.get_quality_id())
        print(msg.found())
        print(msg.get_url())
        '''

        print(msg.get_bit_length())

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(self.whiteboard.get_playback_segment_size_time_at_buffer())
        print(self.whiteboard.get_buffer())
        print(self.whiteboard.get_amount_video_to_play())
        print(self.whiteboard.get_max_buffer_size())
        print(self.whiteboard.get_playback_qi())
        print(self.whiteboard.get_playback_pauses())
        print(self.whiteboard.get_playback_buffer_size())
        print(self.whiteboard.get_playback_history())
        print(self.whiteboard.get_playback_buffer_size())

        current_playtime = int(msg.get_segment_id()) * int(msg.get_segment_size())
        p = msg.get_segment_size()

        t  = min(current_playtime, self.video_duration-current_playtime)
        t1 = max(t/2, 3*p) 

        Q_D_max = min(self.max_buffer_size, t1/p)
        V_D = (Q_D_max-1)/(self.vm + self.gama*p)

        print(self.whiteboard.get_max_buffer_size())

        print("self.whiteboard.get_playback_buffer_size(): " + str(self.whiteboard.get_playback_buffer_size()))
        print("self.whiteboard.get_playback_buffer_size(): " + str(len(self.whiteboard.get_playback_buffer_size())))
        print("self.player.get_buffer_size(): " + str((player.get_buffer_size())))
        
        if len(self.whiteboard.get_playback_buffer_size()) == 0:
            current_buffer_size = 0
        else:
            current_buffer_size = int(self.whiteboard.get_playback_buffer_size()[len(self.whiteboard.get_playback_buffer_size())][1])

        selected_qi = np.argmax((V_D*self.vm + V_D*self.gama*p-current_buffer_size)/self.qi)
        
        if selected_qi >= self.last_selected_qi:
            m_filter = self.qi/p <= max(self.last_throughput, self.qi[0]/p)
            m = self.qi[m_filter][-1]
            if m >= self.qi[selected_qi]:
                pass
            elif m < self.qi[self.last_selected_qi]:
                selected_qi = self.last_selected_qi
            else: 
                selected_qi = selected_qi + 1 if selected_qi + 1 < len(self.qi) else selected_qi

        self.last_selected_qi = selected_qi

        time.sleep(max((p * current_buffer_size - Q_D_max), 0))

        msg.add_quality_id(self.qi[selected_qi])

        self.request_time = time.perf_counter()
        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        t = time.perf_counter() - self.request_time
        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass