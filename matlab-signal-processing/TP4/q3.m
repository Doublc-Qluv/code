clear all;
syms s t
%构造系统函数
H(s)= s / (s^2 + 3*s + 2);
figure(1);%系统的冲激响应
fprintf('系统的冲激响应');
F1(s) = laplace(dirac(t));
h(t) = ilaplace(H(s) * F1(s))
ezplot(t,h(t));
axis([0,5,-1,1.5]);
grid on;
figure(2);%系统的阶跃响应
fprintf('系统的阶跃响应');
F2(s) = laplace(heaviside(t));
g(t) = ilaplace(H(s) * F2(s))
ezplot(t,g(t));
axis([0,5,-1,1.5]);
grid on;
figure(3);%激励 f (t) = cos(20t)e (t)产生的零状态响应
subplot(2,1,1);
fprintf('激励 f(t) = cos(20t)e(t)产生的零状态响应');
F3(s) = laplace(cos(20*t)*heaviside(t));
y(t) = ilaplace(H(s) * F3(s));
ezplot(t,y(t));
axis([0,6,-0.5,0.5]);
grid on;
subplot(2,1,2);
fprintf(' f(t) = cos(20t)');
F4(s) = cos(20*t);
ezplot(t,F4(t));
grid on;