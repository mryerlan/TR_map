from netaddr import IPNetwork

from services.routers import get_info_routing_huawei
from utilities.database import TransmissionTypes, session, engine, Base, QuantitySites, TrMap


class Sites:
    def __init__(self, bts: str, ip: str, vlan: int, mac: str, mac_vrrp: str):
        self.bts = bts
        self.ipaddress = ip
        self.vlan = vlan
        self.mac = mac
        self.mac_vrrp = mac_vrrp
        self.ne = []
        self.ne_downlink = {}
        self.ne_uplink = {}
        self.router = {}
        self.tr_type = ''
        self.tr_type_lm = ''
        self.q_ty_chain = int
        self.q_ty_sites = []

    def __repr__(self):
        return f'Sites({self.bts}{self.q_ty_sites}{self.q_ty_chain}{self.tr_type}{self.tr_type_lm})'

    def find_ne(self, mws, bts):
        find_ne(mws, bts)

    def find_ne_inter(self):
        pass

    def find_fe(self):
        pass

    def find_true_ne(self):
        pass

    def find_tr_types(self):
        pass

    def find_routers(self):
        pass

    def find_tr_type_lm(self):
        pass

    def quantity_hops_in_chain(self):
        pass

    def quantity_sites(self):
        pass


# ############################## function part  #############################

def get_bts_info(csv_file) -> list:
    basestation = []
    with open(csv_file, "r") as file:
        for line in file:
            if len(line) > 35:
                bts, ip, vlan, mac, mac_vrrp = line.strip().split(";")
                bs = Sites(bts=bts, ip=ip, vlan=int(vlan), mac=mac, mac_vrrp=mac_vrrp)
                basestation.append(bs)
    return basestation


# ============================================ find fe info =====================================================


def find_ne_interfaces(bs, mws):
    for dev in mws:
        for bts in bs:
            if len(bts.ne) > 0:
                if bts.ne[-1] == dev.hostname:
                    for table in dev.mac_address_table:
                        vlan, mac, interface = table.split(', ')
                        if mac == bts.mac_vrrp:
                            bts.ne_uplink[dev.hostname] = interface
                        if mac == bts.mac:
                            bts.ne_downlink[dev.hostname] = interface


def find_fe(bs, mws):
    for bts in bs:
        path = len(bts.ne)
        for dev in mws:
            if len(bts.ne) > 0 and bts.ne[-1] == dev.hostname and \
                    ('WAN' or 'ISV3-1' or 'SHXA2-1' or 'SXA3-1' or 'MXXI5-1' in bts.ne_uplink[dev.hostname]):
                try:
                    fe = dev.interfaces[bts.ne_uplink[dev.hostname]]
                    bts.ne.append(fe)
                except KeyError as e:
                    print(f'{e} - {dev.hostname} --> {bts.ne_uplink} --> {dev.interfaces}')

            if len(bts.ne) > 0 and len(bts.ne) == path and dev.site in bts.ne[-1] and \
                    ('WAN' or 'ISV3-1' or 'SHXA2-1' or 'SXA3-1' or 'MXXI5-1' not in bts.ne_uplink[bts.ne[-1]]):
                i = 0
                for table in dev.mac_address_table:
                    vlan, mac, interface = table.split(', ')
                    if (mac == bts.mac_vrrp or mac == bts.mac) and int(vlan) == bts.vlan and dev.hostname not in bts.ne:
                        i += 1
                if i > 1:
                    bts.ne.append(dev.hostname)


def find_ne(bs, mws):
    for dev in mws:
        for bts in bs:
            for table in dev.mac_address_table:
                vlan, mac, interface = table.split(', ')
                if bts.mac == mac and bts.vlan == int(vlan) and (
                        'WAN' or 'ISV3' or 'SXA3-1' or 'SHXA2-1' or 'MXXI5-1' not in interface):
                    i = 0
                    for table1 in dev.mac_address_table:
                        vl, mc, inter = table1.split(', ')
                        if inter == interface:
                            i += 1
                    if i <= 6:
                        bts.ne.append(dev.hostname)

            if dev.sub_type == 'CN 210':
                if bts.bts in dev.hostname:
                    bts.ne.append(dev.hostname)
                    bts.ne_uplink[dev.hostname] = 'WAN 1/2/100'
                    bts.ne_downlink[dev.hostname] = 'LAN 1/2/9'


