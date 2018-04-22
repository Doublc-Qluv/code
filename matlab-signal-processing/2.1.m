t=0:0.01:4;
sys=tf([2,1],[1,4,3]);
h=impulse(sys,t);
s=step(sys,t);
subplot(211);plot(t,h),grid on;
xlabel('t'),ylabel('h(t)');
title('³å¼¤ÏìÓ¦')
subplot(212);plot(t,s),grid on;
xlabel('t'),ylabel('h(s)');
title('½×Ô¾ÏìÓ¦')