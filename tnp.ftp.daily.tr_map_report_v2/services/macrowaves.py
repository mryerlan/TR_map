import re
import zipfile
from abc import ABC, abstractmethod

from settings import DIR_MLTN, nce_rtn_arp, DIR_ML6352, soem_tn_eth, nce_rtn_eth


class MW(ABC):

    def __init__(self, hostname, sub_type, site):
        self.hostname = hostname
        self.sub_type = sub_type
        self.site = site
        self.vendor = ''
        self.mac_address_table = []
        self.interfaces = {}  # '3-ISV3-1(AL8038MWA)': 'AL8038MWA'
        self.log_without_arp = True

    @abstractmethod
    def parse_txt(self, mws):
        """Parse txt files with mac address table"""
        raise NotImplementedError()

    @abstractmethod
    def parse_int(self, mws):
        """Parse interface alias and far end"""
        raise NotImplementedError()

    @abstractmethod
    def get_log_node_without_arp(self):
        """For sending log messages"""
        raise NotImplementedError()


class MiniLinkTN(MW):

    def __init__(self, hostname, sub_type, ip, site):
        MW.__init__(self, hostname, sub_type, site)
        self.ip = ip
        self.vendor = 'ML TN'

    def parse_txt(self, mws):
        parse_txt_files_ml_tn(mws)

    def parse_int(self, mws):
        parse_ne_int_ericsson(mws)

    def get_log_node_without_arp(self):
        if len(self.mac_address_table) == 0:
            self.log_without_arp = False


class OptixRTN(MW):

    def __init__(self, hostname, sub_type, site):
        MW.__init__(self, hostname, sub_type, site)
        self.vendor = 'Huawei'

    def parse_txt(self, mws):
        parse_txt_files_rtn(mws)

    def parse_int(self, mws):
        parse_ne_int_huawei(mws)

    def get_log_node_without_arp(self):
        if len(self.mac_address_table) == 0:
            self.log_without_arp = False


class MiniLink6352(MW):
    def __init__(self, hostname, sub_type, ip, site):
        MW.__init__(self, hostname, sub_type, site)
        self.ip = ip
        self.vendor = 'ML6352'

    def parse_txt(self, mws):
        parse_txt_files_ml6352(mws)

    def parse_int(self, mws):
        parse_ne_int_ericsson(mws)

    def get_log_node_without_arp(self):
        if len(self.mac_address_table) == 0:
            self.log_without_arp = False


def get_mw_info(soem_csv_file, nce_ne_inv) -> list:
    microwave = []
    with open(soem_csv_file, 'r') as file:
        for line in file:
            if 'NodeName' not in line:
                _, _, sub_type, ip, _, _, _, _, hostname, *_ = line.strip().split(",")
                if sub_type in ["AMM 6p C", "AMM 2p B", "AMM 20p B", "CN 210", "AMM 20p", "AMM 6p B", "MINI-LINK 6693",
                                "MINI-LINK 6655"]:
                    site = hostname[3:9]
                    ml = MiniLinkTN(hostname=hostname, sub_type=sub_type, ip=ip, site=site)
                    microwave.append(ml)

                if sub_type in ["MINI-LINK 6352"]:
                    site = hostname[:6]
                    ml = MiniLink6352(hostname=hostname, sub_type=sub_type, ip=ip, site=site)
                    microwave.append(ml)

    with open(nce_ne_inv, 'r') as file:
        for line in file:
            if 'Ne Name' not in line and len(line) > 65:
                ne_name, ne_type, ip, *_ = line.strip().split(",")
                if ne_type in ["OptiX RTN 950A", "OptiX RTN 905", "OptiX RTN 980", "OptiX RTN 380H", "OptiX RTN 310"]:
                    site = ne_name[:6]
                    rtn = OptixRTN(hostname=ne_name, sub_type=ne_type, site=site)
                    microwave.append(rtn)

    return microwave


def parse_txt_files_ml_tn(dev: MiniLinkTN):
    pattern = re.compile(r'(\d*)\s(\S{17})\s\w*\s*\d*\s(\w{3})\s*(\S{5,})')
    # '3000', '60:08:10:18:5b:65', 'WAN', '1/1/100'
    for file in DIR_MLTN:
        ip = file.split('/')[-1].replace('.txt', '')
        if ip == dev.ip:
            with open(file) as file_in:
                text = file_in.read()
            reg = re.findall(pattern, text)
            for line in reg:
                vlan, mac, types, interface = line
                dev.mac_address_table.append(f'{vlan}, {mac}, {types} {interface}')


def parse_txt_files_rtn(dev: OptixRTN):
    result = zipfile.ZipFile(nce_rtn_arp, 'r')
    if dev.vendor == 'Huawei':
        for filename in result.namelist():
            hostname = re.findall(r"SelfMacAddress/.{10}/(.*)\.", filename)
            if len(hostname) > 0:
                if dev.hostname == hostname[0]:
                    for line in result.read(filename).split(b"\n1"):
                        lines = str(line).replace("b'\\t", "").replace("[", "\\t").split("\\t")
                        if len(lines) == 4 and "b'Service ID" not in lines:
                            lines[1] = lines[1].replace("-", ":").lower()
                            lines = f'{lines[0]}, {lines[1]}, {lines[2]}'
                            dev.mac_address_table.append(lines)
#                           '1002, 04:f9:38:a0:96:4c, 1-ISV3-1(AT7202MWA)'


def parse_txt_files_ml6352(dev: MiniLink6352):
    pattern = re.compile(r'(\d*)\s*\|\s*(\S{17})\s\|\s*(\S*\s\d*)')
    if dev.vendor == 'ML6352':
        for file in DIR_ML6352:
            fl = file.split('/')[-1].replace('.txt', '')
            if fl == dev.ip:
                with open(file) as file_in:
                    text = file_in.read()
                reg = re.findall(pattern, text)
                for line in reg:
                    ls = f'{line[0]}, {line[1]}, {line[2]}'
                    dev.mac_address_table.append(ls)
#                   '1730, 00:00:5e:00:01:c8, LAN 3'


def parse_ne_int_ericsson(dev: MiniLinkTN):
    with open(soem_tn_eth, 'r') as file:
        for line in file:
            if 'WAN' in line:
                _, _, _, interface, _, _, _, _, _, _, _, _, _, _, fename, *_, nename = line.strip().split(",")
                if dev.hostname == nename and dev.vendor == 'ML TN':
                    dev.interfaces[interface] = fename
                if dev.hostname == nename and dev.vendor == 'ML6352':
                    dev.interfaces['WAN '] = fename


def parse_ne_int_huawei(dev: OptixRTN):
    with open(nce_rtn_eth, 'r') as file:
        for line in file:
            if len(line) > 40:
                _, _, _, _, _, ne, interface, fe, fe_interface, *_ = line.strip().replace('"', "").split(',')
                if dev.hostname == ne:
                    dev.interfaces[interface] = fe
                elif dev.hostname == fe:
                    dev.interfaces[fe_interface] = ne


def write_mw_info(microwave: list):
    for mws in microwave:
        mws.parse_txt(mws)
        mws.parse_int(mws)
        mws.get_log_node_without_arp()
