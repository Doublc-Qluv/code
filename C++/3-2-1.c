/*1*/#include <stdio.h>
/*2*/#include <stdlib.h>
/*3*/#include<string.h>
/*4*/int main()
/*5*/{
/*6*/    FILE *fp;
/*7*/    char str1[20],str2[20],str[20];
/*8*/    if((fp=fopen("A.dat","r"))==NULL){
/*9*/        printf("无法打开A文件！");
/*10*/        exit(0);
/*11*/    }
/*12*/    fgets(str1,10,fp);
/*13*/    if((fp=fopen("B.dat","r"))==NULL){
/*14*/        printf("无法打开B文件！");
/*15*/        exit(0);
/*16*/    }
/*17*/    int i,j,n;
/*18*/    char t;
/*19*/    
/*20*/    fgets(str2,20,fp);
/*21*/    strcat(str1,str2);
/*22*/    strcpy(str,str1);
/*23*/    n=strlen(str);
/*24*/    for(j=0;j<n-1;j++)
/*25*/        for(i=0;i<n-1-j;i++)
/*26*/        if(str[i]>str[i+1]){
/*27*/            t=str[i];
/*28*/            str[i]=str[i+1];
/*29*/            str[i+1]=t;
/*30*/        }
/*31*/    if((fp=fopen("C.dat","w"))==NULL){
/*32*/        printf("无法打开C文件！");
/*33*/        exit(0);
/*34*/    }
/*35*/    fputs(str,fp);
/*36*/    fputs("\n",fp);
/*37*/    printf("%s\n",str);
/*38*/    return 0;
