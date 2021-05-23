#include <stdio.h>
#include <curses.h>
//#include <conio.h>
#include <stdlib.h>
#include <malloc/malloc.h>
//#include <malloc.h>
#include <string.h>
#define LEN sizeof(struct user) 

//函数声明 
int signin(); //注册
int login();// 登陆
int change();//修改用户密码
int read();//读取用户名密码

int Admi();//管理员界面
int VerificationIdentity();//管理员登陆

int InitMusic();//初始化歌曲信息
int Savemusic();//保存歌曲目录
 
int findsong();//按歌名查找
int findsinger();//按歌手查找
int output(char *p);//打印歌名对应的文件
int save();//将修改信息保存至文件中
 
int Add();//添加歌曲 
int Delete();//链表删除
int Modify();//修改歌曲信息

typedef struct music
{
	char song[20];
	char singer[20];
	struct music *next;
}linklist;
linklist *head,*p,*s;

struct user
{
  char id[20];
  char code[20];
  struct user *unext;
};
struct user *uhead;   



//链表删除
int  Delete(void)
{
	linklist *q,*p;
	char Dsong[20],song[25];
	int
	ch='y';
	while(tolower(ch)=='y')
	{
		printf("\n\n\t*请输入需要删除的歌曲（按回车键确认）：");
		gets(Dsong);
		p=head;
		q=NULL;
		while(p!=NULL)
		{
			if(strcmp(p->song,Dsong))
			{
				q=p;
				p=p->next;
			}
			else
			{
				printf("\n\n\t*您要删除的歌曲是：%s,该歌歌手为:%s\n",p->song,p->singer);
				printf("\n\t请您再次确认[y/Y]:");
				ch=getch();
				if(tolower(ch)=='y')
				{
					q->next=p->next;
					sprintf(song,"%s.txt",p->song);
					remove(song);
					break;
				}
			
			}
		}

		if(p==NULL)
		{
			printf("\n\n\t不存在您要删除的歌曲，请按任意键继续\n");
			getch;
		}
		printf("\n\n\t*是否继续删除下一首歌曲[y/Y],不删除按任意其他键...\n");
		ch=getch();
	}
	return 1;
} 
//添加歌曲 
int Add()
{
	linklist *p3,*p2;
	char ch1,ch2,song[50],str[1024];

	FILE *fp2;
	p2=head;
	while(p2->next!=NULL)
			p2=p2->next;

	ch1='y';
	while(tolower(ch1)=='y')
	{
		p3=(linklist*)malloc(sizeof(linklist));
		printf("\n\n\n\n\t\t**增加歌曲**");
		printf("\n\n\n\t新增歌曲请按如下格式输入：\n");
		printf("\n\t*输入新增歌曲名：");
		gets(p3->song);
		printf("\n\n\t*输入新增歌曲歌手名：");
		gets(p3->singer);
		printf("\n\n\t*请继续添加歌词");
		printf("\n\t");
		gets(str);
		p3->next=NULL;
		
		ch1='0';
		printf("\n\n\t请确认上述输入[y/Y],否则按其他任意键继续:");
		ch2=getch();
		printf("\n%c\n",ch2); 
		if(tolower(ch2)=='y')
		{
			p2->next=p3; 
			p2=p3;
			printf("www\n");
			
			sprintf(song,"%s.txt",p3->song);                    //将新添加歌曲歌词写入文件中 
	   	 	if ((fp2=fopen(song,"w"))==NULL)
	 			
					printf("can not open file\n");
			else
			{
				fputs(str,fp2);
			}
			p3=NULL;
			fclose(fp2);
			printf("\n\n\t歌曲添加成功！");
		}
		else
		{
			printf("\n\n\t未能添加歌曲！！按任意键继续");
			getch();
				
		}
		printf("\n\n\t是否增加下一首歌，如果增加，键入[y/Y]，否则按任意键返回");
		ch1=getch();
	
	}
	p2=NULL;
	return 1;
	
}

