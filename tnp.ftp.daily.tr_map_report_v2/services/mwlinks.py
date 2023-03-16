from dataclasses import dataclass


@dataclass
class MwLinks:
    links_id: str
    vendor: str
    frequency: int
    cur_tx_power: int
    cur_rx_power: int
    planned_tx_power: int
    planned_rx_power: int


def get_links_info(bs: list) -> list:
    links = []
    for bts in bs:
        for interface in bts.ne_uplink:
            if 'WAN' or 'ISV3-1' or 'SHXA2-1' or 'SXA3-1' or 'MXXI5-1' in interface.value:
                link = MwLinks(f'{interface.key}_{interface.value}')
                links.append(link)
    return links
