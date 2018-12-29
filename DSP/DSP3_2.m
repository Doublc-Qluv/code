figure(1)
n=0:40;
x=cos(pi/4*n);
x1=cos(pi/4*n)+cos(pi/8*n);
y1=fft(x,16);
y2=fft(x,8);
f1=(0:15)/8;
f2=(0:7)/4;
subplot(2,2,1);
stem(f1,abs(y1),'.');xlabel('n');ylabel('X_4');title('FFT(x_4(n))  N=16');
subplot(2,2,2);
stem(f2,abs(y2),'.');xlabel('n');ylabel('X_4');title('FFT(x_5(n))  N=8');
axis([0,2,0,8]);

y11=fft(x1,16);
y12=fft(x2,8);
subplot(2,2,3);
stem(f1,abs(y11),'.');xlabel('n');ylabel('X_5');title('FFT(x_5(n))  N=16');
subplot(2,2,4);
stem(f2,abs(y12),'.');xlabel('n');ylabel('X_5');title('FFT(x_5(n))  N=8');
axis([0,2,0,8])

figure(2)
