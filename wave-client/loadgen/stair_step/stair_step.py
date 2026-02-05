#!/usr/bin/python3
# encoding: utf-8
'''
Created on Sept 9, 2024

@author: danilocb21
'''

import logging
import argparse
import datetime
import time
import random
import subprocess
import os
import threading
import math
import csv
from collections import deque

__version__ = 0.1
__updated__ = '2024-09-09'
DEBUG = 0

command = [
           'vlc',
           '-I',
           'dummy',
           '--zoom=0.5',
           '--adaptive-logic=rate',
           '--random',
           '--loop'
           ]
log_file = '/home/vlc/logs/stair_step_wave.csv'

num_client = 0

alive = deque([])

# Start a process and stop it after args.length minutes
def start_process(args, FNULL):
    logger = logging.getLogger("start")

    # Start a new process
    logger.info('Starting new process')

    global command
    eff_command = command + [args.playlist]
    #eff_command = command

    pid = subprocess.Popen(eff_command, stderr=subprocess.STDOUT)
    logger.info('Starting new process pid = %s' % (pid))
    global num_client
    num_client += 1

    return pid


# Terminate the process
def terminate_process(pid):
    # setup logger
    logger = logging.getLogger("terminate")
    logger.info('Terminating process pid = %s' % (pid))
    pid.kill()
    #pid.wait()
    global num_client
    num_client -= 1

def run(args):

    # setup logger
    logger = logging.getLogger("run")

    # set the boundaries
    now   = datetime.datetime.now()
    half  = now + datetime.timedelta(minutes=args.duration / 2)
    end   = now + datetime.timedelta(minutes=args.duration)

    # Null file, just open it for future use
    FNULL = open(os.devnull, 'w')

    # stair step function
    if args.stair_step:
        I, J = args.stair_step.split(',')
        I = float(I)
        J = int(J)
        
        logger.info('Using stair step function with interval=%f jump=%d' % (I, J))


    # set up the main values
    global num_client
    num_client = 0

    global alive

    # time to sleep in between processes
    global sleep_secs
    sleep_secs = I # I is the interval between jumps, during this time the graph stays in a "plateau"

    # file used for create stair step wave graph
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Instances'])
        writer.writerow(
            [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(num_client)])

    # until we finish
    while (now < end):
        logger.debug('Clients active = %s' % (num_client))
        
        for _ in range(int(sleep_secs)):
            with open(log_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(num_client)])

        time.sleep(sleep_secs)
        
        if now < half - datetime.timedelta(seconds=I):
            for _ in range(J):
                #logger.info("Generating new process")
                last_pid = start_process(args, FNULL)
                alive.append(last_pid)
                #last_pid.wait()
                with open(log_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(num_client)])
        else:
            for _ in range(min(J, num_client)):
                #logger.info("Killing a process")
                terminate_process(alive[0])
                alive.popleft()
                with open(log_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(num_client)])

        # refresh the timer
        now = datetime.datetime.now()


def main():

    logger = logging.getLogger("main")

    parser = argparse.ArgumentParser()
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    parser.add_argument('-V', '--version', action='version', version='%%(prog)s %s (%s)' % (program_version, program_build_date))
    parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
    parser.add_argument("-s", "--stair_step", dest="stair_step", metavar='I,J', help="set the stair step behavior, with a interval of I seconds and a J jump")
    parser.add_argument("-l", "--playlist", dest="playlist", help="Set the playlist for the clients", required=True)

    # positional arguments (duration)
    parser.add_argument("duration", type=float, help="set the duration of the experiment in minutes")

    # Process arguments
    args = parser.parse_args()

    if args.verbose is not None:
        if args.verbose >= 1:
            logging.basicConfig(filename='stair_step.log',level=logging.DEBUG)
            # setup logger
            logger.debug("Enabling debug mode")

        else:
            # setup logger
            logging.basicConfig(filename='stair_step.log',level=logging.INFO)

    # main loop
    run(args)

    for pids in alive:
        terminate_process(pids)


# hook for the main function
if __name__ == '__main__':
    main()