//编写程序XMLtoTXT自动将XML文件email.xml转换为文本文件email.txt。命令行格式：XMLtoTXT email.xml email.txt。
#include<stdlib.h>
#include <stdio.h>
#include <string.h>
#define MAXSIZE 1024
void xml2txt(char filename1[], char filename2[]){
    FILE *fp1, *fp2;
    char buf[MAXSIZE];
    char temp[MAXSIZE];
    char *p, *q;
    if((fp1 = fopen(filename1, "r"))==NULL){
        fprintf(stderr, "%s", "can't open this file!\n");
        return ;
    }
    if((fp2 = fopen(filename2, "w")) == NULL){
        fprintf(stderr, "%s", "can't open this file!\n");
        return ;
    }
    while(fgets(buf, MAXSIZE, fp1)){
        if ((p = strstr(buf, "<from>")) != NULL){
            fgets(buf, MAXSIZE, fp1);
            if ((p = strstr(buf, "<address>")) != NULL){
                if ((q = strstr(buf, "</address>")) != NULL){
                    p = p + strlen("<address>");
                    memset(temp, 0, MAXSIZE);
                    strncpy(temp, p, q-p);
                    fprintf(fp2, "from : %s\n", temp);
                }
            }
        }
        if ((p = strstr(buf, "<to>")) != NULL){
            fgets(buf, MAXSIZE, fp1);
            if ((p = strstr(buf, "<address>")) != NULL){
                if ((q = strstr(buf, "</address>")) != NULL){
                    p = p + strlen("<address>");
                    memset(temp, 0, MAXSIZE);
                    strncpy(temp, p, q-p);
                    fprintf(fp2, "to : %s\n", temp);
                }
            }
        }
        if ((p = strstr(buf, "<subject>")) != NULL){
            if ((q = strstr(buf, "</subject>")) != NULL){
                p = p + strlen("<subject>");
                memset(temp, 0, MAXSIZE);
                strncpy(temp, p, q-p);
                fprintf(fp2, "subject : %s\n", temp);
            }
        }
        if ((p = strstr(buf, "<body>")) != NULL){
            if ((q = strstr(buf, "</body>")) != NULL){
                p = p + strlen("<body>");
                memset(temp, 0, MAXSIZE);
                strncpy(temp, p, q-p);
                fprintf(fp2, "body : %s\n", temp);
            }
        }
    }
    
    fclose(fp1);
    fclose(fp2);
}

int main(int argc, char *argv[]){
    if(argc != 3){
        fprintf(stderr, "%s", "Usage ./XML2TXT data/email.xml data/email.txt\n");
        return -1;
    }
    xml2txt(argv[1], argv[2]);
    return 0;
}