# This is a sample Python script.
import streamlit as st
from PIL import Image
import time
import pandas as pd
from finalproject import *

import matplotlib.pyplot as plt
import requests

st.subheader ('Итоговый проект буткэмпа ВШЭ "Старт в DataScience"')
st.title('Анализ средних зарплат по отраслям')
img = Image.open('dinamika_zarplati.jpg')
st.image(img)


#подгружаем данные по средним номинальным зарплатам
salary_1 = pd.read_excel('tab3-zpl_2000-2016.xlsx')
salary_2 = pd.read_excel('tab3-zpl_2023.xlsx')
salary = prepare_salary_data(salary_1, salary_2)

st.text('Среднемесячная номинальная начисленная заработная плата работников организаций \nпо видам экономической деятельности в Российской Федерации за 2000-2023 гг., в рублях')
st.table(salary)


#подгружаем данные по инфляции
url = 'https://уровень-инфляции.рф/таблицы-инфляции'
inflation = get_table(url, 0)
inflation = inflation.fillna(0)
inflation = inflation[['Год', 'Всего']][1:25]
#inflation['Всего'] = inflation['Всего'].apply(lambda x: '%.2f' %float(x))
inflation_data = inflation['Всего'].to_list()
inflation_data.reverse()
#inflation = pd.read_csv('data/data.csv')
#inflation = inflation.drop(columns=['Unnamed: 0'])

#подгружаем данные по курсу доллара
url = 'https://bhom.ru/currencies/usd/?sb=yes&startdate=01.01.2000&enddate=10.01.2024&ysclid=lus5nof585509270363'
usd = get_table(url, -1)
usd = usd[2:26]
usd[1] = usd[1].apply(lambda x: '%.2f' %float(x))
usd_data = usd[1].to_list()
usd_data.reverse()

#Подгружаем данные по безработице
url = 'https://ruxpert.ru/Статистика:Уровень_безработицы_в_России'
unemp = get_table(url, 0)
unemp = unemp[['Год', 'Уровень безработицы (% от населения)']]
unemp_data = unemp['Уровень безработицы (% от населения)'].to_list()

#Подгружаем данные по ВВП
url = 'https://be5.biz/makroekonomika/gdp/ru.html#main'
vvp = get_table(url, 1)
vvp = vvp[['год', 'ВВП, млрд. долл.']]
vvp_data = vvp['ВВП, млрд. долл.']
vvp_data.drop(columns=['постоянные цены 1990'], inplace=True)
vvp_data['Год'] = vvp['год']
vvp_data = vvp_data[10:]
vvp_data = vvp_data['текущие цены'].to_list()

case = st.sidebar.selectbox('Показать', ['Динамику номинальной зарплаты по отраслям', 'Разницу между номинальной и реальной зарплатой за год'])
if case == 'Динамику номинальной зарплаты по отраслям':
    add = st.selectbox('Добавить данные по ',
                       ['не добавлять другие', 'инфляция', 'курс доллара', 'уровень безработицы', 'ВВП', 'Прирост к прошлому году'])

    #Добавляем кнопку, которая отображает график
    if add == 'не добавлять другие':
        if (st.button('Показать график')):
            with st.spinner('Рисуем, рисуем, рисуем...'):
                time.sleep(2)
            st.write(salary_dinamic_graph(salary))
            st.markdown('**Выводы:**\n1) за анализируемый период наблюдается **положительная** динамика среднемесячной номинальной начисленной зарплаты по рассматриваемым отраслям.\n2) Среднемесячная номинальная начисленная зарплата в отрасли "Добыча полезных ископаемых" **больше**, чем в других рассматриваемых отраслях и равна 130 826 руб. (в 2023г.).  В то же время, в отрасли "Добыча полезных ископаемых" наблюдается **наименьший** относительный прирост уровня зарплат в 2023г. к 2000г. (+2102%)\n3) Среднемесячная номинальная начисленная зарплата в отрасли "Образование" **меньше**, чем в других рассматриваемых отраслях и равна 54 263 руб. (в 2023г.). При этом, в отрасли "Образование" наблюдается **наибольший** относительный прирост уровня зарплат в 2023г. к 2000г. (+4275%)\n4) Средний уровень зарплат по 4-рём анализируемым отраслям (сиреневый пунктир) **выше**, чем средние зарплаты во всех отраслях, кроме "Добычи полезных ископаемых".')

    elif add == 'инфляция':
            if (st.checkbox('Показать данные')):
                st.table(inflation.head(5))
            if (st.button('Показать график')):
                with st.spinner('Рисуем, рисуем, рисуем...'):
                    time.sleep(2)
                st.write(salary_dinamic_graph(salary, inflation_data))

    elif add == 'курс доллара':
            if (st.checkbox('Показать данные')):
                st.table(usd.head(5))
            if (st.button('Показать график')):
                with st.spinner('Рисуем, рисуем, рисуем...'):
                    time.sleep(2)
                st.write(salary_dinamic_graph(salary, usd_data))

    elif add == 'уровень безработицы':
            if (st.checkbox('Показать данные')):
                st.table(unemp.head(5))
            if (st.button('Показать график')):
                with st.spinner('Рисуем, рисуем, рисуем...'):
                    time.sleep(2)
                st.write(salary_dinamic_graph(salary, unemp_data))

    elif add == 'ВВП':
            if (st.checkbox('Показать данные')):
                st.table(vvp.head(5))
            if (st.button('Показать график')):
                with st.spinner('Рисуем, рисуем, рисуем...'):
                    time.sleep(2)
                st.write(salary_dinamic_graph(salary, vvp_data))

    elif add == 'Прирост к прошлому году':
            
            if (st.button('Показать график')):
                with st.spinner('Рисуем, рисуем, рисуем...'):
                    time.sleep(2)
                st.write(add_prirost(salary))
                st.text('Номинальная зарплата растет, в то время как прирост по отношению к прошлому году имеет тенденцию к снижению')

else:
    year = st.sidebar.selectbox('Реальная зарплата за', salary.columns.to_list()[2:])
    if (st.button('Показать график')):
        with st.spinner('Рисуем, рисуем, рисуем...'):
            time.sleep(2)
        st.write(real_salary_graph(year, inflation, salary))



