function [F] = q1_1_function(n)
syms t;
s1=(t+2*pi)/(2*pi);
s2=(t-2*pi)/(2*pi);
y1=s1.*exp(-0.5i*n.*t);
y2=s2.*exp(-0.5i*n.*t);
F=(int(y1,t,-2*pi,0)+int(y2,t,0,2*pi))/(4*pi);
end