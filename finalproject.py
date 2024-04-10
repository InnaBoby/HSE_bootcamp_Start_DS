# -*- coding: utf-8 -*-
"""FinalProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_6dexnJaELk63xzIbhUh4b2mfNZzVwVT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

#отображение всех столбцов таблицы - для Colab
#pd.set_option('display.max_columns', None)




def get_table(url, indx):

  ''' Функция для загрузки данных по инфляции с сайта и сохранении в файл data.csv'''

  r=requests.get(url)
  df=pd.read_html(r.content)[indx]
  return df





#load salary data
#salary_1 = pd.read_excel('/content/drive/MyDrive/HSE_FinalProject/tab3-zpl_2023.xlsx')
#salary_2 = pd.read_excel('/content/drive/MyDrive/HSE_FinalProject/tab3-zpl_2000-2016.xlsx')

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





def salary_dinamic_graph (df, df2=False):

  ''' Функция для отрисовки графиков динамики средних зарплат по отраслям по годам'''

  avarage_salary = df.describe().iloc[1]
  years = df.columns.to_list()[1:]
  fig, ax1 = plt.subplots(figsize=(10, 5), layout='constrained')
  color = 'tab:blue'
  for indx in range(len(df)):
    x_data = df.iloc[indx].to_list()[1:]
    legend_data = df.iloc[indx].to_list()[0]
    ax1.plot(years, x_data, label=legend_data)

  # добавим график среднего уровня зарплат по 4-ем отраслям
  ax1.plot(years, avarage_salary, label='avarage_salary', linestyle='--')
  ax1.set_xlabel('years')
  plt.xticks(rotation='vertical')
  ax1.set_ylabel('salary')
  ax1.set_title("Изменение зарплаты по годам")
  ax1.legend()

  if df2:
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Дополнительные данные', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.plot(df2, label='Дополнительные данные', linestyle='-.', color=color)
    ax2.legend(loc='upper right')

  return fig





def real_salary_graph(year, inflation, salary):
    
    ''' Функция для добавления сравнения с прошлым годом номинальной и реальной зп'''
    
  year = int(year)
  infl = inflation['Всего'] [inflation['Год'] == year].item()
  correct_on_infl = salary[str(year)] * ((100 - infl) / 100)
  data = salary[['Sphere', str(year-1), str(year)]]
  data['correct_on_inflation'] = correct_on_infl

  x = np.arange(len(data))

  fig, ax = plt.subplots(figsize=(10, 5))
  # столбец для предыдущего года
  v_1 = ax.bar(x - 0.3, data[str(year-1)], color='green', width=0.3, label=str(year-1))
  ax.bar_label(v_1, padding=3)
  # столбцы для выбранного года
  v_2 = ax.bar(x, data[str(year)], color='blue', width=0.3, label=str(year))
  ax.bar_label(v_2, padding=3)
  # столбцы для скорректированной на инфляцию зарплаты выбранного года
  v_3 = ax.bar(x + 0.3, data['correct_on_inflation'], color='red', width=0.3, label='corrected on inflation')
  ax.bar_label(v_3, padding=3)
  # подпись меток оси х
  ax.set_xticks(x, data['Sphere'].to_list())
  ax.set_xlabel('Отрасли')
  ax.set_ylabel('Средняя зарплата в отрасли, в рублях')
  ax.set_title("Динамика изменения реальных зарплат с учетом инфляции")
  ax.legend()

  return fig



def add_prirost(salary):
    
''' Функция для добавления графика прироста'''
    
  salary2 = salary.T
  salary2.columns = salary2.iloc[0]
  salary2 = salary2[1:]
  salary2['Avarage'] = (salary2['добыча полезных ископаемых'] +
                        salary2['обрабатывающие производства'] +
                        salary2['образование'] +
                        salary2['строительство']) / 4
  for col in salary2.columns.to_list():
    salary2[f'Прирост ' + col] = 0
    for indx in range(1, len(salary2)):
      salary2[f'Прирост ' + col][indx] = (salary2[col][indx] * 100 / salary2[col][indx - 1]) - 100

  salary2 = salary2.T

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

  ax2 = ax1.twinx()
  color = 'tab:red'
  ax2.set_ylabel('Прирост к рошлому году, в %', color=color)
  ax2.tick_params(axis='y', labelcolor=color)
  for indx in range(5, len(salary2)):
    legend_data = salary2.index.to_list()[indx]
    ax2.plot(years, salary2.iloc[indx].to_list(), label=legend_data)
  ax2.legend()

  return fig


def add_real(salary):

    ''' Функция для добавления скорректированной на инфляцию зп'''
    
    salary3 = salary.T
    salary3.columns = salary3.iloc[0]
    salary3 = salary3[1:]
    
    for col in salary3.columns.to_list():
      salary3[f'Реальная ЗП '+ col] = 0
      for indx in range(len(salary3)):
        salary3[f'Реальная ЗП '+ col][indx] = float('%.2f' %float(salary3[col][indx]*((100 - inflation_data[indx])/100)))
    
    salary3 = salary3.T
    
    years = salary3.columns.to_list()
    
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    for indx in range(4):
      legend_data = salary3.index.to_list()[indx]
      ax1.plot(years, salary3.iloc[indx].to_list(), label=legend_data)
        
    ax1.set_xlabel('years', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.tick_params(axis='x', labelcolor=color)
    plt.xticks(rotation='vertical')
    ax1.set_ylabel('Средняя зарплата, в руб.', color=color)
    ax1.set_title("Изменение зарплаты по годам")
    ax1.legend()
    
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Реальная зп, в тыс руб', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    for indx in range(4, len(salary3)):
      ax2.plot(years, salary3.iloc[indx].to_list(), linestyle='--')
    ax2.set_yscale('linear')
    ax2.legend('Реал', loc = 'upper right')
    
    return fig
