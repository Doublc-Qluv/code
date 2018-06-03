 f = @(n,t)(sin(n*t)./n);
 N = [5,10,20,100,200,500,1000];
 for i = 1:length(N)
     n = 1:N(i);
     x = -pi:0.01:pi;
     res = zeros(size(x));
     for k = 1:length(x)
          res(k)=sum(f(n,x(k)));
     end
     plot(x,res);hold on;
     grid on;
     title('f_N(t)');
     xlabel('t');
     ylabel('');
     pause(1);
     legend('n=5','n=10','n=20','n=100','n=200','n=500','n=1000')
 end