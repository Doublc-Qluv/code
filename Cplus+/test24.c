#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
int main(void)
{
    char* str;
    int len=0,start=0;
    scanf("%s",str);
    len = strlen(str);
    if(len % 2 != 0)
    {
        printf("error !");
        return 0;
    }
    len--;
    while(len - start != -1)
    {
        if(str[start] == '{' && str[len] == '}')
        {
            start++;
            len--;
        }
        else
        {
            if(str[start] == '(' && str[len] == ')')
            {
                start++;
                len--;
            }
            else
            {
                printf("error !\n");
                return 0;
            }
        }
    }
    printf("Ok !\n");
    return 0;

