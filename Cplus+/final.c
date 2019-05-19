#include <stdio.h>
#include <curses.h>
//#include <conio.h>
#include <stdlib.h>
#include <malloc/malloc.h>
//#include <malloc.h>
#include <string.h>
#define LEN sizeof(struct user) 

//�������� 
int zhuce();
int denglu();
int xiugai();
int read();

int Admi();
int VerificationIdentity();
int changekey();

int InitMusic();
int Savemusic() ;
 
int findsong();
int findsinger();
int dayin(char *p);
int save();
 
int Add();
int Delete();
int Modify();

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


//����Ա���� 
int Admi()
{

			char chp;
			int legalUser;
			printf("\n\n\n* * * * * * * * * * * * * * * ����Ա��¼�ɹ�����* * * * * * * * * * * * * * * *\n");
			printf("\n\n\t*1.���Ӹ���\n");
			printf("\n\n\n\t*2.ɾ������\n");
			printf("\n\n\n\t*3.�޸ĸ���\n");
			printf("\n\n\n\t*4.�޸�����\n");
			printf("\n\n\n\t*0.�˳���¼\n");
			
			printf("\n\n\t��ѡ��[1/2/3/4/0]:");
			chp=getchar();
			switch(chp)
			{
				case'1':
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
				case'4':changekey();
				Admi();
					break;
				case'0':legalUser=0;
					break;
				default:printf("ѡ�����\n");
					legalUser=1;
					Admi();
					break;
			}
			return legalUser;
		}




//����Ա��½
int VerificationIdentity()
{
	char userID[20],password[20];    //����ɼ���������û����Ϳ��� 
	char superUID[20],passWD[20];    //����ļ��ж�ȡ���û����Ϳ��� 
	int i,legalUser;
	char ch;
	FILE *fp;
	legalUser=0;
	fp=fopen("superUser.txt","r");
	if(fp==NULL)
	{
		printf("\n\tȨ���ļ������ڣ������������..\n");
		getchar();
	}
	else
	{
		do
		{
			ch='0';
			printf("\n\n\t\t\t   *����Ա��½*    \t\t\n");
			printf("\n\t*�������û���(<15���ַ�):");
			gets(userID);
			
			printf("\n\t*����������(<15������,��ĸ�����):");
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
				printf("\n\n\t��������Ƿ���Ҫ���������û��������룿(y/n)");
				ch=getchar();
				}
			}
		}
		while((ch=='y')||(ch=='Y'));
	}
	fclose(fp);
	return legalUser;
}






//����Ա�޸����� 
int changekey()
{
	int i;
	char ch;
	char userID[20],password[20];
	char superUID[20],passWD[20];
	FILE *fp;
	
		fp=fopen("superUser.txt","r+");
		if(fp==NULL)
		{
			printf("\n\tȨ���ļ������ڣ������������..\n");
			getchar();
		}
		else 
		{
			do
			{
				printf("\n\n\t*������ԭ����(<15������,��ĸ�����):");
				i=0;
				while((ch=getchar())!='#'&&(i<15))
				{
					putchar('*');
					password[i]=ch;
					i++;
				}		
				password[i]='\0';
			
				rewind(fp);
				while(!feof(fp))
				{
					fscanf(fp,"%s\t%s\t\n",superUID,passWD);
					fclose(fp);
				
					if(strcmp(password,passWD)==0)
					{
						printf("\n\n\t*������������(<15������,��ĸ�����):");
						i=0;
						while((ch=getchar())!='#'&&(i<15))
							{
							putchar('*');
							password[i]=ch;
							i++;
								}		
						password[i]='\0';
					
						printf("\n\n\t*���ٴ�����������(<15������,��ĸ�����):");
						i=0;
						while((ch=getchar())!='#'&&(i<15))
							{
								putchar('*');
								passWD[i]=ch;
								i++;
							}		
							passWD[i]='\0';
					
						if(strcmp(password,passWD)==0)
						{
							fp=fopen("superUser.txt","w");
								if(fp==NULL)
								{
									printf("\n\tȨ���ļ������ڣ������������..\n");
									getchar();
								}
								else 
								{
					
									fprintf(fp,"%s %s",superUID,passWD);
									printf("\n\n\t�޸�����ɹ���");
								}
							fclose(fp);
							break;
						}
							
					}
				
					else 
					{
							printf("\n\n\t*�Ƿ������������룿(y/n)");
							ch=getchar();
							break;
					}
				}
			}while((ch=='y')||(ch=='Y'));
		}

} 

