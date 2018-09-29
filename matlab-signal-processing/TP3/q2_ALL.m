syms t w;
f1 = 0.5*exp(-2*t).*heaviside(t);
f2 = 0.5*exp(-2*(t-1)).*heaviside(t-1);
f1_FT = fourier(f1,t,w);%f1傅里叶变换
f2_FT = fourier(f2,t,w);%f2傅里叶变换

%原始图像
figure(1);
t = -5:0.01:5;
plot(t,subs(f1,t));%f1图形
hold on;
xlabel({'$t:s$'},'Interpreter','latex');
ylabel({'$f_n$'},'Interpreter','latex');
plot(t,subs(f2,t));%f2图形
grid on;%图例后加

%画出两个幅度图
figure(2);
t = -5:0.01:5;
w = -20:0.01:20;
subplot(2,1,1);
plot(w,subs(abs(f1_FT),w));%f1_FT的幅度图
xlabel({'$\omega:rad/s$'},'Interpreter','latex');
ylabel({'$|F_1(j\omega)|$'},'Interpreter','latex');
grid on;
%title({'$abs{F_2(j\omega)}$'},'Interpreter','latex');
subplot(2,1,2);
plot(w,subs(abs(f2_FT),w),'r');%f2_FT的幅度图
xlabel({'$\omega:rad/s$'},'Interpreter','latex');
ylabel({'$|F_2(j\omega)|$'},'Interpreter','latex');
grid on;

figure(3);
%画出两个相位图
w = -20:0.01:20;
plot(w,subs(angle(f1_FT),w));%f1_FT的相位图
hold on;
xlabel({'$\omega:rad/s$'},'Interpreter','latex');
ylabel({'$\phi_n(\omega)$'},'Interpreter','latex');
plot(w,subs(angle(f2_FT),w));%f2_FT的相位图
grid on;%图例后加