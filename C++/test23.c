#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
struct StuGrade
{
    char* name;
    int score;
};
 
int main(void)
{
    FILE* fp1;
    FILE* fp2;
    FILE* fp3;
 
    struct StuGrade stu1[100];
    struct StuGrade stu2[100];
    int index1=0,index2=0;
    int i=0,j=0;
 
    fp1 = fopen("db1.txt","r");
    fp2 = fopen("db2.txt","r");
    fp3 = fopen("db3.txt","w");
 
    while(!feof(fp1))
    {
        fscanf(fp1,"%s %d\n", stu1[index1].name, stu1[index1].score);
        index1++;
    }
    fclose(fp1);
 
    while(!feof(fp2))
    {
        fscanf(fp2,"%s %d\n", stu2[index2].name, stu2[index2].score);
        index2++;
    }
    fclose(fp2);
 
    for(i=0;i<index1;i++)
    {
        for(j=0;j<index2;j++)
        {
            if(strcmp(stu1[i].name,stu2[j].name) == 0)
            {
                fprintf(fp3,"%s %d %d %f\n",
                        stu1[i].name,
                        stu1[i].score,
                        stu2[j].score,
                        (stu1[i].score+stu2[j].score)*0.5);
            }
        }
    }
    fclose(fp3);
    return 0;
}