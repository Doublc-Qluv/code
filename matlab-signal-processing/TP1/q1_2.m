t=0:0.01:10;
y=4*exp(-0.5*t).*cos(pi*t);
plot(t,y)
xlabel('t');
ylabel('f(t)');
title('f(t)=4e^{-0.5t}cos-(\pit),ȡt = 0~10');