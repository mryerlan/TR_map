import re
from abc import ABC, abstractmethod

from settings import *


class Routers(ABC):
    def __init__(self, hostname: str, ip: str, subrack: str, site, vendor: str):
        self.hostname = hostname
        self.ip = ip
        self.subrack = subrack
        self.site = site
        self.vendor = vendor
        self.arp = []

    def __repr__(self):
        return f'Routers({self.hostname}, {self.ip}, {self.subrack}, {self.site}, {self.vendor})'

    @abstractmethod
    def get_info_arp(self, device):
        """Parse information about ARP for a given device"""
        raise NotImplementedError()

    @abstractmethod
    def get_info_routing(self, device):
        """Parse information about routing table for a given device """
        raise NotImplementedError()


class Ericsson(Routers):
    def __init__(self, hostname, ip, subrack, site, vendor):
        Routers.__init__(self, hostname, ip, subrack, site, vendor)

    def get_info_arp(self, device):
        get_info_arp_r6000(device)

    def get_info_routing(self, device):
        pass


class Huawei(Routers):

    def __init__(self, hostname, ip, subrack, site, vendor):
        Routers.__init__(self, hostname, ip, subrack, site, vendor)

    def get_info_arp(self, device):
        get_info_arp_huawei(device)

    def get_info_routing(self, device):
        pass


def get_info_arp_r6000(devs: Ericsson):
    pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)\s+(\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2})\s+\S+\s+\S+\s+('
                         r'?:(\d+/\d+)\s+\S+\s+(\d+)|(\w+\s+\S+\s+\d+)\s+\S+\s+(\d+))')
    for file in DIR_METRO:
        ip = file.split('/')[-1].replace('.txt', '')
        if ip == devs.ip:
            with open(file) as file_in:
                text = file_in.read()
            reg = re.findall(pattern, text)
            for line in reg:
                if line[2] == '':
                    ip, mac, *_, interface, vlan = line
                    devs.arp.append([ip, mac, interface, vlan])
                else:
                    ip, mac, interface, vlan, *_ = line
                    devs.arp.append([ip, mac, interface, vlan])


def get_info_arp_huawei(devs: Huawei):
    pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)\s+(\w{4}-\w{4}-\w{4})\s+\d+\s+\S*\s*(\S*)\.(\d*)')
    for file in DIR_IP_CORE:
        ip = file.split('/')[-1].replace('.txt', '')
        if ip == devs.ip:
            with open(file) as file_in:
                text = file_in.read()
            reg = re.findall(pattern, text)
            for line in reg:
                ip, mac_address, interface, vlan = line
                mac = mac_address.replace("-", "")
                address = f"{mac[:2]}:{mac[2:4]}:{mac[4:6]}:{mac[6:8]}:{mac[8:10]}:{mac[10:]}"
                devs.arp.append([ip, address, interface, vlan])


def get_info_routing_huawei() -> list:
    routing_table = []
    pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+/\d+).+(Eth-Trunk\d+)\.(\d*)')
    for file in DIR_IP_CORE_ROUTING:
        with open(file) as file_in:
            text = file_in.read()
        reg = re.findall(pattern, text)
        for line in reg:
            prefix, trunk, vlan = line
            if trunk in ['Eth-Trunk6', 'Eth-Trunk7', 'Eth-Trunk2', 'Eth-Trunk15']:
                routing_table.append([prefix, trunk, vlan])
    return routing_table


def get_routers_info(soem_csv_file, nce_ne_inv) -> list:
    devs = []
    with open(soem_csv_file, 'r') as file:
        for line in file:
            if 'NodeName' not in line:
                _, _, sub_type, ip, _, _, _, _, hostname, *_ = line.strip().split(",")
                if sub_type in ['6672', '6471/1', '6675']:
                    site = hostname[4:10]
                    device = Ericsson(hostname=hostname, subrack=f'Router {sub_type}', ip=ip, vendor='Ericsson',
                                      site=site)
                    devs.append(device)

    with open(nce_ne_inv, 'r') as file:
        for line in file:
            if 'Ne Name' not in line and len(line) > 65:
                ne_name, ne_type, ip, *_ = line.strip().split(",")
                if ne_type in ["NE40E-X8A(V8)", "CX600-X3", "ATN950B", "NetEngine 8000 M14"]:
                    device = Huawei(hostname=ne_name, subrack=ne_type, ip=ip, vendor='Huawei', site=hostname)
                    devs.append(device)

    return devs


def write_info_routers(devs):
    for device in devs:
        device.get_info_arp(device)
