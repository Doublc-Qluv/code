wc = 100;

syms t w;
f1 = heaviside(t+2) - heaviside(t-2);
f2 = cos(wc*t);
f3 = f1*f2;
f1_FT = fourier(f1,t,w);
f2_FT = fourier(f2,t,w);
f3_FT = fourier(f3,t,w);

figure(1);
w = -10:0.03:10;
plot(w,subs(abs(f1_FT),w));%f1的幅度谱
axis([-10 10 -1 4.5]);
xlabel({'$\omega:rad/s$'},'Interpreter','latex');
ylabel({'$|f_1|$'},'Interpreter','latex');
title({'$|f_1|$'},'Interpreter','latex');
grid on;

figure(2);
w = -200:200;
plot(w,pi*sign(subs(f2_FT,w)));%f2的幅度谱
axis([-200 200 -1 4]);
xlabel({'$\omega:rad/s$'},'Interpreter','latex');
ylabel({'$|f_2|$'},'Interpreter','latex');
title({'$|f_2|$'},'Interpreter','latex');
grid on;

figure(3);
w = -200:0.07:200;
plot(w,subs(abs(f3_FT),w));%f3的幅度谱
xlabel({'$\omega:rad/s$'},'Interpreter','latex');
ylabel({'$|f_3|$'},'Interpreter','latex');
title({'$|f_3|$'},'Interpreter','latex');
grid on;
