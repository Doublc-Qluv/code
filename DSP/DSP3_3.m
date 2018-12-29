Fs=64;

n=1/Fs;%ÖÜÆÚ
x=cos(8*pi*n)+cos(16*pi*n)+cos(20*pi*n);
y1=fft(x,64);
y2=fft(x,32);
y3=fft(x,16);
f1=(0:63)/32;
f2=(0:31)/16;
f3=(0:15)/8;
figure(1)
subplot(1,3,1);
stem(f1,abs(y1),'.');
%plot(n,y1);grid on;
subplot(1,3,2);stem(f2,abs(y2),'.');
subplot(1,3,3);stem(f3,abs(y3),'.');
