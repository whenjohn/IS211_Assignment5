#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS 211 - Assignment 5"""

# Completed program for the server simulation
class Server:
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task, process_time):
        self.current_task = new_task
        self.time_remaining = process_time
