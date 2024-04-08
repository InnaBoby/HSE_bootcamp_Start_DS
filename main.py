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
salary_1 = pd.read_excel('data/tab3-zpl_2000-2016.xlsx')
salary_2 = pd.read_excel('data/tab3-zpl_2023.xlsx')
salary = prepare_salary_data(salary_1, salary_2)



st.text('Среднемесячная номинальная начисленная заработная плата работников организаций \nпо видам экономической деятельности в Российской Федерации за 2000-2023 гг., в рублях')
st.table(salary)

#подгружаем данные по инфляции
url = 'https://уровень-инфляции.рф/таблицы-инфляции'
inflation = get_table(url)

#inflation = pd.read_csv('data/data.csv')
#inflation = inflation.drop(columns=['Unnamed: 0'])
if (st.checkbox('Показать данные по инфляции')):
    st.table(inflation.head(5))
inflation = inflation.fillna(0)


case = st.sidebar.selectbox('Показать', ['Динамику номинальной зарплаты по отраслям', 'Разницу между номинальной и реальной зарплатой за год'])
if case == 'Динамику номинальной зарплаты по отраслям':

    #Добавляем кнопку, которая отображает график
    if (st.button('Показать график')):
        with st.spinner('Рисуем, рисуем, рисуем...'):
            time.sleep(2)
        st.write(salary_dinamic_graph(salary))
        st.markdown('**Выводы:**\n1) за анализируемый период наблюдается **положительная** динамика среднемесячной номинальной начисленной зарплаты по рассматриваемым отраслям.\n2) Среднемесячная номинальная начисленная зарплата в отрасли "Добыча полезных ископаемых" **больше**, чем в других рассматриваемых отраслях и равна 130 826 руб. (в 2023г.).  В то же время, в отрасли "Добыча полезных ископаемых" наблюдается **наименьший** относительный прирост уровня зарплат в 2023г. к 2000г. (+2102%)\n3) Среднемесячная номинальная начисленная зарплата в отрасли "Образование" **меньше**, чем в других рассматриваемых отраслях и равна 54 263 руб. (в 2023г.). При этом, в отрасли "Образование" наблюдается **наибольший** относительный прирост уровня зарплат в 2023г. к 2000г. (+4275%)\n4) Средний уровень зарплат по 4-рём анализируемым отраслям (сиреневый пунктир) **выше**, чем средние зарплаты во всех отраслях, кроме "Добычи полезных ископаемых".')

else:
    year = st.sidebar.selectbox('Реальная зарплата за', salary.columns.to_list()[2:])
    if (st.button('Показать график')):
        with st.spinner('Рисуем, рисуем, рисуем...'):
            time.sleep(2)
        st.write(real_salary_graph(year, inflation, salary))



