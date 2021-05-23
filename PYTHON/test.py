import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %matplotlib inline

#读取数据集 loan_data.csv，并查看前5条数据
df=pd.read_csv('loan_data.csv',encoding='utf-8') 
zero_col_count = dict(df['not.fully.paid'].value_counts())#统计第0列元素的值的个数

'''x = df['fico']
y = df['int.rate']
for i in df['not.fully.paid']:
    #if i == 1:
    plt.scatter(x,y)
    plt.axis()
    plt.title("not fully paid")
    plt.xlabel("FICO")
    plt.ylabel("interest rate")
plt.show()
'''
  
'''size_mapping = {  
           'XL': 3,  
           'L': 2,  
           'M': 1}  
df['size'] = df['size'].map(size_mapping)  
  
class_mapping = {label:idx for idx,label in enumerate(set(df['class label']))}  
df['class label'] = df['class label'].map(class_mapping)  '''

zero_col_count = dict(df['purpose'].value_counts())
#print(zero_col_count)
#print(pd.get_dummies(df))

feature_cols = ['installment','log.annual.inc','dti','fico']
X = df[feature_cols]
y = df['int.rate']