//保存歌曲目录 
int Savemusic()
{
	
	FILE *fp;
	struct music *p;
	p=head;
	if((fp=fopen("music.txt","w"))==NULL)
	{
		printf("\n保存文件不正常，请核对文件名！\n");
		fclose(fp);
		return 1;
	}
	else
	{
		rewind(fp);
		while (p!=NULL)
		{
				fprintf(fp,"%s\t%s\n",p->song,p->singer);
			p=p->next;
		}
		fclose(fp);
		return 1;
	}
	
}


//修改歌曲信息
int Modify()
{
	linklist *q,*p2,*p3;
	char Msong[20];
	char ch,str[1024],s[20];
	FILE *fp1,*fp2;
	char song[25],song1[25],song2[25];
	do
	{
		printf("\n\n\t*请输入需要修改的歌曲（按回车键确认）：");
		gets(Msong);
		p=head;
		q=NULL;
		while(p!=NULL)
		{
			if(strcmp(p->song,Msong))
				p=p->next;
			else
			 break;
		}
		
	
				printf("\n\n\t*您要修改的歌曲是：%s,该歌歌手为 %s\n",p->song,p->singer);
				printf("\n\t*请输入需要修改的信息名称:");
				printf("\n\t1.歌曲名  2.歌手名  3.歌词\n");
				printf("\n\t请选择[1/2/3]:");
				ch=getch();
				switch(ch)
				{
					case'1':printf("\n\t\n*输入新修改歌曲名：");
							gets(p->song);
							sprintf(song1,"%s.txt",Msong); 
							sprintf(song2,"%s.txt",p->song); 
							rename(song1,song2);
							break;
					case'2':printf("\n\t*输入新修改歌曲歌手名：");
							gets(p->singer);
							break;
					case'3':printf("\n\t*请重新添加歌词\n");
							gets(str);
							sprintf(song,"%s.txt",p->song);                    //将新添加歌曲歌词写入文件中 
	   	 					if ((fp2=fopen(song,"w"))==NULL)
	 						{
								printf("can not open file%s\n",s);
								break;
							}
							else
							{
					
							fputs(str,fp2);
							fclose(fp2);
							break;
							}
							
					default:printf("\n\t\n输入错误，请重新输入:\n");
							break;
				}
			
		if(p==NULL)
		{
			printf("\n\n\t不存在您要修改的歌曲，请按任意键继续\n");
			getch;
		}
		printf("\n\n\t*是否继续修改下一首歌曲[y/Y],不修改按任意其他键...\n");
		ch=getch();
	} while(tolower(ch)=='y');
	return 1;
} 

//管理员界面 
int Admi()
{

			char chp;
			int legalUser;
			printf("\n\n\n* * * * * * * * * * * * * * * 管理员登录成功！！* * * * * * * * * * * * * * * *\n");
			printf("\n\n\t*1.添加歌曲\n");
			printf("\n\n\n\t*2.删除歌曲\n");
			printf("\n\n\n\t*3.修改歌曲\n");
			printf("\n\n\n\t*0.退出登录\n");
			
			printf("\n\n\t请选择[1/2/3/4/0]:");
			chp=getche();
			switch(chp)
			{
				case '1':
				 	Add();
					Savemusic();
					Admi();
					break;                                                                                 
				
				case'2':
				Delete();
				Savemusic();
				Admi();
					break;
					
				case'3':
				Modify();
				Savemusic();
				Admi();
					break;
				case'0':legalUser=0;
					break;
				default:printf("选择错误！\n");
					legalUser=1;
					Admi();
					break;
			}
			return legalUser;
		}




