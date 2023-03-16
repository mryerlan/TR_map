import os
from glob import glob

import environs
from datetime import date, timedelta, datetime
from utilities.ftp import open_file_from_ftp


date_now = date.today()
yesterday = date_now - timedelta(1)
date_soem = f'{datetime.now():%d%m%Y}'
date_ftp = f'{datetime.now():%Y%m%d}'
date_u2000 = f'{datetime.now():%Y_%m_%d}'
date_nce = f'{datetime.now():%Y-%m-%d}'

env = environs.Env()
env.read_env('.env')

# ------------------------------------------- FTP AUTH -----------------------------------------


FTP_SOEM_IP = env('FTP_IP')
FTP_SOEM_USERNAME = env('FTP_USERNAME')
FTP_SOEM_PASS = env('FTP_PASS')
FTP_SOEM_DIR = env('FTP_DIR')
FTP_DIR_INV = env('FTP_DIR_INV')
FTP_DIR_NCE = 'U2000/' + date_ftp

FTP_BSS_IP = env('FTP_BSS_IP')
FTP_BSS_USERNAME = env('FTP_BSS_USERNAME')
FTP_BSS_PASS = env('FTP_BSS_PASS')
FTP_BSS_DIR = env('FTP_BSS_DIR')

# ------------------------------------------- FILENAME -----------------------------------------


U2000_BS_MAC = 'U2000_MAC_TABLE_T2_' + date_u2000 + '.csv'
SOEM_NE_INV = 'soem16_NE_Inventory_' + date_ftp + '*'
SOEM_NE_ETH = 'soem16_Config_Data_MINI-LINK_TN_ETH_' + date_ftp + '*'
SOEM_NE_MMU = 'soem16_Config_Data_MINI-LINK_TN_MMU2B_C_' + date_ftp + '*'
NCE_NE_INV = 'NE Report_' + date_nce + '*'
NCE_NE_ARP = date_nce + '.zip'
NCE_NE_ETH = 'Cable_Report_' + date_nce + '*'
NCE_NE_ISV = 'Microwave_Link_Report_' + date_nce + '*'


# ------------------------------------------- DIR TXT -----------------------------------------

DIR_MLTN = glob('/Users/yerlanakhmetov/Documents/tr_map/telnet_ml_results/save_succ/*.txt')
DIR_ML6352 = glob('/Users/yerlanakhmetov/Documents/tr_map/ssh_ml_6352/save_succ/*.txt')
DIR_METRO = glob('/Users/yerlanakhmetov/Documents/tr_map/telnet_sp_results/save_succ/*.txt')
DIR_SP310 = glob('/Users/yerlanakhmetov/Documents/tr_map/telnet_sp310_results/save_succ/*.txt')
DIR_IP_CORE = glob('/Users/yerlanakhmetov/Documents/tr_map/ssh_routers_results/save_succ/*.txt')
DIR_MBH = glob('/Users/yerlanakhmetov/Documents/tr_map/ssh_mbh_results/save_succ/*.txt')
DIR_IP_CORE_ROUTING = glob('/Users/yerlanakhmetov/Documents/tr_map/routing_table/save_succ/*.txt')

#  ############################# files part  #############################

ddir = '/Users/yerlanakhmetov/PycharmProjects/tnp.ftp.daily.tr_map_report_v2/directory'
os.chdir(ddir)

u2000_bs = open_file_from_ftp(FTP_SOEM_IP, FTP_SOEM_USERNAME, FTP_SOEM_PASS, U2000_BS_MAC, FTP_SOEM_DIR)
soem_ne_inventory = open_file_from_ftp(FTP_SOEM_IP, FTP_SOEM_USERNAME, FTP_SOEM_PASS, SOEM_NE_INV, FTP_DIR_INV)
nce_ne_inventory = open_file_from_ftp(FTP_SOEM_IP, FTP_SOEM_USERNAME, FTP_SOEM_PASS, NCE_NE_INV, FTP_DIR_NCE)
nce_rtn_arp = open_file_from_ftp(FTP_SOEM_IP, FTP_SOEM_USERNAME, FTP_SOEM_PASS, NCE_NE_ARP, FTP_DIR_NCE)
soem_tn_eth = open_file_from_ftp(FTP_SOEM_IP, FTP_SOEM_USERNAME, FTP_SOEM_PASS, SOEM_NE_ETH, FTP_DIR_INV)
nce_rtn_eth = open_file_from_ftp(FTP_SOEM_IP, FTP_SOEM_USERNAME, FTP_SOEM_PASS, NCE_NE_ETH, FTP_DIR_NCE)
soem_ne_mmu = open_file_from_ftp(FTP_SOEM_IP, FTP_SOEM_USERNAME, FTP_SOEM_PASS, SOEM_NE_MMU, FTP_DIR_INV)
nce_ne_isv = open_file_from_ftp(FTP_SOEM_IP, FTP_SOEM_USERNAME, FTP_SOEM_PASS, NCE_NE_ISV, FTP_DIR_NCE)


URL_DB = env('URL_DB')
