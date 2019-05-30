CC=gcc
CFLAGS=-Wall -g -DDEBUG
LDFLAGS=
LIBS=  -lpthread 

objects = test.o ais4citycd.o

test: $(objects)
	$(CC) -m32 -O3 -o test $(objects) $(LIBS)
	
test.o: test.c
	$(CC) -m32 -O3 -c test.c 

ais4citycd.o:ais4citycd.c
	$(CC) -m32 -O3 -c ais4citycd.c 
	
clean:
	rm test $(objects)

