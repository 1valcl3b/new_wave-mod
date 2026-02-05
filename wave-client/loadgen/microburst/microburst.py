#!/usr/bin/python3
# encoding: utf-8
'''
Created on Oct 6, 2024

@author: danilocb21
'''

__version__ = 0.1
__updated__ = '2024-12-10'

from scapy.all import *
import string
import random
import time
import argparse
import logging
import datetime

def generate_packets(src_ip, dst_ip, num_pkts):
    packets = []

    for _ in range(num_pkts):    
        sz_data = random.randint(10,255)
        data = ''.join(random.choices(string.ascii_letters + string.punctuation, k=sz_data))
        packets.append(Ether()/IP(src=src_ip, dst=dst_ip)/Raw(data))

    return packets


def send_burst(packets, packet_interval):
    logger = logging.getLogger("send_burst")

    logger.info("Time before sending packets: %s" % (datetime.datetime.now()))

    #send(packets, inter=packet_interval, verbose=False)
    sendp(packets, inter=packet_interval)
    # pps = len(packets) / packet_interval
    # sendpfast(packets, pps=pps)
    
    logger.info("Time after sending packets: %s" % (datetime.datetime.now()))



def run(args):
    logger = logging.getLogger("run")

    duration = args.duration
    now = datetime.datetime.now()
    end = now + datetime.timedelta(minutes=duration)

    src_ip = args.source_ip # Packets Source
    dst_ip = args.destination_ip # Packets Destiny

    # If no src_ip is passed,
    # it's used the ip from the local machine
    if src_ip is None:
        src_ip = get_if_addr(conf.iface)

    lambda_rate = 0.5
    while now < end:
        num_pkts = random.randint(10, 100)
        packet_interval = random.uniform(0.01, 0.1) # seconds
        packets = generate_packets(src_ip, dst_ip, num_pkts)

        logger.info("Num of packets %d\nInterval to send each packet: %.10f" % (num_pkts, packet_interval))

        send_burst(packets, packet_interval)

        burst_interval = random.expovariate(lambda_rate) # seconds
        time.sleep(burst_interval)
        now = datetime.datetime.now()
        

def main():

    logger = logging.getLogger("main")

    parser = argparse.ArgumentParser()
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    
    parser.add_argument('-V', '--version', action='version', version='%%(prog)s %s (%s)' % (program_version, program_build_date))
    parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
    parser.add_argument("-s", "--source_ip", dest="source_ip", help="set the source IP of the microburst")
    parser.add_argument("-d", "--destination_ip", dest="destination_ip", help="set the destination IP of the microburst", required=True)
    parser.add_argument("duration", type=float, help="set the duration of the experiment in minutes")

    args = parser.parse_args()

    if args.verbose is not None:
        if args.verbose >= 1:
            logging.basicConfig(filename='microburst.log',level=logging.DEBUG)
            # setup logger
            logger.debug("Enabling debug mode")

        else:
            # setup logger
            logging.basicConfig(filename='microburst.log',level=logging.INFO)

    run(args)


if __name__ == "__main__":
    main()