# include<stdio.h>
# include<string.h>
int main()
{
    char str[600];
    printf("your Binary number:");
    gets(str);
    int i, n = strlen(str), sum = 0;
    printf("the lenth of number: %d\n",n);
    for (i = 0; i < n-1; i++)
    {
        sum = (sum + (str[i]-'0'))*2;
        sum +=str[i]-'0';
    }
    printf("the output as Decimal number %d\n",sum);
    return 0;
}