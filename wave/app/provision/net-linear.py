#!/usr/bin/env python3
import yaml
import time
from pathlib import Path

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.clean import cleanup


BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.yaml"
SWITCH_FILE = Path("/tmp/ultimo_switch.txt")


def montar_linear(net, num_switches, delay):
    switches = []

    for i in range(num_switches):
        nome = f"s{i + 1}"

        sw = net.addSwitch(nome, cls=OVSSwitch, failMode='standalone')
        switches.append(sw)

        if i > 0:
            if delay:
                net.addLink(switches[i - 1], sw, delay=delay)
            else:
                net.addLink(switches[i - 1], sw)

    return switches


def main():
    cleanup()

    if not CONFIG_FILE.exists():
        raise Exception(f"Config file not found: {CONFIG_FILE}")

    with open(CONFIG_FILE) as f:
        cfg = yaml.safe_load(f)

    topologia = None
    for i in cfg:
        if 'topology' in i:
            topologia = i['topology']
            break

    if topologia is None:
        raise Exception("Topologia nao foi encontrada")

    num_switches = int(topologia['num_switches'])
    delay = topologia.get('delay')

    net = Mininet(controller=None,switch=OVSSwitch,link=TCLink,build=False)

    switches = montar_linear(net, num_switches, delay)

    net.build()
    net.start()
   
    SWITCH_FILE.write_text(switches[-1].name + "\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    net.stop()


if __name__ == "__main__":
    main()
