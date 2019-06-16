#coding:utf-8
from scapy.all import *
from scapy_ssl_tls.ssl_tls import TLS
def ssl_dos_cat_test(pcap): ipdic={}
    attack=[]
    for p in pcap:
        if p.haslayer(SSL): 
            try:
                if p[SSL].records[0][TLSHandshakes].handshakes[0][TLSHandshake].type==16: 
                    try:
                        ipdic[p[IP].src]+=1 
                    except:
                        ipdic[p[IP].src]=1 
                    if ipdic[p[IP].src]>=3:
                        if p[IP].src not in attack: 
                            attack.append(p[IP].src)
                            print("there may be a ssl_dos,the attackeraddress is : "+p[IP].src) 
            except:
                pass
def Ddos_cat_test(pcap): 
    indict={}
    indetail={} 
    for p in pcap:
        if not p.haslayer(IP): 
            continue
        try: 
            indict[p[IP].dst]+=1
        except: 
            indict[p[IP].dst]=1
        try: 
            indetail[p[IP].dst][p[IP].src]+=1
        except: 
            try:
                indetail[p[IP].dst][p[IP].src]=1 
            except:
                indetail[p[IP].dst]={}
                indetail[p[IP].dst][p[IP].src]=1 for x in indict:
    for y in indetail[x]:
        if indetail[x][y]>=indict[x]*0.5:
            if indetail[x][y]>=1000:
                print("there may be a Ddos attack ,the attacker address\
                    is : {} which request {} for {} times".format(y,x,indetail[x][y]))

def show_info_test(pcap):
    l = float(len(pcap))
    tcpl = len(list(filter(lambda x:x[2].name=="TCP",pcap)))
    udpl = len(list(filter(lambda x:x[2].name=="UDP",pcap)))
    icmpl = len(list(filter(lambda x:x[2].name=="ICMP",pcap)))
    qt = l-tcpl-udpl-icmpl
    print('{:>7}\t:{:.1f}\t '.format('总包数',l))
    print('{:>7}\t:{:.1f} 占比:{:^.6%}'.format('TCP 包数',tcpl,tcpl/l) ) print('{:>7}\t:{:.1f}\t 占比:{:^.6%}'.format('UDP 包数',udpl,udpl/l) ) print('{:>7}:{:.1f}\t 占比:{:^.6%}'.format('ICMP 包数',icmpl,icmpl/l) ) print('{:>7}:{:.1f}\t 占比:{:^.6%}'.format('其他包数',qt,qt/l) )

def show_graph_test(pacp): pcap.plot(lambda x:x[2].name) pcap.plot(lambda x:x.src)
# # pcap=rdpcap(
if __name__ == "__main__":
    # pcap=rdpcap("DDOS.cap")
    name = input('请输入 pcap 文件的路径')
    pcap = rdpcap(name)
    tmp = list(globals().keys())
    fun = [str(name) for name in tmp if name.endswith('_test')] 
    print('可选的功能有:{}'.format(str(fun)))
    while True:
        chose = input('请输入你需要的操作') 
        if chose in fun:
            eval(chose+'(pcap)')
        else :
            break