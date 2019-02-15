from PKCS7 import *
from s_box import *

def main():
    while(1):
      fix()
      f=open('m.txt','r')
      file_data = f.read()
      f.close()
      a = [ord(x) for x in file_data]
      rk=sm4_ex_key()
    #print rk
    #print a
      file_data_list=[]
      m=[]
      sel=input("-----0-exit\n-----1-enc\n-----2-dec\n")
      if sel==1:
    #enc
        for i in range(0,len(a),4):
            file_data_list.append(a[i]<<24|a[i+1]<<16|a[i+2]<<8|a[i+3])
    #print file_data_list
        for i in range(0,len(file_data_list),4):
            YY=sm4_enc(file_data_list[i],file_data_list[i+1],file_data_list[i+2],file_data_list[i+3],rk)
            print hex(YY)
            for j in range(16):
                shift=120-8*j
            #print shift
                sshift=(YY>>shift)&0xff
            #if sshift>16:
               # m.extend([hex(sshift)[:-1]])
           # else:
               # m.extend(['0x0'+hex(sshift)[2:-1]])
                m.append(chr(sshift))
        m=(''.join(m))
        f=open('c.txt','w')
        f.write(m)
        f.close()
      elif sel==2:
        #dec
        cc=[]
        f=open('c.txt','r')
        c_file_data=f.read()
        #print c_file_data
        a = [ord(x) for x in c_file_data]
    #print len(a)
        c_data_list=[]
        for i in range(0,len(a),4):
            c_data_list.append(a[i]<<24|a[i+1]<<16|a[i+2]<<8|a[i+3])
        for i in range(0,len(c_data_list),4):
            XX=sm4_dec(c_data_list[i],c_data_list[i+1],c_data_list[i+2],c_data_list[i+3],rk)
            print hex(XX)
            for j in range(16):
                shift=120-8*j
                shhift=(XX>>shift)&0xff
                cc.append(chr(sshift))
        cc=(''.join(cc))
        print cc
        g=open('mm.txt','w')
        g.write(cc)
        g.close()
      elif sel==0:
        break
      else:
        print 'error sel!'
main()
