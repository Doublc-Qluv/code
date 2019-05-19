#include <stdio.h> /*1. 将合法 C 源程序每行前加上行号并删除其所有注释。*/
#include <string.h> 
int main(){
    printf("将c源程序每行加行号且删除其所有注释\n");   
    int i=0,j,k;   
    char duqu[100][1000],ch;//用这个来储存c程序，这个程序 不大于100行，且每行不大于1000个字符   
    FILE *fp=fopen("3-2-1.c","r+");  
    if(fp==NULL){   
        printf("打开文件失败\n");   
        return 0;
    }   
    while(!feof(fp)){
        fgets(duqu[i],1000,fp);
        i++; //读取的行数   
    }   
    for(k=i-1;k>=0;k--){ //把注释消掉   {   
        for(j=0;j<1000;j++){    
            if(duqu[k][j]=='/' && duqu[k][j-1]!='*' && (duqu[k][j+1]=='/' || duqu[k][j+1]=='*' ) ){ //这是/*情况和 // 情况     {
                if(k!=0 && j!=0) 
                    duqu[k][j]='\n';//防止下面的第一行是注释，消除完后，第一行变空      
                else 
                    duqu[k][j]='\0';     
                    duqu[k][j+1]='\0';     
            }     
            else if(duqu[k][j]=='/' && duqu[k][j-1]=='*') 
                duqu[k][0]='\0'; //*/的这种情况    
        }  
    }   
    fclose(fp);//把原来的c内容删掉   
    fp=fopen("3-2-1.c","wb+"); //同上   
    if(fp==NULL){   
        printf("打开文件失败\n");   
        return 0;  
    }   
    for(j=0,k=1;j<i-1;j++,k++){
        if(strlen(duqu[j])==0){
            k--;
            continue;
        }
        fputs("/*",fp);
        fprintf(fp,"%d",k);
        fputs("*/",fp);
        fputs(duqu[j],fp);
    }
    fclose(fp);
    return 0;
}