n=0:30;
x=(n>=0&n<=13).*(n+1)+(n>13&n<27).*(27-n)+(n>=27)*0;
subplot(3,2,2);
stem(n,x,'.');
y=fft(x,1024);
m=abs(y);
f=(0:length(m)-1)/1024;
subplot(3,2,1);
plot(f,y);
axis([0,1,0,200])

y1=fft(x,32);
y2=ifft(y1);
f1=0:31;
subplot(3,2,3);
stem(f1,abs(y1),'.');
subplot(3,2,4);
stem(f1,y2,'.');

y3=y1(1:2:32);
y4=ifft(y3,16);
f2=0:15;
subplot(3,2,5);
stem(f2,y3,'.');
subplot(3,2,6);
stem(f2,y4,'.');



