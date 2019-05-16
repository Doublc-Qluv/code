/*有两个磁盘文件“A.dat”和“B.dat”，各存放一行字母，要求把这两个文件中的信息合并（按字母顺序排列），输出到一个新文件“C.dat”中。*/
#include <stdio.h>
#include <stdlib.h>
#include<string.h>
int main()
{
    FILE *fp;
    char str1[20],str2[20],str[20];
    if((fp=fopen("A.dat","r"))==NULL){
        printf("无法打开A文件！");
        exit(0);
    }
    fgets(str1,10,fp);
    if((fp=fopen("B.dat","r"))==NULL){
        printf("无法打开B文件！");
        exit(0);
    }
    int i,j,n;
    char t;
    
    fgets(str2,20,fp);
    strcat(str1,str2);
    strcpy(str,str1);
    n=strlen(str);
    for(j=0;j<n-1;j++)
        for(i=0;i<n-1-j;i++)
        if(str[i]>str[i+1]){
            t=str[i];
            str[i]=str[i+1];
            str[i+1]=t;
        }
    if((fp=fopen("C.dat","w"))==NULL){
        printf("无法打开C文件！");
        exit(0);
    }
    fputs(str,fp);
    fputs("\n",fp);
    printf("%s\n",str);
    return 0;
}