//�������Ŀ¼ 
int Savemusic()
{
	
	FILE *fp;
	struct music *p;
	p=head;
	if((fp=fopen("music.txt","w"))==NULL)
	{
		printf("\n�����ļ�����������˶��ļ�����\n");
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




//���Ӹ��� 
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
		printf("\n\n\n\n\t\t**���Ӹ���**");
		printf("\n\n\n\t���������밴���¸�ʽ���룺\n");
		printf("\n\t*����������������");
		gets(p3->song);
		printf("\n\n\t*��������������������");
		gets(p3->singer);
		printf("\n\n\t*��������Ӹ��");
		printf("\n\t");
		gets(str);
		p3->next=NULL;
		
		ch1='0';
		printf("\n\n\t��ȷ����������[y/Y],�����������������");
		ch2=getchar();
		if(tolower(ch2)=='y')
		{
			p2->next=p3; 
			p2=p3;
			
			
			sprintf(song,"%s.txt",p3->song);                    //�������Ӹ������д���ļ��� 
	   	 	if ((fp2=fopen(song,"w"))==NULL)
	 			
					printf("can not open file\n");
				
			else
			{
				fputs(str,fp2);
			}
			p3=NULL;
			fclose(fp2);
			printf("\n\n\t�������ӳɹ���");
		}
		else
		{
		
			printf("\n\n\tδ�����Ӹ������������������");
			getchar();
				
		}
		printf("\n\n\t�Ƿ�������һ�׸裬������ӣ�����[y/Y]���������������");
		ch1=getchar();
	
	}
	p2=NULL;
	return 1;
	
}

//����ɾ��
int  Delete(void)
{
	linklist *q,*p;
	char Dsong[20],song[25];
	int
	ch='y';
	while(tolower(ch)=='y')
	{
		printf("\n\n\t*��������Ҫɾ���ĸ��������س���ȷ�ϣ���");
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
				printf("\n\n\t*��Ҫɾ���ĸ����ǣ�%s,�ø����Ϊ:%s\n",p->song,p->singer);
				printf("\n\t�����ٴ�ȷ��[y/Y]:");
				ch=getchar();
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
			printf("\n\n\t��������Ҫɾ���ĸ������밴���������\n");
			getchar;
		}
		printf("\n\n\t*�Ƿ����ɾ����һ�׸���[y/Y],��ɾ��������������...\n");
		ch=getchar();
	}
	return 1;
} 



//�޸ĸ�����Ϣ
int Modify()
{
	linklist *q,*p2,*p3;
	char Msong[20];
	char ch,str[1024],s[20];
	FILE *fp1,*fp2;
	char song[25],song1[25],song2[25];
	do
	{
		printf("\n\n\t*��������Ҫ�޸ĵĸ��������س���ȷ�ϣ���");
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
		
	
				printf("\n\n\t*��Ҫ�޸ĵĸ����ǣ�%s,�ø����Ϊ %s\n",p->song,p->singer);
				printf("\n\t*��������Ҫ�޸ĵ���Ϣ����:");
				printf("\n\t1.������  2.������  3.���\n");
				printf("\n\t��ѡ��[1/2/3]:");
				ch=getchar();
				switch(ch)
				{
					case'1':printf("\n\t\n*�������޸ĸ�������");
							gets(p->song);
							sprintf(song1,"%s.txt",Msong); 
							sprintf(song2,"%s.txt",p->song); 
							rename(song1,song2);
							break;
					case'2':printf("\n\t*�������޸ĸ�����������");
							gets(p->singer);
							break;
					case'3':printf("\n\t*���������Ӹ��\n");
							gets(str);
							sprintf(song,"%s.txt",p->song);                    //�������Ӹ������д���ļ��� 
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
							
					default:printf("\n\t\n�����������������:\n");
							break;
				}
			
		if(p==NULL)
		{
			printf("\n\n\t��������Ҫ�޸ĵĸ������밴���������\n");
			getchar;
		}
		printf("\n\n\t*�Ƿ�����޸���һ�׸���[y/Y],���޸İ�����������...\n");
		ch=getchar();
	} while(tolower(ch)=='y');
	return 1;
} 



