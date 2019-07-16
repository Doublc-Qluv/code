#include <iostream>
using namespace std;
class Arr
{
public:
	Arr()
	{
		pArr = nullptr;
		size = 0;
		cout << "Constructor with no arg" << endl;
	}
	Arr(int m_size)
	{
		size = m_size;
		pArr = new int[size];
		if (pArr == nullptr)
		{
			cout << "Err in new" << endl;
			exit(0);
		}
		else
		{
			for (int i = 0; i < size; i++)
			{
				pArr[i] = 0;
			}
		}
		cout << "Constructor with One arg" << endl;
	}
	Arr(Arr& Arr_M)//Arr pArr = arr
	{
		size = Arr_M.size;
		pArr = new int[size];
		for (int i = 0; i < size; i++)
		{
			pArr[i] = Arr_M.pArr[i];
		}
	}
	
	~Arr()
	{
		delete[] pArr;
		cout << "Destructor" << endl;
	}
	int getSize(){
		if (pArr != nullptr)
		{
			return size*sizeof(int);
		}
		return 0;
	}
	int length(){ return size; }

	void setLength(int len)
	{
		if (len > size)
		{

			if (pArr == nullptr)
			{
				size = len;
				pArr = new int[len];
				if (pArr == nullptr)
				{
					cout << "Err in new" << endl;
					exit(0);
				}
				else
				{
					for (int i = 0; i < size; i++)
					{
						pArr[i] = 0;
					}
				}
			}
			else
			{

				int* tmp = new int[len];
				if (tmp == nullptr)
				{
					cout << "Err in new" << endl;
					exit(0);
				}
				else
				{
					for (int i = 0; i < size; i++)
					{
						tmp[i] = 0;
					}
				}
				for (int i = 0; i < size; i++)
				{
					tmp[i] = pArr[i];
				}
				delete[] pArr;
				pArr = tmp;
				size = len;
			}
		}
	}

	void setVal(int val, int tip)
	{
		if (tip > size - 1)
		{
			cout << "Out of bound" << endl;
		}
		else
		{
			pArr[tip] = val;
		}
	}
	int getVal(int tip)
	{
		if (tip > size - 1 || tip<0)
		{
			cout << "Out of bound" << endl;
		}
		else
		{
			return pArr[tip];
		}
	}
	//重新解释运算符,运算符重载
	int& operator[](int val)
	{
		return pArr[val];
	}
private:
	int* pArr;
	int size;
};
int main()
{
	Arr arr;
	cout << arr.getSize() << endl;
	cout << arr.length() << endl;
	arr.setLength(6);
	cout << arr.getSize() << endl;
	cout << arr.length() << endl;
	
	arr[0] = 2;//arr.[](int i=0)
	
	Arr arr1 = arr;

	

	/*arr.setVal(1, 0);
	arr.setVal(7, 1);
	arr.setVal(12, 2);
	arr.setVal(35, 3);
	arr.setVal(8, 4);

	
	for (int i = 0; i < arr.length(); i++)
	{
		cout << arr.getVal(i) << endl;
		
	}
	
	for (int i = 0; i < arr.length(); i++)
	{
		cout << arr[i] << endl;

	}
*/

	

	//arr[i];// arr.[](int i)

	class String
	{
	public:
		String();
		String(const char* p);
		~String();
		String operator+(const String& str);
		String operator=(const String& str);
		char& operator[](int val);
	private:
		char *pArr;
	};
	


	

	return 0;
}



