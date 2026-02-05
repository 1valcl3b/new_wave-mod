#!/usr/bin/env python3
'''
Created on Sept 21, 2018

@author: pasquini
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
__updated__ = '2018-09-21'
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

num_client = 0

alive = deque([])

# Start a process and stop it after args.length minutes


def start_process(args, FNULL):
    logger = logging.getLogger("start")

    # Start a new process
    logger.info('Starting new process')

    global command
    eff_command = command + [args.playlist]
    # eff_command = command

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
    # pid.wait()
    global num_client
    num_client -= 1


def run(args):

    # setup logger
    logger = logging.getLogger("run")

    # set the boundaries
    start = now = datetime.datetime.now()
    end = now + datetime.timedelta(minutes=args.duration)

    # Null file, just open it for future use
    FNULL = open(os.devnull, 'w')

    # sinusoidal function
    if args.sinusoid:
        A, T = args.sinusoid.split(',')

        # The angular frequency  is aa scalar measure of rotation rate.
        # One revolution is equal to 2 radians, hence  = 2/T where
        # T is the period (measured in seconds),
        omega = 2.0 * math.pi / (float(T) * 60.0)
        A = float(A)
        logger.info('Using sine wave function with A=%f period=%f' %
                    (A, omega))

        # the amplitude must be smaller than the lambda
        assert (A < args.lambd)

    # general lambda
    lambd = args.lambd

    # set up the main values
    global num_client
    num_client = 0

    global alive

    # used to define poisson interarrival times - time to sleep in between processes
    global sleep_secs

    #   file used for create sinusoid wave graph
    with open('/home/vlc/logs/sinusoid_wave.csv',
              mode='w', newline='') as file:

        writer = csv.writer(file)
        writer.writerow(['Time', 'Instances'])
        writer.writerow(
            [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(num_client)])
    # until we finish
    while (now < end):

        if args.sinusoid:
            # The sine wave or sinusoid is a mathematical curve that describes
            # a smooth repetitive oscillation.
            # Its most basic form as a function of time (t) is:
            # y(t) = A * sin(2ft + ) = A * sin(t + )
            # where:
            #  -  is the phase (equal to 0)
            #  -  is evaluated at the previous step
            lambd = args.lambd + A * \
                math.sin(omega * (now - start).total_seconds())

        # Poisson process:
        # The time between each pair of consecutive events has an exponential
        # distribution with parameter  and each of these inter-arrival times
        # is assumed to be independent of other inter-arrival times.
        if args.poisson:
            sleep_secs = random.expovariate(lambd / 60.0)

        logger.debug('%s - Will sleep for %s sec' % (now, sleep_secs))
        logger.debug('Clients active = %s - lambda = %s' %
                     (num_client, math.ceil(lambd)))

        for i in range(int(sleep_secs)):
            with open('/home/vlc/logs/sinusoid_wave.csv',
                      mode='a', newline='') as file:

                writer = csv.writer(file)

                writer.writerow(
                    [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(num_client)])
                # file.write(str(num_client) + '\n')

        time.sleep(sleep_secs)

        if num_client < math.ceil(lambd):
            # logger.info("Generating new process")
            last_pid = start_process(args, FNULL)
            alive.append(last_pid)
            # last_pid.wait()
            with open('/home/vlc/logs/sinusoid_wave.csv',
                      mode='a', newline='') as file:
                writer = csv.writer(file)

                writer.writerow(
                    [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(num_client)])
                # file.write(str(num_client) + '\n')

        if num_client > math.ceil(lambd):
            # logger.info("Killing a process")
            terminate_process(alive[0])
            alive.popleft()
            with open('/home/vlc/logs/sinusoid_wave.csv',
                      mode='a', newline='') as file:
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
    parser.add_argument('-V', '--version', action='version',
                        version='%%(prog)s %s (%s)' % (program_version, program_build_date))
    parser.add_argument("-v", "--verbose", dest="verbose", action="count",
                        help="set verbosity level [default: %(default)s]")
    parser.add_argument("-s", "--sinusoid", dest="sinusoid", metavar='A,P',
                        help="set the sinusoidal lambda behavior, that varies with amplitude A on period P minutes around the lambda")
    parser.add_argument("-l", "--playlist", dest="playlist",
                        help="Set the playlist for the clients", required=True)

    parser.add_argument('--poisson', dest='poisson', action='store_true')
    parser.add_argument('--no-poisson', dest='poisson', action='store_false')
    parser.set_defaults(poisson=True)

    # positional arguments (duration, lambda)
    parser.add_argument("duration", type=float,
                        help="set the duration of the experiment in minutes")
    parser.add_argument(
        "lambd", type=float, help="set the (average) arrival rate of lambda clients/minute or normal level of functioning Rnorm for flash crowd")

    # Process arguments
    args = parser.parse_args()

    if args.verbose is not None:
        if args.verbose >= 1:
            logging.basicConfig(filename='sinusoid.log', level=logging.DEBUG)
            # setup logger
            logger.debug("Enabling debug mode")

        else:
            # setup logger
            logging.basicConfig(filename='sinusoid.log', level=logging.INFO)

    # main loop
    run(args)

    for pids in alive:
        terminate_process(pids)


# hook for the main function
if __name__ == '__main__':
    main()