# Filter the uneccesary warnings
import warnings
import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

data = pd.read_csv('data.csv')
# print(data.head(10))
print("\nFirst 10 data ", data.head(10).T)
print("\nShape of the entire Dataset", data.shape)
print("\nDescribe the Columns", data.columns)

Classes = Counter(data['Result'].values)

print(Classes)
print(Classes.most_common())

Classes_Distribution = pd.DataFrame(Classes.most_common(), columns=['Class', 'Number_Of_Observations'])

print(Classes_Distribution)

plt.style.use('ggplot')
subplot = Classes_Distribution.groupby('Class')['Number_Of_Observations'].sum().plot(kind='barh', width=0.2, figsize=(10,8))

subplot.set_title('Class distribution of the websites', fontsize = 15)
subplot.set_xlabel('Number of Observations', fontsize = 14)
subplot.set_ylabel('Class', fontsize = 14)

for i in subplot.patches:
    subplot.text(i.get_width()+0.1, i.get_y()+0.1, \
            str(i.get_width()), fontsize=11)
    
plt.show()