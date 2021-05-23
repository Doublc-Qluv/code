syms t w;
f = exp(-2*abs(t));
f_FT = fourier(f,t,w);%����Ҷ�仯
t = -10:0.01:10;
subplot(2,1,1);
plot(t,subs(f,t));%����f(t)
xlabel({'$t:s$'},'Interpreter','latex');
ylabel({'$f(t)$'},'Interpreter','latex');
title({'$f(t)=e^{-2|t|}$'},'Interpreter','latex');
grid on;

w = -10:0.01:10;
subplot(2,1,2);
plot(w,subs(f_FT,w),'r');%����F(t)
xlabel({'$\omega:rad/s$'},'Interpreter','latex');
ylabel({'$F(j\omega)$'},'Interpreter','latex');
title({'$F(j \omega )$'},'Interpreter','latex');
grid on;