st=mstg;


ap=0.1;
as=60;
Fs=10000;
T=1/Fs;

%低通
fp=280;
fs=450;
wp=2*fp/Fs;
ws=2*fs/Fs;
[n1,wp]=ellipord(wp,ws,ap,as);
[B1,A1]=ellip(n1,ap,as,wp);
y1=filter(B1,A1,st);
figure(1);
subplot(2,1,1);
freqz(B1,A1);
subplot(2,1,2);
m=(0:length(y1)-1)/Fs;
plot(m,y1);
axis([0,0.08,-1,1])


%带通
fp1=450;
fs1=280;
fp2=560;
fs2=930;
fp=[fp1,fp2];
fs=[fs1,fs2];
wp=2*fp/Fs;
ws=2*fs/Fs;
[n2,wp]=ellipord(wp,ws,ap,as);
[B2,A2]=ellip(n2,ap,as,wp);
y2=filter(B2,A2,st);
figure(2);
subplot(2,1,1);
freqz(B2,A2);
subplot(2,1,2);
m=(0:length(y2)-1)/Fs;
plot(m,y2);
axis([0,0.08,-1,1])


%高通
fp=900;
fs=560;
wp=2*fp/Fs;
ws=2*fs/Fs;st=mstg;
[n3,wp]=ellipord(wp,ws,ap,as);
[B3,A3]=ellip(n3,ap,as,wp,'high');
y3=filter(B3,A3,st);
figure(3);
subplot(2,1,1);
freqz(B3,A3);
subplot(2,1,2);
m=(0:length(y3)-1)/Fs;
plot(m,y3);
axis([0,0.08,-1,1])


