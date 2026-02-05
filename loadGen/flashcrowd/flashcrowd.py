#!/usr/bin/env python3
'''
Created on May 05, 2021
@authors: leandro almeida (leandro.almeida@ifpb.edu.br) / Rafael Pasquini (rafael.pasquini@ufu.br)
'''

__version__ = 0.2
__updated__ = '2021-05-15'
DEBUG = 0

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
import signal
from collections import deque

# command used to start new instances of the application
command = [
           'vlc',
           '-I',
           'dummy',
           '--zoom=0.5',
           '--adaptive-logic=rate',
           '--random',
           '--loop',
           '--quiet',
           '-V',
           'x11'
           ]

num_client = 0

alive = deque([])
alive_Rnorm = deque([])

# Start a process and stop it after args.length minutes


def start_process(args):

    logger = logging.getLogger("start")

    # Start a new process
    logger.info('Starting new process')

    global command
    # eff_command = command + [args.playlist]
    eff_command = command

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
    global num_client
    num_client -= 1


def run(args):

    # setup logger
    logger = logging.getLogger("run")

    # shock_level used was equal 20 and n equal 4
    Rnorm, S, n = args.flashcrowd.split(',')
    # same values used on the paper "Managing flash crowds on the Internet", available in: https://ieeexplore.ieee.org/document/1240667
    Rnorm = int(Rnorm)
    S = int(S)
    n = int(n)

    # set up the main values
    global num_client
    num_client = 0

    # define queues to store proccess IDs
    global alive
    global alive_Rnorm

    #   file used for create flashcrowd wave graph
    with open('/home/vlc/logs/flashcrowd_wave.csv',
              mode='w', newline='') as file:

        writer = csv.writer(file)
        writer.writerow(['Time', 'Instances'])
        writer.writerow(
            [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(num_client)])

    # Rflash is a peak of a flash event. Rnorm is a normal load.
    # Shock_level defines the order of magnitude increase in the load.
    # Rflash is defined by equation: (Rnorm * Shock_level) - Rnorm
    # flashcrowd phenomenon is modeled by three parts:
    # ramp-up / sustained / ramp-down
    #       1) ramp-up is defined by equation: 1 / log10(1 + Shock_level)
    #       2) sustained is defined by equation:   log10(1 + Shock_level)
    #       3) ramp-down is defined by equation: n * log10(1 + Shock_level), where "n" is a constant.

    Rflash = (Rnorm * S) - Rnorm

    rampup = 1 / math.log10(1 + S)
    ru_sleep = (rampup*60) / Rflash

    sustained = math.log10(1 + S)
    st_sleep = sustained*60

    rampdown = n * math.log10(1 + S)
    rd_sleep = (rampdown*60) / Rflash

    for i in range(Rnorm):
        global command
        rnorm_command = command + [args.playlist]
        pid_Rnorm = subprocess.Popen(rnorm_command, stderr=subprocess.STDOUT)
        alive_Rnorm.append(pid_Rnorm)

        with open('/home/vlc/logs/flashcrowd_wave.csv',
                  mode='a', newline='') as file:

            writer = csv.writer(file)

            writer.writerow(
                [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(num_client)])

    # rumpup phase
    while num_client < Rflash:
        last_pid = start_process(args)
        alive.append(last_pid)

        for i in range(int(ru_sleep)):
            with open('/home/vlc/logs/flashcrowd_wave.csv',
                      mode='a', newline='') as file:

                writer = csv.writer(file)

                writer.writerow(
                    [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(num_client)])

        time.sleep(ru_sleep)

    # sustained phase
    for i in range(int(st_sleep)):
        with open('/home/vlc/logs/flashcrowd_wave.csv',
                  mode='a', newline='') as file:

            writer = csv.writer(file)

            writer.writerow(
                [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(num_client)])

    time.sleep(st_sleep)

    # rampdown phase
    for i in range(num_client):
        terminate_process(alive[0])
        alive.popleft()

        for i in range(int(rd_sleep)):
            with open('/home/vlc/logs/flashcrowd_wave.csv',
                      mode='a', newline='') as file:

                writer = csv.writer(file)

                writer.writerow(
                    [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(num_client)])
        time.sleep(rd_sleep)

    # kill instances from Rnorm load
    for i in range(Rnorm):
        terminate_process(alive_Rnorm[0])
        alive_Rnorm.popleft()


def main():

    logger = logging.getLogger("main")

    parser = argparse.ArgumentParser()
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)

    parser.add_argument('-V', '--version', action='version',
                        version='%%(prog)s %s (%s)' % (program_version, program_build_date))
    parser.add_argument("-v", "--verbose", dest="verbose", action="count",
                        help="set verbosity level [default: %(default)s]")
    parser.add_argument("-f", "--flashcrowd", dest="flashcrowd", metavar='Rnorm,S,n',
                        help="set the flashcrowd behavior, that varies with Rnorm (normal load), S (shock_level) and n (constant used in rampdown)")
    parser.add_argument("-l", "--playlist", dest="playlist",
                        help="Set the playlist for the clients", required=True)

    args = parser.parse_args()

    run(args)

    for pids in alive:
        terminate_process(pids)


# hook for the main function
if __name__ == '__main__':
    main()