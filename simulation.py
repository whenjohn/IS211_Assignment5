#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS 211 - Assignment 5"""

import csv
import urllib2
import argparse
import sys
import logging
import logging.handlers

import queue
import server
import request

def main():
    """Main function that runs at start of program.

    Args:
        --file (url): command line parameter of url
        --server (int): number of server(optional)

    Examples:
        >>> python simulation.py --file "http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv"
        Average Wait 2477.81 secs 4975 requests remaining.

        >>> python simulation.py --file "http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv" --servers 5000
        Average Wait 412.02 secs 3343 requests remaining.

    """
    # Set up logger named assignment2 with output level
    my_logger = logging.getLogger('assignment5')
    my_logger.setLevel(logging.ERROR)
    # Add the log message handler to the logger. output to file
    handler = logging.FileHandler('errors.log')
    my_logger.addHandler(handler)

    # Enable command-line arguments
    parser = argparse.ArgumentParser()
    # Add command-line argmuemnt
    parser.add_argument('--file')
    parser.add_argument('--servers', type=int)
    args = parser.parse_args()


    # Ensure that argument has returned URL
    if not args.file:
        print "Error URL argument missing"
        my_logger.error('Error file argument missing')
        sys.exit()
    else:
        req = urllib2.Request(args.file)

    # Retreive file from url
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as exception:
        print "Error {}".format(exception.code)
        my_logger.error('Error Download: {}'.format(exception.code))
        sys.exit()
    except urllib2.URLError as exception:
        print "Error {}".format(exception.reason)
        my_logger.error('Error Download: {}'.format(exception.reason))
        sys.exit()


    if  (args.servers and args.servers > 1):
        # run simulation on many server
        simulateManyServers(response, args.servers)

    else:
        # run simulation on one server
        simulateOneServer(response)


def simulateOneServer(file):
    """Simulates one server processing list of network requests

    Args:
        file (web response): CSV web response retrieved from argument

    Attributes:
        readCSV (csv object): Interable CSV object
        web_server (Server instance): Instance of Server Class
        server_queue (Queue instance): Instnace of Queue class
        waiting_times (list): List of wait times

    Returns:
        Returns the average wait time of the requests
        "Average Wait 2477.81 secs 4975 requests remaining."

    Examples:
    """
    readCSV = csv.reader(file)

    web_server = server.Server()
    server_queue = queue.Queue()
    waiting_times = []

    for row in readCSV:
        # The time when a request came in
        arrival_time = int(row[0])
        # The amount of time needed to process request
        process_amount = int(row[2])

        # create new tasks for the arrival-time
        server_request = request.Request(arrival_time)
        # add to queue
        server_queue.enqueue(server_request)

        # If the printer is not busy and a task is waiting
        if (not web_server.busy()) and (not server_queue.is_empty()):
            # Remove the next task from the print queue
            next_request = server_queue.dequeue()
            # add wait times to list, the current counter - arrival time.
            waiting_times.append(next_request.wait_time(arrival_time))
            # assign task to the printer. NEW. Second param is time remaining aka col 3
            web_server.start_next(next_request, process_amount)

        # incrimennt down time remaining based on start_next(process_amount)
        web_server.tick()

    average_wait = float(sum(waiting_times)) / len(waiting_times)
    print("Average Wait %6.2f secs %3d requests remaining." %(average_wait, server_queue.size()))


def simulateManyServers(file, num_servers):
    """Simulates multiple server processing list of network requests

    Args:
        file (web response): CSV web response retrieved from argument
        num_servers (int): Number of servers to simulate

    Attributes:
        readCSV (csv object): Interable CSV object
        server_queue (Queue instance): Instnace of Queue class
        waiting_times (list): List of wait times
        num_of_servers (int): number of servers
        web_server_list (list): list of server class instances
        count: counter

    Returns:
        Returns the average wait time of the requests
        "Average Wait 2477.81 secs 4975 requests remaining."

    Examples:
    """
    readCSV = csv.reader(file)

    server_queue = queue.Queue()
    waiting_times = []
    num_of_servers = num_servers

    web_server_list = []
    count = 0

    # Instantiate list of servers
    for i in range(num_of_servers):
        web_server_list.append(server.Server())

    for row in readCSV:
        # The time when a request came in
        arrival_time = int(row[0])
        # The amount of time needed to process request
        process_amount = int(row[2])

        # create new tasks for the arrival-time
        server_request = request.Request(arrival_time)
        # add to queue
        server_queue.enqueue(server_request)

        # check to determine which server bucket to put these requets in
        if count < num_of_servers:
            # If the printer is not busy and a task is waiting
            if (not web_server_list[count].busy()) and (not server_queue.is_empty()):
                # Remove the next task from the print queue
                next_request = server_queue.dequeue()
                # add wait times to list, the current counter - arrival time.
                waiting_times.append(next_request.wait_time(arrival_time))
                # assign task to the printer. NEW. Second param is time remaining aka col 3
                web_server_list[count].start_next(next_request, process_amount)

            # incrimennt down time remaining based on start_next(process_amount)
            web_server_list[count].tick()

            count += 1

        else:
            count = 0

            # If the printer is not busy and a task is waiting
            if (not web_server_list[count].busy()) and (not server_queue.is_empty()):
                # Remove the next task from the print queue
                next_request = server_queue.dequeue()
                # add wait times to list, the current counter - arrival time.
                waiting_times.append(next_request.wait_time(arrival_time))
                # assign task to the printer. NEW. Second param is time remaining aka col 3
                web_server_list[count].start_next(next_request, process_amount)

            # incrimennt down time remaining based on start_next(process_amount)
            web_server_list[count].tick()

    average_wait = float(sum(waiting_times)) / len(waiting_times)
    print("Average Wait %6.2f secs %3d requests remaining." %(average_wait, server_queue.size()))


# Run main if file directly executed
if __name__ == '__main__':
    main()
