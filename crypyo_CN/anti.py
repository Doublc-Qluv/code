from scapy.all import *
pcaps=rdpcap("./pktDump-icmp 嗅探.cap")


# ---- TCP Flags ----------
FIN='F'
SYN='S'
RST='R'
PSH='P'
ACK='A'
URG='U'
ECE='E'
CWR='C'
# ------Log--------------
arp_pattack_log= [0,0]
arp_pattack_src= []
dos_pattack_log= [0,0]
dos_pattack_src= []
icmp_pattack_log= [0,0]
icmp_pattack_src= []
packet=pcaps
flag=0
x=0
y=0
z=0
attack_ornot= [0,0,0,0]
timer=packet[0].time


for i in packet:
# arp_spoofing check
    if i.type==0x806:

# 判断是否有 padding
        if i.haslayer("Padding"):
            x+=1
            if x==1:
                 arp_pattack_log[0] =i.time
                 continue
            temp=arp_pattack_log[1]
            arp_pattack_log[1] =i.time-arp_pattack_log[0] +temp
            arp_pattack_log[0] =i.time
            arp_pattack_src.append(i.src)
            # 若在短时间内有大量 padding arp
            # 则视为被攻击
            if x%10==0:
                if timer-i.time<0.5:
                    for n in range(len(arp_pattack_src)):
                        if n==0:
                            continue
                        if arp_pattack_src[n] ==arp_pattack_src[n-1]:
                            flag+=1
                        if flag>=8:
                            flag=0
                            break
                    print("You have been Attack!!!")
                    attack_ornot[0] =1
                    attack_ornot[1] =1
                    continue
    # SSL DoS checking
    if i.type==0x800:
        # 被攻击的网关为 192.168.3.1
        if i.haslayer("TCP"):
            if int(i.dport) ==443 and i['IP'].dst=='192.168.3.1' and (i['TCP'].flags==PSH+ACKori['TCP'].flags==SYN+ACK):
                y+=1
                # print("src IP: ",i['IP'].src)
                dos_pattack_src.append(i['IP'].src)
                if y==1:
                    dos_pattack_log[0] =i.time
                    continue
                temp=dos_pattack_log[1]
                dos_pattack_log[1] =i.time-dos_pattack_log[0] +temp
                dos_pattack_log[0] =i.time
                
                if y%10==0:
                    if timer-i.time<0.5:
                        for n in range(len(dos_pattack_src)):
                            if n==0:
                                continue
                            if dos_pattack_src[n] == dos_pattack_src[n-1]:
                                flag+=1
                            if flag>=8:
                                flag=0
                                break
                        print("You have been Attack!!!")
                        attack_ornot[0] =1
                        attack_ornot[3] =1
                        continue
        # IP_Spoofing check
        elif i.proto==1:
            if i.haslayer("Padding") and i['ICMP'].type==8:
                z+=1
                if z==1:
                    icmp_pattack_log[0] =i.time
                    continue
                temp=icmp_pattack_log[1]
                icmp_pattack_log[1] =i.time-icmp_pattack_log[0] +temp
                if z%10==0:
                    if timer-i.time<0.5:
                        print("You have been Attack!!!")
                        attack_ornot[0] =1
                        attack_ornot[2] =1
                        continue
                    else:
                        timer=i.time
                icmp_pattack_log[0] =i.time


# --- check point -------
if attack_ornot[0] ==0:
    print("No problem!~")
elif attack_ornot[1] ==2:
    print("ARP SPOOFING ATTACK!!!!")
elif attack_ornot[2] ==1:
    print("IP SPOOFING ATTACK!!!!")
elif attack_ornot[3] ==1:
    print("SSL DOS ATTACK!!!!")