//��ʼ��������Ϣ
int InitMusic()
{
	FILE *fp;
	struct music *p1,*p2;
	fp=fopen("music.txt","r");
	if(fp==NULL)
	{
		printf("δ�ܳ�ʼ��\n");
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
		free(fp);
		p1=NULL;
		p1=head;
		
		fclose(fp);
		return 1;
	}
	
} 
//�û���¼���� 
int user()
    {
      int userflag=1; 
      char ch,ch1;
      while(userflag)
     {
        printf("\n\t ----------------------��ӭ�����û�����----------------------\n");
        printf("\t|                        1.ע��                              |\n");
        printf("\t|                        2.��¼                              |\n");
        printf("\t|                        0.�˳�                              |\n");
        printf("\t ------------------------------------------------------------\n");
        printf("\t*����������ѡ��(0/1/2):");
        ch=getchar();
        ch1=getchar();
        switch (ch)
       {
          case'1' : userflag=zhuce();//����ע��ģ��,ע��ɹ�����2 
          break;
          case'2' : userflag=denglu();//���õ�¼ģ�飬��¼�ɹ�����1 
          break;
          case'0' : userflag=0;
          break;
          default : printf("\n\t*�������������ѡ��\n\n\n");
          break;
       }
       
     }
      return userflag;
    }
    
    
//ע�ắ��
int zhuce()
    {
    	read(); 
      struct user *p3,*p2;
      char ch;
      int zhuceflag;
      
      p2=uhead;
      while (p2->unext!=NULL)
      p2=p2->unext;
      ch='y';
        p3=(struct user*)malloc(LEN);
        printf("\n\t*�밴���¸�ʽ����\n");
        getchar();
        printf("\t*������ע���û�����");
        gets(p3->id);
        printf("\n\t*���������룻");
        gets(p3->code);
        p3->unext=NULL;
        printf("\n\t*��ȷ����������(Y/y),�����������������......"); 
        ch=getchar();
        if((ch=='y')||(ch=='Y'))
        {
          p2->unext=p3;
          p2=p3;
          p2->unext=NULL;
          save();  //ע�����ӵ��û��������ļ� 
          printf("\n\t*��ϲ��ע��ɹ��������������......");
          getchar();
          putch('\n');
          zhuceflag=2;
        }
        else
        {
          printf("\n\t*δ��ע��ɹ����������������.......");
          getchar();
          putch('\n');
          zhuceflag=0;
        }
        free(p3);
        return zhuceflag;
    }
      
        
      
    
      
        
      
    
//��¼����
int denglu()
    { 
      read();
      char ch,ch1;
      char id[20],code[20];
      struct user *p;
      int flag=0,xflag;
      p=uhead;
      do 
      {
        printf("\n\t*�����û�����С��19���ַ���:");
        gets(id);
        printf("\n\t*���������루С��19�����֣�:");
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



        if(flag)//��½�ɹ�����ʼѡ��
        {
          while(xflag)
          {
            printf("\n\t* * * * * * * * * * * *��ӭ�������û�������* * * * * * * * * * * * * *\n");
            printf("\t*                          1.���                                      *\n");
            printf("\t*                          2.�޸�����                                  *\n");
            printf("\t*                          0.�˳�                                      *\n");
            printf("\t* * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * * \n") ;
            printf("\n\t*������ѡ��1/2/0��:");
            ch=getchar();
            ch1=getchar(); 
            putch('\n');
            switch(ch)
            {
              case'1':xflag=diange();
              break;
              case'2':xflag=xiugai();
              break;         
			  case'0':xflag=0;
              break;
              default:printf("\n\t*�������,���������룺");
              xflag=3;break;
            }
          }
          break;
        }
        else  //��½ʧ��
        {
        	printf("\n\t *�û���������������"); 
          printf("\n\t*�Ƿ����������û��������룿��y/n��");
           ch=getchar();
           getchar();
           putch('\n');
        }
      }
      while (ch=='y'||ch=='Y');
      return 0;
    }
    
            
//��躯��
int diange()
{
	char song[20],singer[20];
	char ch;
	int flag=1,diangeflag=0;
	while(flag)
	{
		printf("\n\t1.����������             ");
	    printf("\n\t2.����������             ");
	    printf("\n\t0.�˳�                    "); 
	    printf("\n\t*������ѡ��1/2/0��:");
        ch=getchar();
        getchar();
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
		  
    	  default: printf("\n\t*�������,���������룺");
    	  break;
	    }
        if(flag==4)//����ʧ�ܱ�־
        {
          printf("\n\t*�������ҵĸ���/���ֲ����ڣ�\n");
          printf("\t*�Ƿ�������ң�(y/n)");
          ch=getchar();
          getchar();
          putch('\n');
          if((ch=='y')||(ch=='Y'))
             ;
          else diangeflag=1;
        }
	
	}

	 return diangeflag;
 } 
