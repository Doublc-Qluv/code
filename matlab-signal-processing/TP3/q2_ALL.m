syms t w;
f1 = 0.5*exp(-2*t).*heaviside(t);
f2 = 0.5*exp(-2*(t-1)).*heaviside(t-1);
f1_FT = fourier(f1,t,w);%f1����Ҷ�任
f2_FT = fourier(f2,t,w);%f2����Ҷ�任

%ԭʼͼ��
figure(1);
t = -5:0.01:5;
plot(t,subs(f1,t));%f1ͼ��
hold on;
xlabel({'$t:s$'},'Interpreter','latex');
ylabel({'$f_n$'},'Interpreter','latex');
plot(t,subs(f2,t));%f2ͼ��
grid on;%ͼ�����

%������������ͼ
figure(2);
t = -5:0.01:5;
w = -20:0.01:20;
subplot(2,1,1);
plot(w,subs(abs(f1_FT),w));%f1_FT�ķ���ͼ
xlabel({'$\omega:rad/s$'},'Interpreter','latex');
ylabel({'$|F_1(j\omega)|$'},'Interpreter','latex');
grid on;
%title({'$abs{F_2(j\omega)}$'},'Interpreter','latex');
subplot(2,1,2);
plot(w,subs(abs(f2_FT),w),'r');%f2_FT�ķ���ͼ
xlabel({'$\omega:rad/s$'},'Interpreter','latex');
ylabel({'$|F_2(j\omega)|$'},'Interpreter','latex');
grid on;

figure(3);
%����������λͼ
w = -20:0.01:20;
plot(w,subs(angle(f1_FT),w));%f1_FT����λͼ
hold on;
xlabel({'$\omega:rad/s$'},'Interpreter','latex');
ylabel({'$\phi_n(\omega)$'},'Interpreter','latex');
plot(w,subs(angle(f2_FT),w));%f2_FT����λͼ
grid on;%ͼ�����