def find_true_ne(bs):
    for bts in bs:
        if len(bts.ne) > 1:
            for hostname in bts.ne:
                if bts.bts[:6] not in hostname:
                    bts.ne.remove(hostname)


def find_tr_types(bs, routing):
    sat = ['10.11.80.1/22', '10.11.136.1/21', '10.11.168.1/21', '10.10.65.0/24', '10.160.65.0/24', '10.10.66.0/24']
    ttk = ['10.130.228.16/28', '10.10.246.96/28', '10.130.229.52/32', '	10.130.228.20/32']  # networks transtelecom
    ktc = ['10.50.17.133/32']  # networks jusan mobile
    for bts in bs:
        for net in sat:
            if bts.ipaddress in IPNetwork(net):
                bts.tr_type = 'Satellite'
                break
        for net in ttk:
            if bts.ipaddress in IPNetwork(net):
                bts.tr_type = 'VPN TTK'
                break
        for net in ktc:
            if bts.ipaddress in IPNetwork(net):
                bts.tr_type = 'VPN KTC'
                break
        for line in routing:
            if str(line[2] == bts.vlan) and bts.tr_type == '':
                if bts.ipaddress in IPNetwork(line[0]):
                    if line[1] == 'Eth-Trunk6':
                        bts.tr_type = 'OWN'
                        break
                    if line[1] == 'Eth-Trunk7':
                        bts.tr_type = 'OWN'
                        break
                    if line[1] == 'Eth-Trunk2':
                        bts.tr_type = 'VPN'
                        break
                    if line[1] == 'Eth-Trunk15':
                        bts.tr_type = 'MBH'
                        break


def find_router(bs, routers):
    for bts in bs:
        for router in routers:
            for table in router.arp:
                if len(table) > 0:
                    ip, address, interface, vlan = table
                    if bts.mac == address and bts.ipaddress == ip:
                        bts.router[router.hostname] = interface


def find_tr_type_lm(bs):
    for bts in bs:
        for line in bts.ne_uplink.values():
            if 'WAN ' in line:
                bts.tr_type_lm = 'MW'
            elif 'ISV3' in line:
                bts.tr_type_lm = 'MW'
            elif 'SXA3-1' in line:
                bts.tr_type_lm = 'MW'
            elif 'SHXA2-1' in line:
                bts.tr_type_lm = 'MW'
            elif 'MXXI5-1' in line:
                bts.tr_type_lm = 'MW'
        if bts.tr_type_lm == '':
            bts.tr_type_lm = bts.tr_type


def quantity_hops_in_chain(bs, mws):
    for bts in bs:
        sites = []
        for dev in mws:
            for node in bts.ne:
                if node == dev.hostname:
                    sites.append(dev.site)
        bts.q_ty_chain = len(list(tuple(sites)))


def quantity_sites(bs, mws):
    for dev in mws:
        for bts in bs:
            for node in bts.ne:
                if node == dev.hostname:
                    for site in bs:
                        if site.bts == dev.site:
                            if bts.bts not in site.q_ty_sites:
                                site.q_ty_sites.append(bts.bts)


def load_data(bs):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    for bts in bs:
        tr_type = TransmissionTypes(site=bts.bts, tr_type_lm=bts.tr_type_lm, tr_type=bts.tr_type)
        session.add(tr_type)
        quantity = QuantitySites(site=bts.bts, quantity=len(bts.q_ty_sites), quantity_list=str(bts.q_ty_sites))
        session.add(quantity)
        tr_map = TrMap(site=bts.bts, chain=bts.q_ty_chain, fe=str(bts.ne), uplink=str(bts.ne_uplink))
        session.add(tr_map)
    session.commit()
    session.close()


def write_bs_info(bs, mw, routers):
    find_ne(bs, mw)
    find_true_ne(bs)
    find_true_ne(bs)
    find_true_ne(bs)
    find_ne_interfaces(bs, mw)
    for _ in range(13):
        find_fe(bs, mw)
        find_ne_interfaces(bs, mw)
    find_router(bs, routers)
    routing = list(tuple(get_info_routing_huawei()))
    find_tr_types(bs, routing)
    find_tr_type_lm(bs)
    quantity_hops_in_chain(bs, mw)
    quantity_sites(bs, mw)
    load_data(bs)
