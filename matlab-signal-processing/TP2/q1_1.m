t=-2*pi:0.01:2*pi;
y1=sawtooth(0.5*t,1);%��Ŀԭʼ��������
y2=((t+2*pi).*stepfun(t,-2*pi)-(t-2*pi).*stepfun(t,2*pi))/(2*pi)-2*stepfun(t,0);%����ģ�����
% subplot(1,2,0);
% plot(t,y1,'blue');
% axis([-10,10,-1.5,1.5]);
% xlabel('t');
% ylabel(' ');
% title('ԭʼ�ź�һ�����ڲ���');
% grid on;

subplot(1,2,1);
plot(t,y2,'blue'); 
axis([-10,10,-1.5,1.5]);
xlabel('t');
ylabel(' ');
title('ԭʼ�ź�һ�����ڲ���(�Ѿ��ı����뷽ʽ)');
grid on;

sum=zeros(size(t));
for k=-10:10
       sum=sum+pro1_fun(k).*exp(0.5i*k.*t);%��г�������Ӵ���
end
subplot(1,2,2);
plot(t,sum,'r');
axis([-10,10,-1.5,1.5]);
xlabel('t');
ylabel(' ');
title('ǰ11��г�����ӳ���һ�����ڲ���');
grid on;