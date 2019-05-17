//统计一个英文文本文件中26个英文字母出现次数并按英文字母序输出统计结果，查找并替换此英文文本文件中某字符串。
#include<stdio.h>
#include<stdlib.h>
void fun(char one, FILE*fp ){
    char letter;
    int num=0;
    while(!feof(fp)){
        if(letter==one)num++;
        fscanf(fp, "%c", &letter); 
    }
    printf("%c:%d  ", one, num);

    return ; 
}

int main(){
    FILE *fp;	
    if((fp=fopen("english.txt", "r"))==NULL){
        printf("Cannot open the file!\n");
        exit(0);
    }

    char str[26];
    int i=0;
    str[0]='a';

    for (i=0; i<26; i++){
        str[i+1]=str[i]+1;
        //	printf("str[%d]=%c ", i, str[i]);
        fun(str[i], fp);
        rewind(fp);
    }
    fclose(fp);
    printf("\n");
    return 0;
}