x=[ones(1,4)];
n=0:30;;
x1=(n>=0&n<=3).*(n+1)+(n>3&n<=7).*(8-n)+(n>7)*0;
x2=(n>=0&n<=3).*(4-n)+(n>3&n<=7).*(n-3)+(n>7)*0
y1=fft(x,16);
y2=fft(x,8);
f1=(0:15)/8;
f2=(0:7)/4;
subplot(3,2,1);
stem(f1,abs(y1),'.');
subplot(3,2,2);
stem(f2,abs(y2),'.');

y11=fft(x1,16);
y12=fft(x1,8);
subplot(3,2,3);
stem(f1,abs(y11),'.');
subplot(3,2,4);
stem(f2,abs(y12),'.');

y21=fft(x2,16);
y22=fft(x2,8);
subplot(3,2,5);
stem(f1,abs(y21),'.');
subplot(3,2,6);
stem(f2,abs(y22),'.');

