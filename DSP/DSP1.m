close all;clear all;
%调用fliter解差分方程，由系统对un的响应判断稳定??

%内容1??调用filter解差分方程，  由系统对u(n)的响应判断稳定??
A=[1,-0.9];B=[0.05,0.05];
x1n=[1 1 1 1 1 1 1 1 zeros(1,50)];
x2n=ones(1,128);
y1n=filter(B,A,x1n);
subplot(1,3,1);y='y1(n)';tstem(y1n,y);
ylabel('y_1(n)','Interpreter','tex');
title({'(a) 系统对R_8(n)的响应y_1(n)'},'Interpreter','tex');
y2n=filter(B,A,x2n);
subplot(1,3,2);y='y2(n)';tstem(y2n, y);
ylabel('y_2(n)','Interpreter','tex');
title('(b) 系统对u(n)的响应y_2(n)','Interpreter','tex');
hn=impz(B,A,58);
subplot(1,3,3);y='h(n)';tstem(hn,y);
ylabel('h(n)','Interpreter','tex');
title('(c) 系统单位脉冲响应h(n)','Interpreter','tex');

%内容2??调用conv函数计算卷积
x1n=[1 1 1 1 1 1 1 1]; %产生信号x1n=R8n
h1n=[ones(1,10) zeros(1,10)];
h2n=[1 2.5 2.5 1 zeros(1,10)];
y21n=conv(h1n,x1n);
y22n=conv(h2n,x1n);
figure(2)
subplot(2,2,1);y='h1(n)';tstem(h1n,y);
ylabel('h_1(n)','Interpreter','tex');    
title('(d) 系统单位脉冲响应h_1(n)','Interpreter','tex');

subplot(2,2,2);y='y21(n)';tstem(y21n,y);
ylabel('y_2_1(n)','Interpreter','tex');
title('(e) h_1(n)与R_8(n)的卷积y_2_1(n)','Interpreter','tex');
subplot(2, 2,3); y='h2(n)';tstem(h2n,y);     %调用函数tstem绘图
ylabel('h_2(n)','Interpreter','tex');
title('(f) 系统单位脉冲响应h_2(n)','Interpreter','tex');
subplot(2, 2, 4); y='y22(n)';tstem(y22n, y);
ylabel('y_2_2(n)','Interpreter','tex');
title('(g) h2(n)与R8(n)的卷积y_2_2(n)','Interpreter','tex');
%=====================================

%内容3??谐振器分??
un=ones(1, 256);    %产生信号un
n=0:255;
xsin=sin(0.014*n)+sin(0.4*n);  %产生正弦信号
A=[1,-1.8237,0.9801];
B=[1/100.49,0,-1/100.49]; 
%系统差分方程系数向量B和A
y31n=filter(B,A,un);   %谐振器对un的响应y31n
y32n=filter(B,A,xsin);
%谐振器对正弦信号的响应y32n
figure(3)
subplot(2,1,1);y='y31(n)';tstem(y31n,y);
ylabel('y_3_1(n)','Interpreter','tex');
title('(h) 谐振器对u(n)的响应y_3_1(n)','Interpreter','tex');
subplot(2,1,2);y='y32(n)';tstem(y32n,y);
ylabel('y_3_2(n)','Interpreter','tex');
title('(i) 谐振器对正弦信号的响应y_3_2(n)','Interpreter','tex');


function tstem(xn,yn)
n = 0:length(xn)-1;
stem(n,xn,'.');
xlabel('n','Interpreter','tex');
axis([0,n(end),min(xn),1.2*max(xn)]);
end