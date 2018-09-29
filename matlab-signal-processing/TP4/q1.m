clear all;
Wc = 500;%½ØÖ¹ÆµÂÊ(cut-off frequency)
N = 2:1:5;
color = ['r','b','g','k'];
f = @(W,n) ( 1 ./ (1 + (W ./ Wc).^(2 * n)));
w = -1000:0.01:1000;
for i=1:length(N)
   plot(w / Wc, sqrt(f(w , N(i))),color(i));
   hold on;
end
grid on;
title('|F(j\omega)|');
ylabel('A');
xlabel({'$f/Hz$'},'Interpreter','latex');
legend('N=2','N=3','N=4','N=5');
