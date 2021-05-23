t=-2*pi:0.01:2*pi;
y1=sawtooth(0.5*t,1);%题目原始函数代码
y2=((t+2*pi).*stepfun(t,-2*pi)-(t-2*pi).*stepfun(t,2*pi))/(2*pi)-2*stepfun(t,0);%函数模拟代码
% subplot(1,2,0);
% plot(t,y1,'blue');
% axis([-10,10,-1.5,1.5]);
% xlabel('t');
% ylabel(' ');
% title('原始信号一个周期波形');
% grid on;

subplot(1,2,1);
plot(t,y2,'blue'); 
axis([-10,10,-1.5,1.5]);
xlabel('t');
ylabel(' ');
title('原始信号一个周期波形(已经改变输入方式)');
grid on;

sum=zeros(size(t));
for k=-10:10
       sum=sum+pro1_fun(k).*exp(0.5i*k.*t);%对谐波做叠加处理
end
subplot(1,2,2);
plot(t,sum,'r');
axis([-10,10,-1.5,1.5]);
xlabel('t');
ylabel(' ');
title('前11次谐波叠加出的一个周期波形');
grid on;