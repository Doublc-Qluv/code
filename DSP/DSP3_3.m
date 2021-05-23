t=1/64;
n=0:30;
x=cos(pi*8*n*t)+cos(pi*16*n*t)+cos(pi*20*n*t);
y1=fft(x,16);
y2=fft(x,32);
y3=fft(x,64);
f1=(0:15)/16*30;
f2=(0:31)/32*30;
f3=(0:63)/64*30;

subplot(3,1,1);
stem(f1,abs(y1),'.');
subplot(3,1,2);
stem(f2,abs(y2),'.');
subplot(3,1,3);
stem(f3,abs(y3),'.');