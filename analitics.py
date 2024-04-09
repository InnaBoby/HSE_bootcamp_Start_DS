# -*- coding: utf-8 -*-
"""Analitics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_6dexnJaELk63xzIbhUh4b2mfNZzVwVT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

salary_1 = pd.read_excel('/content/drive/MyDrive/HSE_FinalProject/tab3-zpl_2000-2016.xlsx')
salary_2 = pd.read_excel('/content/drive/MyDrive/HSE_FinalProject/tab3-zpl_2023.xlsx')

def prepare_salary_data (df_1, df_2):

  ''' Функция для конкатенации данных по зарплате из двух таблиц за разные годы'''

  df_1['Unnamed: 0'] = df_1['Unnamed: 0'].apply(lambda x: x.lower().replace('  ', '').replace('  ', ''))
  df_2['Unnamed: 0'] = df_2['Unnamed: 0'].apply(lambda x: x.lower().replace('  ', '').replace('  ', ''))
  salary = df_1.merge(df_2, on ='Unnamed: 0')
  # переводим названия столбцов из int в str
  str_cols = list(map(str, salary.columns.to_list()))
  salary.columns = str_cols
  salary.rename(columns={'Unnamed: 0': 'Sphere'}, inplace=True)
  return salary

salary = prepare_salary_data (salary_1, salary_2)

salary.describe()

salary2 = salary.T
salary2.columns = salary2.iloc[0]
salary2 = salary2[1:]
salary2['Avarage'] = (salary2['добыча полезных ископаемых']+
                      salary2['обрабатывающие производства']+
                      salary2['образование']+
                      salary2['строительство']) / 4
salary2

for col in salary2.columns.to_list():
  salary2[f'Прирост '+ col] = 0
  for indx in range(1, len(salary2)):
    salary2[f'Прирост '+ col][indx] = (salary2[col][indx]*100/salary2[col][indx-1]) - 100
salary2

salary2 = salary2.T

salary2

years = salary2.columns.to_list()
fig, ax1 = plt.subplots()
color = 'tab:blue'
for indx in range(len(salary2[:5])):
  legend_data = salary2.index.to_list()[indx]
  ax1.plot(years, salary2.iloc[indx].to_list(), label=legend_data, linestyle='--')
ax1.set_xlabel('years', color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.tick_params(axis='x', labelcolor=color)
plt.xticks(rotation='vertical')
ax1.set_ylabel('Средняя зарплата, в руб.', color=color)
ax1.set_title("Изменение зарплаты по годам")
ax1.legend()

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Прирост к рошлому году, в %', color=color)
ax2.tick_params(axis='y', labelcolor=color)
for indx in range(5, len(salary2)):
  legend_data = salary2.index.to_list()[indx]
  ax2.plot(years, salary2.iloc[indx].to_list(), label=legend_data)

plt.show()

"""Номинальная зарплата растут, в то время как прирост по отношению к прошлому году имеет тенденцию к снижению"""

salary2.index

