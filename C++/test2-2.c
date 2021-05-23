#include<stdio.h>
int a[105],cnt=0;
int main() {
    freopen("num1.txt","r",stdin);
    int x;
    while(scanf("%d",&x)!=EOF) {
        a[++cnt] = x;
    }
    freopen("num2.txt","r",stdin);
    while(scanf("%d",&x)!=EOF) {
        a[++cnt] = x;
    }
    for(int i=1;i<cnt;i++){
        for(int j=i+1;j<=cnt;j++){
            if(a[i]>a[j]) {
                int t = a[i];
                a[i] = a[j];
                a[j] = t;
            }
        }
    }
    freopen("num3.txt","w",stdout);
    for(int i=1;i<=cnt;i++) {
        printf("%d ",a[i]);
    }
    printf("\n");
}