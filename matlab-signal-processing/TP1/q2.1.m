t=0:0.01:4;
sys=tf([2,1],[1,4,3]);
h=impulse(sys,t);
s=step(sys,t);
subplot(211);plot(t,h),grid on;
xlabel('t'),ylabel('h(t)');
title('�弤��Ӧ')
subplot(212);plot(t,s),grid on;
xlabel('t'),ylabel('h(s)');
title('��Ծ��Ӧ')

%��Ծ��������
%y=[1,4,3]
%x=[0,2,1]
%plot(x,y)