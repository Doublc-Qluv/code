#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
void MySort(int num[],int len)
{
    int i,j,temp;
    for(i=0;i<len;i++)
    {
        for (j=0;j<len-i;j++)
        {
            if (num[j]>num[j+1])
            {
                temp=num[j+1];
                num[j+1]=num[j];
                num[j]=temp;
            }
        }
    }
}
 
int main(void)
{
    FILE * fp1 = NULL;
    FILE * fp2 = NULL;
    FILE * fp3 = NULL;
 
    int num[200];
    int temp=0,index=0;
 
    fp1 = fopen("num1.txt","r");
    fp2 = fopen("num2.txt","r");
    fp3 = fopen("num3.txt","w");
 
    while(!feof(fp1))
    {
        fread(&temp,sizeof(int),1,fp1);
        num[index++]=temp;
    }
    fclose(fp1);
    while(!feof(fp2))
    {
        fread(&temp,sizeof(int),1,fp2);
        num[index++]=temp;
    }
    fclose(fp2);
 
    MySort(num,index);
    fwrite(num,sizeof(int),index,fp3);
    fclose(fp3);
 
    return 0;
}