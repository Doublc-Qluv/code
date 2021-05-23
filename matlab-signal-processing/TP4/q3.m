clear all;
syms s t
%����ϵͳ����
H(s)= s / (s^2 + 3*s + 2);
figure(1);%ϵͳ�ĳ弤��Ӧ
fprintf('ϵͳ�ĳ弤��Ӧ');
F1(s) = laplace(dirac(t));
h(t) = ilaplace(H(s) * F1(s))
ezplot(t,h(t));
axis([0,5,-1,1.5]);
grid on;
figure(2);%ϵͳ�Ľ�Ծ��Ӧ
fprintf('ϵͳ�Ľ�Ծ��Ӧ');
F2(s) = laplace(heaviside(t));
g(t) = ilaplace(H(s) * F2(s))
ezplot(t,g(t));
axis([0,5,-1,1.5]);
grid on;
figure(3);%���� f (t) = cos(20t)e (t)��������״̬��Ӧ
subplot(2,1,1);
fprintf('���� f(t) = cos(20t)e(t)��������״̬��Ӧ');
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