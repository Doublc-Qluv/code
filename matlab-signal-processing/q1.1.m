t=0:0.01:10;
y=heaviside(t);
plot(t,y);
axis([-1,10,0,1.5]);
xlabel('t');
ylabel('\epsilon(t)');
title('f(t)=\epsilon(t),ȡt = 0 ~ 10');