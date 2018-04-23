t=0:0.01:10;
f1(t)=heaviside(t+0)-heaviside(t-1);
f2(t)=2*t.*f1(t);
y=conv(f1(t),f2(t))*0.01;
n=length(f1(t))+length(f2(t))-2;
x=0:0.01:n*0.01;
plot(t,y);
axis([-1,10,0,1]);



t=-1:0.01:10;
y1=stepfun(t,0)-stepfun(t,1);
y2=2*t.*y1;
y=conv(y1,y2)*0.01;
n=length(y1)+length(y2)-2;
x=0:0.01:n*0.01;
plot(x,y,'r');
axis([-1,10,0,1]);
title('¾í»ý');
xlabel('t');
ylabel('y(t)');
