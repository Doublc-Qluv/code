k=-5:0.05:15;
y=7*(0.6).^(k).*cos(0.9*pi*k);
stem(k,y,'LineStyle','none','MarkerSize',2.5);
xlabel('k');
ylabel('f(k)');
title('f(t)=7(0.5)^{k}cos(0.9\pik)');