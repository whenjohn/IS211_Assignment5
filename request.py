#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS 211 - Assignment 5"""

class Request:
    def __init__(self, time):
        self.timestamp = time
        self.pages = 1 # use to be random.randrange(1, 21). but pages is equiv to the simiar req in the given sec?

    def get_stamp(self):
        return self.timestamp

    def get_pages(self):
        return self.pages  #this just stores the number of pages per min set in init. just used to determine time_remaining

    def wait_time(self, current_time):
        return current_time - self.timestamp
