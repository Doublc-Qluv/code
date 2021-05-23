/*从键盘输入一个字符串，将其中的小写字母全部转换成大写字母，然后输出到一个磁盘文件test中保存。输入的字符串以"!"结束。*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(){
    FILE *fp;
    //char filename[20];//存储文件名
    char ch;//存储输入的字符
    int i;

    //printf("输入要保存的文件名:  ");
    //scanf("%s",filename);
    char filename[] = "test.dat";
    if((fp=fopen(filename,"w"))==NULL){
        printf("Can't open the file!\n");
        exit(0);
    }
    ch=getchar();//吃掉回车符

    printf("输入字符串,以\"!\"结束:\n");
    ch=getchar();//接收从键盘输入的第一个字符

    while(ch!='!'){//循环输入，碰到"!"就结束
        if(ch>='a' || ch<='z'){
            ch=toupper(ch);
            fputc(ch,fp);//把输入的字符写在文件里
            putchar(ch);//显示文件在屏幕上
            ch=getchar();//再接收从键盘输入的一个字符,否则死循环
        }
            
    }
    fclose(fp);
    return 0;

}