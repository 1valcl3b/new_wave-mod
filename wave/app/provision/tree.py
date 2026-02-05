#!/usr/bin/env python3
import yaml
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink, Intf
from mininet.cli import CLI
from mininet.clean import cleanup
from pathlib import Path

def montar_arvore(net, depth, branching, max_switches, delay):
    contador = 0
    switches = []

    def adicionar(pai=None, nivel=0):
        nonlocal contador
        if contador >= max_switches:
            return

        nome = f"s{contador + 1}"

        sw = net.addSwitch(
            nome,
            cls=OVSSwitch,
            failMode='standalone'
        )

        switches.append(sw)
        contador += 1

        if pai:
            if delay: 
                net.addLink(pai, sw, delay=delay)
            else:
                net.addLink(pai, sw)

        if nivel < depth - 1:
            for _ in range(branching):
                if contador < max_switches:
                    adicionar(sw, nivel + 1)

    adicionar()
    return switches

    # if switches:
    #     Intf('br0', node=switches[0])    
    #     Intf('br1', node=switches[-1])   

   


def main():
    cleanup()

    with open("config.yaml") as f:
        cfg = yaml.safe_load(f)

    topologia = None
    for i in cfg:
        if 'topology' in i:
            topologia = i['topology']
            break

    if topologia is None:
        raise Exception("Topologia nao foi encontrada")

    depth = int(topologia['depth'])
    branching = int(topologia['branching'])
    max_switches = int(topologia['max_switches'])
    delay = topologia.get('delay')

    net = Mininet(controller=None,switch=OVSSwitch,link=TCLink,build=False)

    switches = montar_arvore(net,depth=depth,branching=branching,max_switches=max_switches,delay=delay)

    # montar_arvore(
    #     net,
    #     depth=depth,
    #     branching=branching,
    #     max_switches=max_switches,
    #     delay=delay
    # )

    net.build()
    net.start()    

    # Path("/tmp/ultimo_switch").write_text(switches[-1].name + "\n")
    
    with open("/tmp/ultimo_switch.txt", "w") as f:
         f.write(switches[-1].name + "\n")
    
    #CLI(net)
    

    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    net.stop()


if __name__ == "__main__":
    main()