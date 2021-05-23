#include<stdio.h>
#include<string.h>
typedef struct{
    char name[30];
    int score;
}cre;

cre math[100];
cre english[100]; 
int n1,n2;
char s[30],x;
int main() {
   freopen("db1.txt","r",stdin);
    while(scanf("%s %s",s,&x)!=EOF){
        int nn = strlen(s);
        n1++;
        for(int i=0;i<=nn;i++) math[n1].name[i]=s[i];
        math[n1].score = x;
    }
    freopen("db2.txt","r",stdin);
    freopen("db3.txt","w",stdout);
    while(scanf("%s%s",s,&x)!=EOF){
        int nn = strlen(s);
        n2++;
        for(int i=0;i<=nn;i++) english[n2].name[i]=s[i];
        english[n2].score = x;
    }
    for(int i=1;i<=n1;i++){
        for(int j=1;j<=n2;j++){
            if(strcmp(math[i].name,english[j].name)==0) {
                printf("%s %d %d\n",math[i].name,math[i].score,english[j].score);
                break;
            }
        }
    }
    return 0;
}