function [wave] = square_wave(n)
t = 0:4*pi/1000:4*pi;
wave = zeros(size(t));
for k = 1:n
    wave = wave+sin((2*k-1).*t)/(2*k-1);
end
end
