close all;clear all;
%����fliter���ַ��̣���ϵͳ��un����Ӧ�ж��ȶ�??

%����1??����filter���ַ��̣�  ��ϵͳ��u(n)����Ӧ�ж��ȶ�??
A=[1,-0.9];B=[0.05,0.05];
x1n=[1 1 1 1 1 1 1 1 zeros(1,50)];
x2n=ones(1,128);
y1n=filter(B,A,x1n);
subplot(1,3,1);y='y1(n)';tstem(y1n,y);
ylabel('y_1(n)','Interpreter','tex');
title({'(a) ϵͳ��R_8(n)����Ӧy_1(n)'},'Interpreter','tex');
y2n=filter(B,A,x2n);
subplot(1,3,2);y='y2(n)';tstem(y2n, y);
ylabel('y_2(n)','Interpreter','tex');
title('(b) ϵͳ��u(n)����Ӧy_2(n)','Interpreter','tex');
hn=impz(B,A,58);
subplot(1,3,3);y='h(n)';tstem(hn,y);
ylabel('h(n)','Interpreter','tex');
title('(c) ϵͳ��λ������Ӧh(n)','Interpreter','tex');

%����2??����conv����������
x1n=[1 1 1 1 1 1 1 1]; %�����ź�x1n=R8n
h1n=[ones(1,10) zeros(1,10)];
h2n=[1 2.5 2.5 1 zeros(1,10)];
y21n=conv(h1n,x1n);
y22n=conv(h2n,x1n);
figure(2)
subplot(2,2,1);y='h1(n)';tstem(h1n,y);
ylabel('h_1(n)','Interpreter','tex');    
title('(d) ϵͳ��λ������Ӧh_1(n)','Interpreter','tex');

subplot(2,2,2);y='y21(n)';tstem(y21n,y);
ylabel('y_2_1(n)','Interpreter','tex');
title('(e) h_1(n)��R_8(n)�ľ��y_2_1(n)','Interpreter','tex');
subplot(2, 2,3); y='h2(n)';tstem(h2n,y);     %���ú���tstem��ͼ
ylabel('h_2(n)','Interpreter','tex');
title('(f) ϵͳ��λ������Ӧh_2(n)','Interpreter','tex');
subplot(2, 2, 4); y='y22(n)';tstem(y22n, y);
ylabel('y_2_2(n)','Interpreter','tex');
title('(g) h2(n)��R8(n)�ľ��y_2_2(n)','Interpreter','tex');
%=====================================

%����3??г������??
un=ones(1, 256);    %�����ź�un
n=0:255;
xsin=sin(0.014*n)+sin(0.4*n);  %���������ź�
A=[1,-1.8237,0.9801];
B=[1/100.49,0,-1/100.49]; 
%ϵͳ��ַ���ϵ������B��A
y31n=filter(B,A,un);   %г������un����Ӧy31n
y32n=filter(B,A,xsin);
%г�����������źŵ���Ӧy32n
figure(3)
subplot(2,1,1);y='y31(n)';tstem(y31n,y);
ylabel('y_3_1(n)','Interpreter','tex');
title('(h) г������u(n)����Ӧy_3_1(n)','Interpreter','tex');
subplot(2,1,2);y='y32(n)';tstem(y32n,y);
ylabel('y_3_2(n)','Interpreter','tex');
title('(i) г�����������źŵ���Ӧy_3_2(n)','Interpreter','tex');


function tstem(xn,yn)
n = 0:length(xn)-1;
stem(n,xn,'.');
xlabel('n','Interpreter','tex');
axis([0,n(end),min(xn),1.2*max(xn)]);
end