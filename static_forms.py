from data_sql import get_newest_list_beton_or_lista
from order import Order
import re

import logging
from pprint import pprint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pandas import Series, DataFrame
rng = np.random.default_rng(123545)


# %config Completer.use_jedi = False


# region logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
lg = logging.debug
cr = logging.critical
inf = logging.info
exp = logging.exception
# logging.disable(logging.DEBUG)
# logging.disable(logging.INFO)
# logging.disable(logging.CRITICAL)
# logging_end
# endregion


def get_list_construction_place(date_order="10.02.2025"):
    """возвращает список словарей словарь заказов на основание класса order его 
    переменные которые достаёт из базы данных на дату

    Args:
        date_order (str, optional): _description_. Defaults to "07.02.2025".
    """
    orders = {}
    count = 1
    df_bud = []

    for item in get_newest_list_beton_or_lista("beton", date_order):
        orders[f"{count}bud"] = Order(date_order, *item)
        count += 1

    for key_bud in orders.keys():
        bud = orders[key_bud]

        df_bud.append({
            "name": bud.name[:30]+"...",
            "meter": bud.metres,
            "time": bud.times,
            "start_time": bud.start_time,
            "finish_time": bud.finish_time,
            "list_of_loads": bud.list_of_loads,
            "it_is_zaprawa": bud.it_is_zaprawa,
            "it_is_concret": bud.it_is_concret,
            "list_of_courses": bud.list_of_courses,
            "pompa_dzwig": bud.pompa_dzwig,
            "reszta": bud.reszta,
            "date_order": bud.date_order,
            "date_order": bud.date_order,
        })

    return df_bud


def rozklad_curs(df_orders=get_list_construction_place()):

    try:
        bud = DataFrame(df_orders)

        # УБЕРАЕМ СУХОЙ БЕТОН
        bud_without_dry = bud[bud["it_is_zaprawa"] | bud["it_is_concret"]]
        # оставляем название курсы метров и курсы выселки
        rozklad_curs = bud_without_dry[['list_of_loads', 'list_of_courses', 'name', 'reszta', 'it_is_zaprawa', 'pompa_dzwig']].explode(
            ['list_of_loads', 'list_of_courses', 'reszta']).sort_values('list_of_loads')

        graph = rozklad_curs.copy()

        rozklad_curs["list_of_loads"] = rozklad_curs["list_of_loads"].dt.time
        rozklad_curs['list_of_loads'] = rozklad_curs['list_of_loads'].apply(
            lambda x: x.strftime('%H:%M'))

        rozklad_curs["it_is_zaprawa"] = rozklad_curs["it_is_zaprawa"].replace(
            {True: 'zap', False: 'bet'})
        rozklad_curs["pompa_dzwig"] = rozklad_curs["pompa_dzwig"].replace(
            {True: 'pom', False: 'dz'})

        rozklad_curs = rozklad_curs.reset_index(drop=True)
        rozklad_curs.index = rozklad_curs.index+1

        rozklad_curs.columns = ["time", 'metrów',
                                'budowa', 'reszta', 'mat', 'p/d']

        html_table = rozklad_curs.to_html(
            index=True, table_id="rozklad_curs", classes='rozklad_curs_tab', border=0, justify='center')

        # html_table = re.sub(r'<tr style="text-align: right;">', '<tr>', html_table)

        graph.set_index('list_of_loads', inplace=True)
        graph_corect = graph.resample('h').sum()
        graph_corect = graph_corect[['list_of_courses', 'reszta', 'name']]
        graph_corect.columns = ['intensywność m/g',
                                'nadal trzeba wysłać', 'name']

        fig = px.line(graph_corect, x=graph_corect.index,
                      y=['intensywność m/g', 'nadal trzeba wysłać', 'name'],
                      labels={'list_of_loads': 'time'},
                      title='Intensywność pracy',
                      hover_data={'name': True},
                      markers=True
                      )

        fig.update_layout(
            # Установить цвет фона графика в прозрачный
            plot_bgcolor='rgba(255, 255, 255, 0)',
            # Установить цвет фона области фигуры в прозрачный
            paper_bgcolor='rgba(255, 255, 255, 0.5)',
            yaxis_title='Metrów',
            margin=dict(l=1, r=1, t=15, b=5),
            legend_title='',
            title=dict(
                y=0.91,
                x=0.09,  # Смещение заголовка вправо
                xanchor='left',  # Определяет выравнивание заголовка
                font=dict(
                        family='Arial',
                        size=12,
                        color='black'
                )  # Размер шрифта для заголовка

            ),
            xaxis=dict(
                automargin=True,
                title=dict(
                    standoff=5  # Установка отступа для названия оси X
                )
            ),
            yaxis=dict(
                automargin=True,
                title=dict(
                    standoff=5  # Установка отступа для названия оси Y
                )
            ),

            xaxis_title_font_size=9,
            yaxis_title_font_size=9,
            font=dict(size=7),
            legend=dict(
                orientation="v",         # Горизонтальная ориентация
                yanchor="top",        # Выравнивание по нижнему краю
                y=0.98,                  # Расположение немного выше границы графика
                xanchor="right",        # Центрирование по горизонтали
                x=1,                    # Горизонтальная позиция по центру
                font=dict(
                    size=9         # Размер текста в легенде
                )
            )
        )
        fig.update_traces(
            # Отображение только комментария
            hovertemplate='<b>%{customdata[0]}</b><extra></extra>',
            line=dict(width=2)
        )

        graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn', config={
            'displayModeBar': True,        # Отображение панели управления
            'displaylogo': False,
            'editable': False,
            'responsive': True,
            'staticPlot': True,
        }
        )

    except Exception as err:
        inf(f"Ошибка при формировании rozklad_cours>>>>>>>>>>>>{err} ")
        return "<p>Brak</p>", 0, 0, "<p>Brak</p>"

    return html_table, rozklad_curs.shape[0], bud_without_dry["meter"].sum(), graph_html


if __name__ == "__main__":
    df_orders = get_list_construction_place()
    # print(rozklad_curs()[0])
