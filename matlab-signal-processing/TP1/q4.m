y=2*wgn(1,500,0);%������ֵΪ0����Ϊ2����0dbw�ĸ�˹������
subplot(3,1,1);
plot(y);%��ͼ
title('��˹������');
ylabel('wgn����');
n=length(y);
[ACF,lags,bounds] = autocorr(y,n-1) ;
subplot(3,1,2) ;
plot(lags,ACF) ;
title('autocorr������غ���');

x=1+2*randn(1,500);%������ֵΪ1������Ϊ4�ĸ�˹������
%subplot(2,1,1);
%plot(y);%��ͼ
%title('��˹������');
%ylabel('wgn����');
[r1,lags]=xcorr(x);%����غ����Ĺ���
subplot(3,1,3) ;
plot(lags,r1);
title('xcorr������غ���');