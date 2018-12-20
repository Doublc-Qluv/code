 #define WIN 4 /*定义窗口大小*/
 #define MAX 25/*定义发送报文计数最大值*/
 chan s_r=[10] of {mtype,byte,byte};/*定义发送端到接收端传输通道*/
 chan r_s=[10] of {mtype,byte,byte};/*定义接收端到发送端传输通道*/
 mtype={mesg, ack, err};/*定义消息类型*/
 proctype udt_sender() /*发送端进程*/
 {
    byte s,r,swl;/*s 为要发送的报文的序号,r 为确认报文的序号,swl 为滑动窗口下限*/
    swl = 0; /*窗口初始化*/
    do
        ::swl = swl;
        progress:s = MAXSEQ;wl; /*将要发送报文指针移到窗口头*/
        progress1: ifMAXSEQ;
            ::s_r!mesg(0,s)-> /*成功发送正确报文*/
            (swl<=s)->s = (s+1)%MAX;/*s 后移*/
                if
                ::goto progress1; /*在窗口内连续发送*/
                ::skip/*也可以不发送*/
                fi;
            ::s_r!err(s,0) -> /*发送的报文在传输通道中出错*/
            (swl<=s)->s = (s+1)%MAX;
                if
                ::goto progress1;
                ::skip
                fi;
            ::skip -> /*报文在传输通道中丢失*/
            (swl<=s)->s = (s+1)%MAX;
                if
                ::goto progress1;
                ::skip
                fi;
            fi;
        if
        ::timeout -> goto progress /*超时,从超时报文开始重发*/
        ::r_s?err(0,r) -> skip /*收到错误报文不工作*/
        ::r_s?ack(r,0) ->/*收到正确应答报文*/
            if
            ::(r<swl)->skip /*确认序号低于窗口下限*/
            ::(r>s) -> skip /*高于已发送报文最大值*/
            ::(swl<=r<=s) -> /*正确确认*/
            swl = r;/*移动窗口*/
            goto progress; /*继续发送*/
            fi;
        fi;
    od
 }
 proctype udt_receiver()/*接收端进程*/
 {
    byte t,es;/*t 为接收报文的序号,es 为期望收到的报文序号*/
    es = 0; /*初始化*/
    do
        ::s_r?mesg(0,t) ->/*收到正确报文*/
        if
        ::(t==es)-> /*收到报文为所期望报文*/
        progress2:es = (es + 1)%MAX;/*更新期望值*/
            if
            ::r_s!ack(es,0) /*发送确认*/
            ::r_s!err(0,es) /*发送的确认报文在传输通道中出错*/
            ::skip /*确认报文在传输通道中丢失*/
            fi
        ::(t!=es)->/*收到无效报文*/
            if
            ::r_s!ack(es,0)/*重发确认*/
            ::r_s!err(0,es) /*发送的确认报文在传输通道中出错*/
            ::skip /*确认报文在传输通道中丢失*/
            fi
        fi
        ::s_r?err(t,0)->/*收到的报文出错*/
            if
            ::r_s!ack(es,0)/*重发确认*/
            ::r_s!err(0,es) /*发送的确认报文在传输通道中出错*/
            ::skip /*确认报文在传输通道中丢失*/
            fi
    od
 }
 init
 { /*启动进程*/
    run udt_sender();
    run udt_receiver();
 }