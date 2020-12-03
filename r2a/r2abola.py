# -*- coding: utf-8 -*-
"""

"""

from player.parser import *
from r2a.ir2a import IR2A


class R2ABola(IR2A):
    def __init__(self, id):
        pass

    @abstractmethod
    def handle_xml_request(self, msg):
        pass

    @abstractmethod
    def handle_xml_response(self, msg):
        pass

    @abstractmethod
    def handle_segment_size_request(self, msg):
        pass

    @abstractmethod
    def handle_segment_size_response(self, msg):
        pass

    @abstractmethod
    def initialize(self):
        SimpleModule.initialize(self)
        pass

    @abstractmethod
    def finalization(self):
        SimpleModule.finalization(self)
        pass