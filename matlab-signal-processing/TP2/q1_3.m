t=-2*pi:0.1:2*pi;
y=sawtooth(0.5*t,1);
plot(t,y,'blue');hold on;
sum=zeros(size(t));
for k=-5:5
       sum=sum+q1_1_function(k).*exp(0.5i*k.*t);%��г������6�ε��Ӵ���
end
plot(t,sum,'green');hold on;
sum=zeros(size(t));
for k=-10:10
       sum=sum+q1_1_function(k).*exp(0.5i*k.*t);%��г������11�ε��Ӵ���
end
plot(t,sum,'red');
sum=zeros(size(t));
for k=-20:20
       sum=sum+q1_1_function(k).*exp(0.5i*k.*t);%��г������21���Ӵ���
end
plot(t,sum,'c');
legend('ԭ�ź�һ������','г��6�ε���','г��11�ε���','г��21�ε���');
xlabel('t');
ylabel(' ');
title('����˹����');
grid on;