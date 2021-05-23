#include<stdio.h>
#include<string.h>
char s[105];
char stack[105];
int top=0;
int main() {
    printf("请输入括号序列: ");
    scanf("%s",s);
    int n = strlen(s);
    for(int i=0;i<n;i++){
        if(s[i] == '('||s[i]=='{') stack[++top] = s[i];
        else{
            if(s[i]=='}'&&top>0&&stack[top]=='{') top--;
            else if(s[i]==')'&&top>0&&stack[top]=='(') top--;
            else {
                printf("error\n");
                return 0;
            }
        }
    }
    if(top!=0) {
       printf("error\n");
    }
    else{
        printf("correct\n");
    }

}