//管理员登陆
int VerificationIdentity()
{
	char userID[20],password[20];    //存放由键盘输入的用户名和口令 
	char superUID[20],passWD[20];    //存放文件中读取的用户名和口令 
	int i,legalUser;
	char ch;
	FILE *fp;
	legalUser=0;
	fp=fopen("superUser.txt","r");
	if(fp==NULL)
	{
		printf("\n\t权限文件不存在！按任意键继续..\n");
		getch();
	}
	else
	{
		do
		{
			ch='0';
			printf("\n\n\t\t\t   *管理员登陆*    \t\t\n");
			printf("\n\t*请输入用户名(<15个字符):");
			gets(userID);
			
			printf("\n\t*请输入密码(<15个数字,字母或符号):");
			gets(password);
			
			rewind(fp);
			while(!feof(fp))
			{
				fscanf(fp,"%s\t%s",superUID,passWD);
				if((strcmp(userID,superUID)==0)&&(strcmp(password,passWD)==0))
				{
					legalUser=1;
					break;
				}
				else
				{
				legalUser=0;
				printf("\n\n\t密码错误，是否需要重新输入用户名和密码？(y/n)");
				ch=getch();
				}
			}
		}
		while((ch=='y')||(ch=='Y'));
	}
	fclose(fp);
	return legalUser;
}













//初始化歌曲信息
int InitMusic()
{
	FILE *fp;
	struct music *p1,*p2;
	fp=fopen("music.txt","r");
	if(fp==NULL)
	{
		printf("未能初始化\n");
		fclose(fp);
		return 0;
	}
	else
	{
		p1=(struct music *)malloc(sizeof(linklist));
		head=p1;
	
		while(!feof(fp))
		{
			fscanf(fp,"%s\t%s\n",p1->song,p1->singer);
			p2=p1;
			p1=(struct music*)malloc(sizeof(linklist));
			p2->next=p1;
			
		}
		p2->next=NULL;
		p2=NULL;
		p1=NULL;
		p1=head;
		
		
		fclose(fp);
		return 1;
	}
	
} 

//用户登录函数 
int user()
    {
      int userflag=1; 
      char ch,ch1;
      while(userflag)
     {
        printf("\n\t ----------------------欢迎进入用户界面----------------------\n");
        printf("\t|                        1.注册                              |\n");
        printf("\t|                        2.登录                              |\n");
        printf("\t|                        0.退出                              |\n");
        printf("\t ------------------------------------------------------------\n");
        printf("\t*请输入您的选择(0/1/2):");
        ch=getche();
        getch();
        switch (ch)
       {
          case'1' : userflag=signin();//调用注册模块,注册成功返回2 
          break;
          case'2' : userflag=login();//调用登录模块，登录成功返回1 
          break;
          case'0' : userflag=0;
          break;
          default : printf("\n\t*输入错误，请重新选择\n\n\n");
          break;
       }
       
     }
      return userflag;
    }
    
    
//注册函数
int signin()
    {
    	read(); 
      struct user *p3,*p2;
      char ch;
      int signinflag;
      
      p2=uhead;
      while (p2->unext!=NULL)
      p2=p2->unext;
      ch='y';
        p3=(struct user*)malloc(LEN);
        printf("\n\t*请按如下格式输入\n");
        printf("\t*请输入注册用户名：");
        gets(p3->id);
        printf("\n\t*请输入密码；");
        gets(p3->code);
        p3->unext=NULL;
        printf("\n\t*请确认上述输入(Y/y),否则按其他任意键继续......"); 
        ch=getche();
        if((ch=='y')||(ch=='Y'))
        {
          p2->unext=p3;
          p2=p3;
          p2->unext=NULL;
          save();  //注册增加的用户保存至文件 
          printf("\n\t*恭喜您注册成功，按任意键继续......");
          getch();
          putch('\n');
          signinflag=2;
        }
        else
        {
          printf("\n\t*未能注册成功！！按任意键继续.......");
          getch();
          putch('\n');
          signinflag=0;
        }
        free(p3);
        return signinflag;
    }
      
        
      
    
      
        
      
    
