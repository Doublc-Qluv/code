# -*- coding: utf-8 -*-
'''
@Date: 2019-06-15 00:29:41
@Last Modified by: mykko
@Last Modified time: 2019-06-15 02:54:51
            '''
import re
import time
from scapy.all import *

log_path = 'debug_info\\var\\exportinfo\\logtmp'

def cap_count(): 
    ip_packet = {}
    packets = rdpcap("pktDump (2).cap") 
    for p in packets:
        try:
            if p.type==0x0800:
                ip_src = p[1].src
                if ip_src[:7] == '192.168' and ip_src != '192.168.3.1':
                    if not ip_packet.__contains__(ip_src): 
                        ip_packet[ip_src] =[{'start':0,'end':0,'flag':False},0,0] 
                        ip_packet[ip_src][0]['start'] = p.time
                    if p[1].dst == '192.168.3.1': 
                        ip_packet[ip_src][1] += 1 
                        ip_packet[ip_src][0]['end'] = p.time
                    else:
                        ip_packet[ip_src][2] += 1
        except: 
            pass
    return ip_packet 

def log_count():
    log_flag = []
    with open(log_path,'r',encoding='UTF-8') as f:
        for f_line in f.readlines(): 
            if '成功登录。' in f_line:
                ip_result = re.findall(r'\d+\.\d+\.\d+\.\d+',f_line)[0] 
                time_result = f_line.split()[0] + ' ' + f_line.split()[1] 
                time_result =time.mktime(time.strptime(time_result,'%Y-%m-%d %H:%M:%S')) 
                log_flag.append([ip_result,time_result])
    return log_flag

if __name__ == "__main__": 
    ip_packet = cap_count() 
    log_flag = log_count() 
    for i in ip_packet:
        print(i, ip_packet[i])
        s_time = ip_packet[i][0]['start'] 
        e_time = ip_packet[i][0]['end'] 
        for l in log_flag:
            if l[0] == i and l[1] <= e_time and l[1] >= s_time: 
                ip_packet[i][0]['flag'] = True
        if ip_packet[i][1] > 100 and not ip_packet[i][0]['flag']: 
            print(i)