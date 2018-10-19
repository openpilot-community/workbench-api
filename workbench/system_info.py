import os
from collections import OrderedDict, namedtuple
import platform



def meminfo():
    '''Return a dictionary of memory info.

    Information is taken from '/proc/meminfo' and written to an ordered dictionary.
    '''
    meminfo = OrderedDict()

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()    
    return meminfo


def netdevs():
    '''Return bytes from network devices.  

    RX and TX bytes for each of the network devices 
    '''

    with open('/proc/net/dev') as f:
        net_dump = f.readlines()
    
    device_data = {}
    data = namedtuple('data',['rx','tx'])

    for line in net_dump[2:]:
        line = line.split(':')
        if line[0].strip() != 'lo':
            device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0), 
                                                float(line[1].split()[8])/(1024.0*1024.0))
    return device_data


def process_list():
    '''Return a list of processes
    '''
    pids = []

    for subdir in os.listdir('/proc'):
        if subdir.isdigit():
            pids.append(subdir)
    return pids


def get_system_info():
    """Return a dictionary containing information about the system. 
    
    Returned Items:
        avg_load: 
        uptime: How lond the system has been running
        system: 
        memory: Dictionary of memory info
        network: Dictionary of network devices 
    """

    uptime = None

    for index, item in enumerate(cpuinfo):
        print("    " + str(index) + ": " + item)

    with open("/proc/cpuinfo", "r")  as f:
        info = f.readlines()
        cpuinfo = [x.strip().split(":")[1] for x in info if "model name"  in x]
  
    with open("/proc/uptime", "r") as f:
        uptime = f.read().split(" ")[0].strip()
        uptime = int(float(uptime))

    with open("/proc/loadavg", "r") as f:
        avg_load = f.read().strip()
    
    system = platform.uname()
    memory = meminfo()
    #processes = process_list()
    network = netdevs()
  

    data = {
    "avg_load": avg_load,
    "uptime": uptime,
    "system": system,
    "memory": memory,
    "network": network
    }

    return data