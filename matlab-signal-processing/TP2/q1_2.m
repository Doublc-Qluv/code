for k=-3:1:3
    t=-2*pi+4*k*pi:0.001:2*pi+4*k*pi;
    y=((t+2*pi-4*k*pi).*stepfun(t,-2*pi+4*k*pi)-(t-2*pi-4*k*pi).*stepfun(t,2*pi+4*k*pi))/(2*pi)-2*stepfun(t,4*k*pi);
    plot(t,y);hold on;
end
grid on;
title('periodic extension');
xlabel('t');
ylabel(' ');