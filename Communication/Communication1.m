clc
clear all
close all
frmLen = 100;       % frame length  
numPackets = 100;  % number of packets
EbNo = 0:2:10;      % Eb/No varying to 20 dB
N = 2;              % maximum number of Tx antennas
M = 4;              % maximum number of Rx antennas
clr = ['r','b','g','k','m','c']; % Cell array of colros.
c=1;
mrkr = ['*','o','s','d','+','x'];
% and set up the simulation.
   
% Create a local random stream to be used by random number generators for
% repeatability.
hStr = RandStream('mt19937ar', 'Seed', 55408);
 
hh = gcf; grid on; hold on;
set(gca, 'yscale', 'log', 'xlim', [0, 10], 'ylim', [1e-4 1]);
xlabel('Eb/No (dB)'); ylabel('BER'); set(hh,'NumberTitle','off');
set(hh, 'renderer', 'zbuffer'); set(hh,'Name','MQAM_BER');
title('Alamouti Scheme with M-QAM Modulation');
 
data=zeros(frmLen,1);demod22=data;demod11=data;demod21=data;
error11 = zeros(1, numPackets); BER11 = zeros(1, length(EbNo));
error21 = error11; BER21 = BER11; error22 = error11; BER22 = BER11; 
 
% Create MQAM mod-demod objects
p=[4];%16 32 64];
% Create MPSK mod-demod objects
%p=[2 4 8 16 32 64];
for ii=1:length(p)
P =p(ii);% modulation order
h = modem.qammod('M', P, 'SymbolOrder', 'Gray');
d = modem.qamdemod('M', P, 'SymbolOrder', 'Gray');
%h = modem.pskmod('M', P, 'SymbolOrder', 'Gray');
%d = modem.pskdemod('M', P, 'SymbolOrder', 'Gray');
 
k=log2(P);  %bits per symbol
Set=[0:P-1]'; 
Smap=modulate(h,Set);
Eav=(Smap'*Smap)/P;
K=2;
snr=EbNo+10*log10(k);
for i=1:length(EbNo)
  NF=10^(EbNo(i)/10)*k;
  S=sqrt(N*Eav/(2*NF));
  for PacketIdx=1:numPackets
   data = randi(hStr, [0 P-1], frmLen, 1);   % data vector per user 
   tx=modulate(h,data);
    
   %Simulate channel using toolbox mimochan
   %chan = mimochan(N, M, 1e-4, 0);
   %chan.KFactor = 0;    
   %H(:,:)=chan.PathGains;
   %chan.ResetBeforeFiltering = 0;
   %chan.StorePathGains = 1;
   %channel assumed const over a frame
    
   for idx=1:N:frmLen
    s1 = tx(idx); s2 = tx(idx+1);
    tx2 = [s1 -conj(s2); s2 conj(s1)];
    %w =S*(randn(2,M) + 1i*randn(2,M));  %Get noise
    H=(randn(M,N) + 1i*randn(M,N))/sqrt(2);  %Channel Gain Matrix Rayleigh
    %H = sqrt(K/(K+1)) + sqrt(1/(K+1))*((randn(N,M)+1i*randn(N,M))/sqrt(2));%Rician
    r11=awgn(H(1,:).*[s1 s2],snr(i),'measured');%+w(1,:)/sqrt(N);%H(1,:).*[s1 s2]+w(1,:)/sqrt(N);  %Eav is for 1 antenna
    r21=awgn(H(1,:)*tx2,snr(i),'measured');%H(1,:)*tx2+w(1,:);
    r22=awgn(H*tx2,snr(i),'measured');%H*tx2+w;
 
    %Demodulate
    %Detecting s1 and s2, minimize decision metric
    S1=0; S2=0; Hnorm=0;
    for j=1:M,
        S1 = S1 + r22(j,1)*H(j,1)' + r22(j,2)'*H(j,2);
        S2 = S2 + r22(j,1)*H(j,2)' - r22(j,2)'*H(j,1);
        Hnorm = Hnorm + H(j,:)*H(j,:)';
    end
         
    S1=S1/Hnorm;
    S2=S2/Hnorm;
    demod22(idx)=demodulate(d,S1);
    demod22(idx+1)=demodulate(d,S2);
    Hnorm11=(H(1,1)'*H(1,1));
    Hnorm21=(H(2,1)'*H(2,1));
     
    S1=r11(1,1)*conj(H(1,1))/Hnorm11;
    S2=r11(1,2)*conj(H(1,2))/Hnorm21;
    demod11(idx)=demodulate(d,S1); 
    demod11(idx+1)=demodulate(d,S2); 
     
    Hnorm2=Hnorm11+Hnorm21;
    S1=r21(1,1)*conj(H(1,1))+ conj(r21(1,2))*H(1,2);
    S2=r21(1,1)*conj(H(1,2))- conj(r21(1,2))*H(1,1);
    demod21(idx)=demodulate(d,S1/Hnorm2);
    demod21(idx+1)=demodulate(d,S2/Hnorm2);
     
  end
  error22(PacketIdx) = biterr(demod22, data);
  error11(PacketIdx) = biterr(demod11, data);
  error21(PacketIdx) = biterr(demod21, data);
  end
  BER22(i)=sum(error22)/(frmLen*numPackets*k);
  BER11(i)=sum(error11)/(frmLen*numPackets*k);
  BER21(i)=sum(error21)/(frmLen*numPackets*k);
end
semilogy(EbNo, BER11, 'color',clr(c),'marker',mrkr(c));
c=c+1;
semilogy(EbNo, BER21, 'color',clr(c),'marker',mrkr(c));
c=c+1;
semilogy(EbNo, BER22, 'color',clr(c),'marker',mrkr(c));
c=c+1;
end
legend('1X1','2X1','2X2');
%legend('2X2 M=4','2X2 M=16','2X2 M=32','2X2 M=64');
%legend('2X2 M=4');