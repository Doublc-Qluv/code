//统计一个英文文本文件中所有单词出现次数并按英文字母序输出统计结果，查找并替换此英文文本文件中某单词。
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#define FILENAME "english.txt"
struct WORD{
    char w[100];
    int n;
};
int main(void){
    int i,j,k,l;
    struct WORD w[1000];
    FILE *fp;
    if((fp=fopen(FILENAME,"r"))==NULL){
        printf("Open the file failure...\n");
        exit(0);
    }
    i=0;
    while(fscanf(fp,"%s",w[i].w),!feof(fp)){
        if(!isalpha(w[i].w[0]))
            strcpy(w[i].w,w[i].w+1);
        if(!isalpha(w[i].w[j=strlen(w[i].w)-1]))
            w[i].w[j]='\0';
        for(j=0;j<i;j++)
            if(strcmp(w[j].w,w[i].w)==0){
                w[j].n++;
                break;
            }
        if(j>=i)w[i++].n=1;
    }
    fclose(fp);
    for(k=0;k<i;k++){
        for(l=k,j=l+1;j<i;j++)
            if(strcmp(w[l].w,w[j].w)>0) l=j;
        if(l!=k){
            w[i]=w[l];
            w[l]=w[k];
            w[k]=w[i];
        }
        printf("%-20s%d\n",w[k].w,w[k].n);
    }
    return 0;
}
