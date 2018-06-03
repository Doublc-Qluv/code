f = @(n,t)(sin(n*t)./n);
N = [5,10,20,100,200,500,1000];
for i = 1:length(N)
    n = N(i);
    x = -pi:0.01:pi;
    res = zeros(size(x));
    for k = 1:length(x)
        for m = 1:n
            res(k) = res(k) + sum(f(1:m,x(k)));
        end
        res(k)=res(k)/n;
    end
    plot(x,res);hold on;
    grid on;
    title('F_N(t)');
    xlabel('t');
    ylabel(' ');
    pause(1);
    legend('n=5','n=10','n=20','n=100','n=200','n=500','n=1000');
end