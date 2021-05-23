//编写程序XMLtoTXT自动将XML文件email.xml转换为文本文件email.txt。命令行格式：XMLtoTXT email.xml email.txt。
#include <stdio.h>
#include <string.h>
int search(char *s1, char *s2){
	if(strstr(s1, s2) != NULL){
		return (int)(strstr(s1, s2) - s1)/sizeof(char);
		}else{
			return -1;
		}
}
int main(int argc, char *argv[]){
	int k1,k2;
	char ss[1000]="";
	char s1[100]="";
	char kk[1000]="";
	char hh[100]="";
	FILE *fp;
	fp = fopen(argv[1],"r");
	if(fp == NULL){
		printf("open file error\n");
	}
	while(!feof(fp)){
		fgets(s1,101,fp);
		strcat(ss,s1);
	}
	puts(ss);
	fclose(fp);
	fp =  fopen(argv[2],"wb+");
	if(fp == NULL){
		printf("open file error\n");
	}
	k1 = search(ss,"<from>");
	k2 = search(ss,"</from>");
	if(k1!= -1 && k2!= -1){
		strcpy(kk,ss);
		kk[k2-13] = '\0';
		strcpy(hh,&kk[k1+19]);
		puts(hh);
		fprintf(fp,"from: %s\r\n",hh);
	}
	k1 = search(ss,"<to>");
	k2 = search(ss,"</to>");
	if(k1!= -1 && k2!= -1){
		strcpy(kk,ss);
		kk[k2-13] = '\0';
		strcpy(hh,&kk[k1+17]);
		puts(hh);
		fprintf(fp,"to: %s\r\n",hh);
	}
	k1 = search(ss,"<subject>");
	k2 = search(ss,"</subject>");
	if(k1!= -1 && k2!= -1){
		strcpy(kk,ss);
		kk[k2] = '\0';
		strcpy(hh,&kk[k1+9]);
		puts(hh);
		fprintf(fp,"subject: %s\r\n",hh);
	}
	k1 = search(ss,"<body>");
	k2 = search(ss,"</body>");
	if(k1!= -1 && k2!= -1){
		strcpy(kk,ss);
		kk[k2] = '\0';
		strcpy(hh,&kk[k1+7]);
		puts(hh);
		fprintf(fp,"body: %s\r\n",hh);
	}
	return 0;
}