//登录函数
int login()
    { 
      read();
      char ch,ch1;
      char id[20],code[20];
      struct user *p;
      int flag=0,xflag;
      p=uhead;
      do 
      {
        printf("\n\t*请输用户名（小于19个字符）:");
        gets(id);
        printf("\n\t*请输入密码（小于19个数字）:");
        gets(code);
        while (p!=NULL)
        {
          if((strcmp(id,p->id)==0)&&(strcmp(code,p->code)==0))
          {
          	flag=1;
            break;
		  }
          else
            p=p->unext;
        }
        if(flag)//登陆成功，开始选歌
        {
          while(xflag)
          {
            printf("\n\t* * * * * * * * * * * *欢迎您进入用户点歌界面* * * * * * * * * * * * * *\n");
            printf("\t*                          1.点歌                                      *\n");
            printf("\t*                          2.修改密码                                  *\n");
            printf("\t*                          0.退出                                      *\n");
            printf("\t* * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * \n") ;
            printf("\n\t*请输入选择（1/2/0）:");
            ch=getche();
            ch1=getch(); 
            putch('\n');
            switch(ch)
            {
              case'1':xflag=diange();
              break;
              case'2':xflag=change();
              break;         
			  case'0':xflag=0;
              break;
              default:printf("\n\t*输入错误,请重新输入：");
              xflag=3;break;
            }
          }
          break;
        }
        else  //登陆失败
        {
        	printf("\n\t *用户名或者密码有误！"); 
          printf("\n\t*是否重新输入用户名和密码？【y/n】");
           ch=getche();
           getch();
           putch('\n');
        }
      }
      while (ch=='y'||ch=='Y');
      return 0;
    }
    
            
//点歌函数
int diange()
{
	char song[20],singer[20];
	char ch;
	int flag=1,diangeflag=0;
	while(flag)
	{
		printf("\n\t1.按歌名查找             ");
	    printf("\n\t2.按人名查找             ");
	    printf("\n\t0.退出                    "); 
	    printf("\n\t*请输入选择（1/2/0）:");
        ch=getche();
        getch();
        switch(ch)
        {
    	  case '1':  flag=findsong();
    	  break;
    	  case '2': flag=findsinger();
    	  break;
    	  case '0': 
    	  {
    	  	flag=0;
    	  	diangeflag=1;
    	    break;
		  }
		  
    	  default: printf("\n\t*输入错误,请重新输入：");
    	  break;
	    }
        if(flag==4)//查找失败标志
        {
          printf("\n\t*您所查找的歌曲/歌手不存在！\n");
          printf("\t*是否继续查找？(y/n)");
          ch=getche();
          getch();
          putch('\n');
          if((ch=='y')||(ch=='Y'))
             ;
          else diangeflag=1;
        }
	
	}

	 return diangeflag;
 } 

//修改用户密码//检查过 
int change()
{
	int i;
	char ch,ch1;
	struct user *p,*q;
	
	int flag=1,flag2=0;
	char code[20],code1[20],code2[20];
	printf("请输入您的原始密码：(按回车键确认)");
	gets(code); 
	p=uhead;
		q=NULL;
		while(p!=NULL)
		{
			if(strcmp(p->code,code)==0)
			{
				//flag2=1;
		      	break;
			}
			else
	    	  	p=p->unext;
		}
		
		while(1)
		{
			printf("\n请输入您的新密码：（按回车键确认）");
			gets(code1);
			for(i=0;i<3;i++)
			{
				printf("\n请再次输入确认新密码：（按回车键确认）");
			    gets(code2); 
			    if(strcmp(code1,code2)==0)
			    {
			    	printf("\n请您确认是否永久性保存您所做的修改【y/n】");
			    	ch1=getche();
			    	getch();
					if((ch1=='y')||(ch1=='Y'))
					{  
					    strcpy(p->code,code1);
						save();
			            flag=0;
					}
			    }
			    if(flag==0)
			    	break;
			    else 
			    	continue;
			    
			}
			if(i==3)
			{
				printf("\n修改密码失败，即将进入用户界面界面");
				flag=0;
			}
			else
			{
				printf("\n修改密码成功，请重新登陆");
				break;
			}
		}

	return flag;
} 

//将修改信息保存至文件中

int  save()
{
	FILE *fp;
	struct user *p;
	p=uhead;
	if((fp=fopen("user.txt","w"))==NULL)
	{
		printf("\n\t*保存文件不正常，请核对文件名！\n");
		fclose(fp);
		return 1;
	}
	else
	{
		rewind(fp);
		while (p!=NULL)
		{
			fprintf(fp,"%s\t%s\n",p->id,p->code);
			p=p->unext;
		}
		fclose(fp);
		return 0;
	}
}

