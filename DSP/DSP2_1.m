Fs=[1000;300;200];
Tp=[64/1000;64/300;64/200]
a=444.128;
b=50*sqrt(2)*pi;
w=50*sqrt(2)*pi;
n=0:63;
for i = 1 : 3
    t=1/Fs(i,1)
    x=a*exp(-1*b*t*n).*sin(w*t*n).*(t*n>0);
    y=fft(x,64);
    m=abs(y);
    f=(0:63)/Tp(i,1);
    subplot(3,2,2*i-1);
    stem(n,x,'.');
    subplot(3,2,2*i);
    plot(f,m);
end
