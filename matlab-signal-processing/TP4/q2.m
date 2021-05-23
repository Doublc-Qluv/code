clear all;
%laplace变换
syms t s
f = t + 2;
F = laplace(f,t,s)
figure(1);%画出H1(s)的零极点图
num = [0 0 1 2];
den  = [1 1 2 6];
Hs = tf (num,den);
zplane(num,den);
title('H_1(s)的零极点分布');
figure(2);%画出H2(s)的零极点图
num = [0 1 0 1];
den  = [3 5 4 6];
Hs = tf (num,den);
zplane(num,den);
title('H_2(s)的零极点分布');