//按歌名查找
 int findsong()
     {
     	int i;
       FILE *fp; 
	   char s[20],str[1000];
       struct music  *p;
       char song[20];
       int flag=4;//查找失败标志
       p=head;
       printf("\n\n\t*请输入要查找的歌名：");
       gets(song);
       while(p!=NULL)
       {
         if(strcmp(p->song,song)==0)
         {
         	output(song);
	        fclose(fp);
            flag=1;
            printf("\n\t*按任意键退出......");
            getch();
          }
          p=p->next;
       }
       return flag;
     }
 
 //按歌手查找
 int findsinger()
     {
       char  song[50][20];
       char singer[20];
       int flag=4,i=0,j,k;   //查找失败标志
       struct music *p;
    
       p=head;
       printf("\n\n\t*请输入要查找的歌手姓名：");
       gets(singer);
       while(p!=NULL)
       {
         if(strcmp(singer,p->singer)==0)
         {
          i++;
          strcpy(song[i-1],p->song);
        
         }
        

         flag=1;
         p=p->next;
       }
       if(flag!=4)
       {
         printf("\n\n\t*该歌手的歌曲如下：\n");
         for(j=0;j<i;j++)
         printf("\t*%d\t%s\n", j+1,song[j]);
         printf("\n\t*请输入要查找的歌名序号(数字):");
         scanf("%d",&k) ;
         output(song[k-1]);
         printf("\n\t*按任意键退出......");
         getch();
       }
       return flag;
     }


//打印歌名对应的文件
int output(char p[])
{
	int i;
	FILE *fp; 
	char s[20],str[1000];
		   sprintf(s,"%s.txt",p);
       	   if ((fp=fopen(s,"r"))==NULL)
	       {
	   	    printf("\n\t*can not open file%s\n",s);
		    exit(0);
	       }
	       fgets(str,1000,fp);
	       printf("\n\t歌词：");
	       puts(str);
	       fclose(fp);
	       return 0;
} 

//从文件中读取用户名和密码,存放到链表中 
int read()
{
	FILE *fp;
	struct user *p1,*p2;
	fp=fopen("user.txt","r");
	if(fp==NULL)
	{
		printf("\n\t*未能初始化用户信息\n");
		fclose(fp);
		return 0;
	}
	else
	{
		p1=(struct user*)malloc(LEN);
		uhead=p1;   //将读出的用户信息存放在链表uhead中  
		while(!feof(fp))
		{
			fscanf(fp,"%s\t%s\t\n",p1->id,p1->code);
			p2=p1;
			p1=(struct user*)malloc(LEN);
			p2->unext=p1;
		}
		p2->unext=NULL;
		p2=NULL;
		free(p1);
		fclose(fp);
		return 1;
	}
} 

int main()
 {
 	int i,legalUser=0;
 	char chp='0',ch;
 	InitMusic();
	read();
 	
 	do
	{
		printf("\n * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *");
		printf("\n           					                    	 ");
		printf("\n\t* * * * * * * * * * * *欢迎进入点歌系统* * * * * * * * * * * **");
		printf("\n\t*                        			              *\t");
		printf("\n\t*                        1.用户登录                           *");
		printf("\n\t*                        			              *\t");
		printf("\n\t*                        2.管理员登录                         *");
		printf("\n\t*                        			              *\t");
		printf("\n\t*                        0.退出                               *");
		printf("\n\t*                        			              *\t");
		printf("\n\t*                      请选择进入[1/2/0]                        *");
		printf("\n\t*                        			              *\t");
		printf("\n\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n");
	 
		chp=getch();		
	
		switch(chp)
		{
			case'1':
					if(user()!=0)
						legalUser=1; 
					else
						legalUser=0;
				
					break;
			case'2':
			if(VerificationIdentity()==1)
			{	
				if(Admi()==1)
					legalUser=0;
				break;
			}
			 
					
			else 	legalUser=0;
					break;
			case'0':
					return 0;
			default:
				printf("选择错误！\n");
				legalUser=0;
					break;
			
		}
	
	} while(legalUser==0);
	return 0;
}