t=0:0.01:10;
f1=heaviside(t)-heaviside(t-1);
f2=2*t.*f1;
y=conv(f1,f2)*0.01;
n=length(f1)+length(f2)-2;
x=0:0.01:n*0.01;
plot(x,y);
axis([-1,10,0,1]);
title('����');
xlabel('t');
ylabel('y(t)');