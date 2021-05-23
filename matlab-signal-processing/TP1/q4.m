y=2*wgn(1,500,0);%产生均值为0方差为2功率0dbw的高斯白噪声
subplot(3,1,1);
plot(y);%画图
title('高斯白噪声');
ylabel('wgn生成');
n=length(y);
[ACF,lags,bounds] = autocorr(y,n-1) ;
subplot(3,1,2) ;
plot(lags,ACF) ;
title('autocorr求自相关函数');

x=1+2*randn(1,500);%产生均值为1，方差为4的高斯白噪声
%subplot(2,1,1);
%plot(y);%画图
%title('高斯白噪声');
%ylabel('wgn生成');
[r1,lags]=xcorr(x);%自相关函数的估计
subplot(3,1,3) ;
plot(lags,r1);
title('xcorr求自相关函数');