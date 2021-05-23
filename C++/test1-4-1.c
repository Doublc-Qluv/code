#include <stdio.h>
int main(){
    int data[1000];
    int N=0;
    printf("\t\tplease enter your N:"); 
    scanf("%d", &N);
    int index;
    int temp = 0;
    int counter = 0;
    printf("\t\tresult:");
    for (index = 0; index <= 10; index++) {//当两位数的个位大于 3 时会越来越大，故只进行十次
        if (index == 0) {
            data[index] = N;
    } else {
    //第一位 data[index]%10 //第二位(data[index]/10)%10
    int reminder = 0;//取余
    int integer = data[index - 1];//整除 int temp = 0;
    int t=1;
            temp = (data[index - 1] % 10) * (data[index - 1] % 10) +(data[index - 1] / 10)*(data[index - 1] / 10);
            data[index] = temp;
        }
    if (data[index] % 10 == 1) {//记录末尾为 1 的数 counter += 1;
    }
    if (data[index] / 10 == 0) {//只含个位则退出
            printf("%d", data[index]);
    break; }
        else {
            printf("%d->", data[index]);
        }
    }
    printf("\n\t\tend with 1:%d", counter); 
}