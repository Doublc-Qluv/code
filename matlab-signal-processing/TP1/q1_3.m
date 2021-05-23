k=-5:0.01:15;
y=heaviside(k+2)-heaviside(k-5);
stem(k,y,'LineStyle','none','MarkerSize',2.5);
set(gca,'xtick',[-5:1:10]);
set(gca,'ytick',[0:0.5:1.2]);
axis([-5,10,0,1.2]);
xlabel('k');
ylabel('f(k)');
title('f(k)=\epsilon(k+2)-\epsilon(k-5)');