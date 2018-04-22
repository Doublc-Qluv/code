t=-5,0.01,10;
f1(t)=heaviside(t)-heaviside(t-1)
f2(t)=2*t*(heaviside(t)-heaviside(t-1)) 
conv(f1(t),f2(t))