#include <iostream>
#include <string.h>
using namespace std;

class String
{
private:
    /* data */
    char *pString;
    int size;
public:
    String(const char * str): pString(NULL)
    {
        if(str != NULL)
        {

            this->pString = new char(strlen(str) + 1);
            if (this->pString == NULL)
            {
                cout << "new error!" << endl;
                exit(-1);
            }
            strcpy(this->pString, str);
        }
        cout << "Constructor with One arg deafult NULL" << endl;
    }
    String(const String& str)
    {
        if (str.pString == NULL)
        {
            this->pString = NULL;
        }
        else
        {
            this->pString = new char(strlen(str)+1);
            if (this->pString == NULL)
            {
                cout<< "Err in new "<<endl;
                exit(-1);
            }
            strcpy(this->pString, str.pString); 
        }
        
        

    }
    ~String()
    {
        if (this->data != NULL)
        {
            delete pString;
            pString = NULL;
            cout << "Destructor" << endl;
        }
    }
    String operator+(const String& str)
    {
        String newString;
        if (str.pString == NULL)
        {
            newString = *this;
        }
        else if (this->pString == NULL)
        {
            newString = str;
        }
        else
        {
            newString.pString = new char(strlen(this->pString) + strlen(str.pString) + 1);
            strcpy(newString.pString, this->pString);
            strcat(newString.pString, str.pString);
        }
        return newString;
    }
    String operator=(const String& str)
    {
        if (this->pString!= str.pString)
        {
            delete this->pString;
            this->pString = NULL;

            if (str.pString != NULL)
            {
                this->pString = new char(strlen(str.pString) + 1);
                if (this->pString == NULL)
                {
                    cout << "new error!" << endl;
                    exit(-1);
                }
                strcpy(this->pString, str.pString);
            }
        }

        return *this;
    }
};

int main1(){
    String str1 = "s";
    cout<< str1<<endl;
    return 0;
}

/* 
    继承
    在原有代码基础上进行更详细的定义，用来代码复用
    拿到原有类的内容
    改造原有类的内容
    添加属于自己的新内容
*/

/*
    类型兼容性原则
    子类是一种、特殊的父类
    子类的对象可以初始化父类的对象
    父类指针可以访问子类的
 */

/* 
    多态，接收不同的对象，产生不同的结果
    1.重载多态：知道对象
    2.运行多态：不知道对象，运行时多态

    重载多态  函数多态（编译时多态
    强制多态  强制类型多态（编译时多态
    参数化多态  模版（编译时多态
    包含多态  虚函数重写（运行是多态
    关键字：virtual
    虚函数表指针 Vptr

*/

/* 
    模板：
    template <typename T>
    * 类 模版
    函数模板->模板函数->编译

*/