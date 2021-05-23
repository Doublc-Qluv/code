syms t w;
f_FT = 1/(1+w^2);
f = ifourier(f_FT,w,t);%傅里叶逆变化
w = -10:0.01:10;
subplot(2,1,1);
plot(w,subs(f_FT,w));%画出F(t)
xlabel({'$\omega:rad/s$'},'Interpreter','latex');
ylabel({'$F(j\omega)$'},'Interpreter','latex');
title({'$F(j \omega)=\frac{1}{1+ \omega^2}$'},'Interpreter','latex');
grid on;

t = -10:0.01:10;
subplot(2,1,2);
plot(t,subs(f,t),'r');%画出f(t)
xlabel({'$t:s$'},'Interpreter','latex');
ylabel({'$f(t)$'},'Interpreter','latex');
title({'$f(t)$'},'Interpreter','latex');
grid on;