#include <stdio.h>

struct complex{
	float a,b;
};
struct complex d,e;

int main()
{
	printf("a:");
	scanf("%f %f",&d.a,&d.b);
	printf("a=%f+%fi\n",d.a,d.b);
	printf("b:");
	scanf("%f %f",&e.a,&e.b);
	printf("b=%f+%fi\n",e.a,e.b);
	printf("a+b=%f+%fi\n",d.a+e.a,d.b+e.b);
	if((d.a<e.a)&&(d.b<e.b)){
		printf("a-b=%f%fi\n",d.a-e.a,d.b-e.b);
	}
	else{
		printf("a-b=%f+%fi\n",d.a-e.a,d.b-e.b);}
	printf("a*b=%f+%fi\n",d.a*e.a-d.b*e.b,d.a*e.b+d.b*e.a);
}