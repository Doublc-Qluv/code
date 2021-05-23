%MRC_scheme.m 
%接收分集-MRC 
clear,clf 
tic 
L_frame=130; 
N_packet=4000; 
b=2;               %设置1/2/3/4对应BPSK/QPSK/16-QAM/64-QAM 
SNRdBs=[0:2:20];%0 2 4 6 8 10 12 14 16 18 20 
sq2=sqrt(2); 
for iter=1:4        %修改 
    if iter==1 
          NT=1; 
          NR=1;      %SISO 
          gs='-kx'; 
    elseif iter==2 
          NT=1; 
          NR=2;      %1*2 
          gs='-^'; 
    elseif iter==3    %添加1*3的情况 
           NT=1;      % 
           NR=3;      % 
           gs='-b*';  % 
    else 
          NT=1; 
          NR=4;      %1*4 
          gs='-ro'; 
    end 
    sq_NT=sqrt(NT);  %对发送天线数求平方根 
    for i_SNR=1:length(SNRdBs)   %length(SNRdBs)的长度是11  每次循环i_SNR=1 2 3 4 5 6 7 8 9 10 11 
        SNRdB=SNRdBs(i_SNR);     %取SNRdBs第i_SNR个元素  每次循环SNRdB的值都不一样 
        sigma=sqrt(0.5/(10^(SNRdB/10)));%sigma=sqrt(1/2SNR) 
        for i_packet=1:N_packet   %循环次数 
            symbol_data=randint(L_frame*b,NT);%  260*1 矩阵 
            [temp,sym_tab,P]=modulator(symbol_data.',b);  %调用Modulator函数进行 进行信号调制  %symbol_data.'对symbol_data进行转置1*260阶矩阵 
            X=temp.'; 
            Hr=(randn(L_frame,NR)+j*randn(L_frame,NR))/sq2;%%每次循环生成信道矩阵Hr：(130x1)、（130x2）、（130x3）、（130x4）阶矩阵 
            H=reshape(Hr,L_frame,NR);% 
            Habs=sum(abs(H).^2,2);  %abs(H).^2 求矩阵H的各元素的模平方 %sum(A,2)表对矩阵A进行按行求和 
            Z=0; 
            for i=1:NR    %NR表示接收天线数 
                R(:,i)=sum(H(:,i).*X,2)/sq_NT+sigma*(randn(L_frame,1)+j*randn(L_frame,1)); %%%%%%%%%%%%%%%%%% 
                   Z=Z+R(:,i).*conj(H(:,i));   %conj（）求复数的共轭   
            end 
            for m=1:P   %P=4 
                d1(:,m)=abs(sum(Z,2)-sym_tab(m)).^2+(-1+sum(Habs,2))*abs(sym_tab(m))^2;    %%%%%%%%%%%%%%%%%%%%                              
            end 
            [y1,i1]=min(d1,[],2);%返回的是列向量，y1存的是每行最小值，i1存的是每行最小值所在的列数 
            Xd=sym_tab(i1).'; 
            temp1=X>0;%%%%%%%% 
            temp2=Xd>0;%%%%%%%% 
            noeb_p(i_packet)=sum(sum(temp1~=temp2)); 
        end 
        BER(iter,i_SNR)=sum(noeb_p)/(N_packet*L_frame*b);%将每次循环的结果存到BER(iter,i_SNR)中 
    end  
    semilogy(SNRdBs,BER(iter,:),gs) 
    hold on 
    axis([SNRdBs([1 end]) 0.5*10^(-4) 1e0]) 
end 
title('BER performacede of MRC Scheme') 
xlabel('SNR[dB]'),ylabel('BER') 
grid on 
set(gca,'fontsize',9) 
legend('SISO','MRC(Tx:1,Rx:2)','MRC(Tx:1,Rx:3)','MRC(Tx:1,Rx:4)',1)
toc