def hanoi(n, x, y, z):
    if n == 1:
	    print(x,'-->',z)
    else:
	    hanoi(n-1,x,z,y)
	    # S(n-1):x-->y
	    print(x,'-->',z) 
	    hanoi(n-1,y,x,z)
n = int(input('input the layer:'))
hanoi(n,'X','Y','Z')
