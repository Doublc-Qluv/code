#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAXNAME 1000

int main()
{
    FILE *fp,*fp2;
    char fname1[MAXNAME],fname2[MAXNAME];
    int i = 1;
    
    printf("Please enter two need to compare file name:\n");
    scanf("%s %s",fname1,fname2);
        if((fp = fopen(fname1,"r")) == NULL || (fp2 = fopen(fname2,"r")) == NULL){
            printf("Error!\n");
            exit(1);
        }
    while(fgets(fname1,MAXNAME,fp) && fgets(fname2,MAXNAME,fp2))
        if(strcmp(fname1,fname2) == 0){
            i++;
            continue;
    }
        else{
            fputs(fname1,stdout);
            fputs(fname2,stdout);
            break;
        }
    printf("line: %d\n",i);
    if(ferror(fp) || ferror(fp2)){
        fprintf(stderr,"error writing stdout\n");
        exit(2);
    }
    exit(0);
}