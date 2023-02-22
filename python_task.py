import requests
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import psycopg2
import random
from bs4 import BeautifulSoup

##***************BEGINNING OF DATA PREPARATION********************************

#open the downloaded html file with beautiful soup
with open("python_class_question.html") as file:
    soup=BeautifulSoup(file,'lxml')

# extract the table 
table=soup.find_all('td')

#create an empty list
column_header=[]

#append all the table headers,MONDAY,TUESDAY,etc in the list
for i in np.arange(0,10,2):
    
    column_header.append(table[i].contents[0])
    
# Extract the rows'content
row_data=[]
for i in np.arange(1,11,2):
    row_data.append(table[i].contents[0])

#filter individual rows in the row ist
rows=[ v.split(' ') for v in row_data]

# create an empty dictionary and set the keys
data={}
data=data.fromkeys(column_header)

# convert dictionary to pandas dataframe
df=pd.DataFrame(data)

# clean up the data frame to remove the ',' in each cell
for i in range(0,len(df.columns)):
    df[df.columns[i]]=df[df.columns[i]].str.strip(',')

# create a single list of all colors    
x=rows[0]+rows[1]+rows[2]+rows[3]+rows[4]
#clean up to remove  the','
c_data=[ v.strip(',') for v in x]


#Note: c_data  and df are the working data that will be used to answer the questions with some pandas functions

##***************END OF DATA PREPARATION********************************


############ ANSWER TO QUESTION 1,2 ###########################
#decribe the data
y=pd.DataFrame(c_data).iloc[:,0].value_counts()
y.describe()

"""
count    12.000000
mean      7.916667
std       8.306168
min       1.000000
25%       1.750000
50%       5.500000
75%       9.250000
max      30.000000
Answer to Qestion 1-3: 
The mean of the colors cannot be calculated as color is nominal data (non-numeric). However this can still be gotten from the frquency distribution which is not advisable

The modal color (shirt with the popular color) is BLUE because it has the highest frequency from Monday-Friday 

"""
############ ANSWER TO QUESTION 1  ###########################
print("The mean of the colors using the frequency distribution is ",y.describe()[1])

############ ANSWER TO QUESTION 2  ###########################

#summarize the data frame
df.describe()
"""
The ouput of the above codes shows that Blue shirt is the frequent

MONDAY	TUESDAY	WEDNESDAY	THURSDAY	FRIDAY
count	19	19	19	19	19
unique	9	9	8	9	7
top	BLUE	BLUE	BLUE	BLUE	BLUE
freq	6	6	5	7	6
"""

############ ANSWER TO QUESTION 3 ###########################
# sort and compute the median of the data
c_data.sort()
print("Sum of colors: {}".format(len(c_data)))
print("After sorting middle number lies in position: {}th".format(round(len(c_data)/2+0.5)))
print("The median color is {} ".format(c_data[round(len(c_data)/2+0.5)-1]))


"""
ANSWER
Sum of colors: 95
After sorting, the middle number lies in position: 48th
The median color is GREEN 
"""

# compute the frequency of the colors
y=pd.DataFrame(c_data).iloc[:,0].value_counts()

# convert to pandas dataframe
z=pd.DataFrame(y)
z.columns=['frequency']
t=z.reset_index()

############ ANSWER TO QUESTION 4  ###########################

print("The variance of the colors using the frequency distribution is ",y.describe()[2])

############ ANSWER TO QUESTION 5 ###########################

print("The probability of picking a red ball is ",t[t['index']=='RED'][['frequency']].values[0][0]/t.frequency.sum())


############ ANSWER TO QUESTION 6 ###########################
# save frequency table to postgresql
"""
This was connected to my localhost. 
password and username are wrong. Running this code will throw an error
"""
engine=create_engine('postgresql://oluwasola:password@localhost:5432/shirt_colors')
df.to_sql('shirt_colors',engine)


############ ANSWER TO QUESTION 8 ###########################
# Generate a random 4-digit number consisting of only 0s and 1s
random_num = random.choices([0, 1], k=4)

# Convert the random number to base 10 using the int() function
base10_num = int(''.join(map(str, random_num)), 2)

# Print the generated number and its base 10 equivalent
print(f"Generated number: {random_num}")
print(f"Base 10 equivalent: {base10_num}")

############ ANSWER TO QUESTION 9 ###########################
#create function to generate the fib numbers
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    
## get, save, and compute the sum of the fibonacci numbers
fibs=[]
for i in np.arange(30):
    fibs.append(fibonacci(i))
print("The sum of the first 50 numbers in the Fibonacci sequence is:", sum(fibs))