//�޸��û�����//���� 
int xiugai()
{
	int i ,flag;
	char ch,ch1;
	struct user *p,*q;
	do
	{
		int i, flag=1;
		char code[20],code1[20],code2[20];
		printf("����������ԭʼ���룺(���س���ȷ��)");
		gets(code); 
		p=uhead;
		q=NULL;
		while(p!=NULL)
		{
			if(strcmp(p->code,code)==0)
		      break;
			else
	    	  p=p->unext;
		}
		
		while(1)
		{
			printf("\n���������������룺�����س���ȷ�ϣ�");
			gets(code1);
			for(i=0;i<5;i++)
			{
				printf("\n���ٴ�����ȷ�������룺�����س���ȷ�ϣ�");
			    gets(code2); 
			    if(strcmp(code1,code2)==0)
			    {
			    	printf("\n����ȷ���Ƿ������Ա������������޸ġ�y/n��");
			    	
			    	ch1=getchar();
			    	getchar();
			    	
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
			if(i==5)
			{
				printf("\n�޸�����ʧ�ܣ����������û��������");
				flag=0;
			}
			break;
		}
		printf("\n�Ƿ�Ҫ�޸����롾y/n��") ;
		ch=getchar();
		getchar();	 
	}while(ch=='y'||ch=='Y');
	return flag;
} 
//���޸���Ϣ�������ļ���

int  save()
{
	FILE *fp;
	struct user *p;
	p=uhead;
	if((fp=fopen("user.txt","w"))==NULL)
	{
		printf("\n\t*�����ļ�����������˶��ļ�����\n");
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

//����������
 int findsong()
     {
     	int i;
       FILE *fp; 
	   char s[20],str[1000];
       struct music  *p;
       char song[20];
       int flag=4;//����ʧ�ܱ�־
       p=head;
       printf("\n\n\t*������Ҫ���ҵĸ�����");
       gets(song);
       while(p!=NULL)
       {
         if(strcmp(p->song,song)==0)
         {
         	dayin(song);
	        fclose(fp);
            flag=1;
            printf("\n\t*��������˳�......");
            getchar();
          }
          p=p->next;
       }
       return flag;
     }
 //�����ֲ���
 int findsinger()
     {
       char  song[50][20];
       char singer[20];
       int flag=4,i=0,j,k;   //����ʧ�ܱ�־
       struct music *p;
    
       p=head;
       printf("\n\n\t*������Ҫ���ҵĸ���������");
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
         printf("\n\n\t*�ø��ֵĸ������£�\n");
         for(j=0;j<i;j++)
         printf("\t*%d\t%s\n", j+1,song[j]);
         printf("\n\t*������Ҫ���ҵĸ������(����):");
         scanf("%d",&k) ;
         dayin(song[k-1]);
         printf("\n\t*��������˳�......");
         getchar();
       }
       return flag;
     }
//��ӡ������Ӧ���ļ�
int dayin(char p[])
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
	       printf("\n\t");
	       puts(str);
	       fclose(fp);
	       return 0;
} 
//���ļ��ж�ȡ�û���������,��ŵ������� 
int read()
{
	FILE *fp;
	struct user *p1,*p2;
	fp=fopen("user.txt","r");
	if(fp==NULL)
	{
		printf("\n\t*δ�ܳ�ʼ���û���Ϣ\n");
		fclose(fp);
		return 0;
	}
	else
	{
		p1=(struct user*)malloc(LEN);
		uhead=p1;   //���������û���Ϣ���������uhead��  
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
 	//InitMusic();
	read();
 	
 	do
	{
		printf("\n * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *");
		printf("\n           					                    	 ");
		printf("\n\t* * * * * * * * * * * *��ӭ������ϵͳ* * * * * * * * * * * **");
		printf("\n\t*                        			              *\t");
		printf("\n\t*                        1.�û���¼                           *");
		printf("\n\t*                        			              *\t");
		printf("\n\t*                        2.����Ա��¼                         *");
		printf("\n\t*                        			              *\t");
		printf("\n\t*                        0.�˳�                               *");
		printf("\n\t*                        			              *\t");
		printf("\n\t*                      ��ѡ�����[1/2/0]                        *");
		printf("\n\t*                        			              *\t");
		printf("\n\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n");
	 
		chp=getchar();		
	
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
				system("cls");
				printf("ѡ�����\n");
				legalUser=0;
					break;
			
		}
	
	} while(legalUser==0);
	return 0;
}

