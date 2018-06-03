t=-2*pi:0.1:2*pi;
y=sawtooth(0.5*t,1);
plot(t,y,'blue');hold on;
sum=zeros(size(t));
for k=-5:5
       sum=sum+q1_1_function(k).*exp(0.5i*k.*t);%对谐波进行6次叠加处理
end
plot(t,sum,'green');hold on;
sum=zeros(size(t));
for k=-10:10
       sum=sum+q1_1_function(k).*exp(0.5i*k.*t);%对谐波进行11次叠加处理
end
plot(t,sum,'red');
sum=zeros(size(t));
for k=-20:20
       sum=sum+q1_1_function(k).*exp(0.5i*k.*t);%对谐波进行21叠加处理
end
plot(t,sum,'c');
legend('原信号一个周期','谐波6次叠加','谐波11次叠加','谐波21次叠加');
xlabel('t');
ylabel(' ');
title('吉布斯现象');
grid on;