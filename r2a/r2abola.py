# -*- coding: utf-8 -*-
"""

"""

from player.parser import *
from r2a.ir2a import IR2A
import time


class R2ABola(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.request_time = 0
        self.throughputs = []
        self.qi = []

    def handle_xml_request(self, msg):
        self.request_time = time.perf_counter()
        self.send_down(msg)

    def handle_xml_response(self, msg):
        # print(dir(msg))
        # print(msg.get_payload())
        # exit(0)
        parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = parsed_mpd.get_qi()

        t = time.perf_counter() - self.request_time
        self.throughputs.append(msg.get_bit_length() / t)

    def handle_segment_size_request(self, msg):
        msg.add_quality_id(self.qi[19])
        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        t = time.perf_counter() - self.request_time
        self.throughputs.append(msg.get_bit_length() / t)
        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass