# include<stdio.h>
int solve(int n){
    while(n>=10){
        int nex = 0;
        while(n) {
            int tmp = n%10;
            nex+=tmp*tmp;
            n/=10;
        }
        n = nex;
    }
    if(n == 1) return 1;
    return 0;
}
int main(){
    printf("请输入n: ");
    int n;
    scanf("%d",&n);
    int cnt = 0;
    for(int i=1;i<=n;i++){
        cnt+=solve(i);
    }
    printf("1～%d共有%d条数据链末尾是1\n",n,cnt);   

}