function st=mstg

N=1600;
Fs=10000;
T=1/Fs;
Tp=N*T;
t=0:T:(N-1)*T;
k=0:N-1;
f=k/Tp;
fc1=Fs/10;
fm1=fc1/10;
fc2=Fs/20;
fm2=fc2/10;
fc3=Fs/40;
fm3=fc3/10;

xt1=cos(2*pi*fm1*t).*cos(2*pi*fc1*t);
xt2=cos(2*pi*fm2*t).*cos(2*pi*fc2*t);
xt3=cos(2*pi*fm3*t).*cos(2*pi*fc3*t);

st=xt1+xt2+xt3;

fxt=fft(st,N);
%figure(1);
%subplot(2,1,1);
%plot(t,st);
%grid;xlabel('t/s');
%ylabel('s(t)');
%axis([0,0.08,min(st),max(st)]);
%title('(a)s(t)');
%subplot(2,1,2)
%stem(f,abs(fxt)/max(abs(fxt)),'.');
%axis([0,2000,0,1]);

