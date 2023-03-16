from services.basestations import get_bts_info, write_bs_info
from services.macrowaves import get_mw_info, write_mw_info
from settings import *
from services.routers import get_routers_info, write_info_routers


if __name__ == '__main__':

    start_time = datetime.now()
    current_date = start_time.strftime("%Y.%m.%d")
    current_time = start_time.strftime("%H.%M")

    bs = get_bts_info(U2000_BS_MAC)
    mw = get_mw_info(soem_ne_inventory, nce_ne_inventory)
    routers = get_routers_info(soem_ne_inventory, nce_ne_inventory)

    write_mw_info(mw)
    write_info_routers(routers)
    write_bs_info(bs, mw, routers)

    for i in bs:
        print(f'{i.bts};{i.tr_type_lm};{i.tr_type};{i.ne};{i.ne_uplink};{i.q_ty_sites};{i.q_ty_chain};'
              f'{len(i.q_ty_sites)}')

    for i in mw:
        if not i.log_without_arp and i.hostname != 'CN210':
            print(f'{i.hostname}')

    total_devices = len(mw)

    print(
        "\n"
        f"Total devices: {total_devices}\n"
        "-------------------------------------------------------------------------------------------------------\n"
        "hostname               ip address      comment\n"
        "---------------------- --------------- ----------------------------------------------------------------\n"
    )
    duration = datetime.now() - start_time
    duration_time = timedelta(seconds=duration.seconds)

    print("\n"
          "-------------------------------------------------------------------------------------------------------\n"
          f"elapsed time:..........{duration_time}\n"
          "-------------------------------------------------------------------------------------------------------")
