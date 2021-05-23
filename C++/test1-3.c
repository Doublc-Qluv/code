#include <stdio.h>
#include <string.h>

int main(){
    char str[100];
    int  num[100];
    int res[2000];
    printf("input your decimal number and you can get the binary number: \n");
    while(scanf("\n%s",str)!=EOF){  //字符串转数字
        for(int i=0;i<strlen(str);i++)
            num[i]=str[i]-'0';
        int size=strlen(str);
        int index=0;//结果数组游标
        for(int i=0;i<size;){ //控制被除数开始位置
            int temp=0,remain=0;//余数
            for(int j=i;j<size;j++){ //控制除法运算，竖式除法，从头往后每一位依次作除法
                temp=(10*remain+num[j])%2;
                num[j]=(10*remain+num[j])/2;
                remain=temp;
            }
            res[index]=remain;
            index++;
            while(num[i]==0) //从第一个非0开始
                i++;
        }
        for(int i=index-1;i>=0;i--) //逆序输出

                printf("%d",res[i]);
            }
    printf("\n");
    return 0;
}