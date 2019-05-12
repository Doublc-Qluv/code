#include <stdio.h>
#include <stdlib.h>
 
void ERROR(char b, int l, int *e)
{
	(*e)++;
	printf("without maching '%c' at line %d\n",b,l);
}
 
int main()
{
	FILE *fin;
	int tmp;
	int linenum[1000];
	char bracket_stack[500], bracket_w_stack[1000];
	int  iter_bstack = -1, iter_w_bstack = -1, error = 0, line = 1;
	fin = fopen("test24.c", "r");
	if (fin == NULL) exit(1);
	for (;;)
	{
		tmp = fgetc(fin);
		if (tmp == EOF) break;
		else if (tmp == '\n') line++;
		else if (tmp == '"')
		{
			for (;;)
			{
				tmp = fgetc(fin);
				if(tmp=='\\') tmp = fgetc(fin);
				else if (tmp == '"') break;
			}
		}
		else if (tmp == '\'')
		{
			for (;;)
			{
				tmp = fgetc(fin);
				if (tmp == '\\') tmp = fgetc(fin);
				else if (tmp == '\'') break;
			}
		}
		else if (tmp == '/')
		{
			tmp = fgetc(fin);
			if (tmp == '/') 
			{// single-line comment 
				while ((tmp = fgetc(fin)) != '\n'); 
				line++;
			} 
			else if (tmp == '*')
			{// multi-line comment
				int flag = 0;
				tmp = fgetc(fin);
				if (tmp == '\n') line++;
				for (;;)
				{
					if (flag) break;
					while (tmp != '*') 
					{ 
						tmp = fgetc(fin); 
						if (tmp == '\n') line++;
					}
					tmp = fgetc(fin);
					if (tmp == '\n') line++;
					if (tmp == '/') flag = 1;
				}
			}
			else if (tmp == '(')
			{
				bracket_stack[++iter_bstack] = tmp;
				bracket_w_stack[++iter_w_bstack] = tmp;
				linenum[iter_bstack] = line;
			}
		}
		else if (tmp == '(' || tmp == '{')
		{
			bracket_stack[++iter_bstack] = tmp;
			bracket_w_stack[++iter_w_bstack] = tmp;
			linenum[iter_bstack] = line;
		}
		else if (tmp == ')')
		{
			bracket_w_stack[++iter_w_bstack] = tmp;
			linenum[iter_bstack] = line;
			int leap = 0;
			while (leap <= iter_bstack && bracket_stack[iter_bstack - leap] != '(') leap++;
			if (iter_bstack<0 || leap) ERROR(tmp, line, &error);
			if (leap <= iter_bstack)
			{
				int i;
				for (i = iter_bstack - leap; i < iter_bstack; i++)
				{
					bracket_stack[i] = bracket_stack[i + 1];
					linenum[i] = linenum[i + 1];
				}
				iter_bstack--;
			}
		}
		else if (tmp == '}')
		{
			bracket_w_stack[++iter_w_bstack] = tmp;
			linenum[iter_bstack] = line;
			int leap = 0;
			while (leap <= iter_bstack && bracket_stack[iter_bstack - leap] != '{') leap++;
			if (iter_bstack<0 || leap) ERROR(tmp, line, &error);
			if (leap <= iter_bstack)
			{
				int i;
				for (i = iter_bstack - leap; i < iter_bstack; i++)
				{
					bracket_stack[i] = bracket_stack[i + 1];
					linenum[i] = linenum[i + 1];
				}
				iter_bstack--;
			}
		}
		else continue;
	}
	bracket_w_stack[++iter_w_bstack] = '\0';
	while (!error && iter_bstack >= 0)
	{
		ERROR(bracket_stack[iter_bstack], linenum[iter_bstack], &error);
		iter_bstack--;
	}
	if(!error) printf("%s", bracket_w_stack);
	fclose(fin);
	return 0;
}