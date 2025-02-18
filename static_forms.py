from data_sql import get_newest_list_beton_or_lista
import data_sql
from order import Order
import re
import altair as alt
import io
import threading
from datetime import datetime



db_lock = threading.Lock()

import logging
from pprint import pprint
import numpy as np
import pandas as pd
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


count_graph = 1

def get_list_construction_place(date_order):
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


def rozklad_curs(date_of_request="18.02.2025"):

    df_orders = get_list_construction_place(date_of_request)

    try:
        global count_graph
        bud = DataFrame(df_orders)

        # УБЕРАЕМ СУХОЙ БЕТОН
        bud_without_dry = bud[bud["it_is_zaprawa"] | bud["it_is_concret"]]

        bud_without_dry["namber_cours"] = bud_without_dry["list_of_courses"].apply(lambda x: list(range(1, len(x) + 1)))


        # оставляем название курсы метров и курсы выселки
        rozklad_curs = bud_without_dry[['list_of_loads', 'list_of_courses', 'name', 'reszta', 'it_is_zaprawa', 'pompa_dzwig', 'namber_cours']].explode(
            ['list_of_loads', 'list_of_courses', 'reszta', 'namber_cours'])

        rozklad_curs["list_of_loads"] = rozklad_curs["list_of_loads"].dt.time
        rozklad_curs['list_of_loads'] = rozklad_curs['list_of_loads'].apply(
            lambda x: x.strftime('%H:%M'))

        rozklad_curs["it_is_zaprawa"] = rozklad_curs["it_is_zaprawa"].replace(
            {True: 'z', False: 'b'})
        rozklad_curs["pompa_dzwig"] = rozklad_curs["pompa_dzwig"].replace(
            {True: 'p', False: 'd'})
        

        # todo тут встовляем проверку есть ли изменения которые прислали с бота
        # with db_lock:
        #     df_changes = pd.read_sql_table('changes', con=data_sql.engine)

        
        rozklad_curs.sort_values("list_of_loads", inplace=True)

        graph = rozklad_curs

        rozklad_curs = rozklad_curs.reset_index(drop=True)
        rozklad_curs.index = rozklad_curs.index+1

        
        rozklad_curs.columns = ['time', 'm3', 'budowa', 'res', 'mat', 'p/d', 'c']
        rozklad_curs = rozklad_curs.reindex(['time', 'm3', 'c','budowa', 'res', 'mat', 'p/d' ], axis=1)


        today = datetime.today()
        today = today.strftime('%d.%m.%Y')

        if date_of_request == today:
            with db_lock:
                rozklad_curs.to_sql('actual', con=data_sql.engine, if_exists='replace', index=True)
        
        html_table = rozklad_curs.to_html(
            index=True, table_id="rozklad_curs", classes='rozklad_curs_tab', border=0, justify='center')

        current_date = datetime.strptime(date_of_request, '%d.%m.%Y').date()
        graph['list_of_loads'] =  pd.to_datetime(graph['list_of_loads'].apply(lambda x: f"{current_date} {x}"))

        graph.set_index('list_of_loads', inplace=True)


        # todo разкоментировать в случае применнения среднего взвешаного
        # def weighted_mean(values):
        #     '''  Функция для вычисления взвешенного среднего'''
        #     weights = np.arange(1, len(values) + 1)  # Пример: веса нарастают
        #     return np.average(values, weights=weights)

        # nadal_reszta = pd.to_numeric(graph['reszta']).resample('30min').apply(weighted_mean)

        nadal_reszta = pd.to_numeric(graph['reszta']).resample('30min').quantile(0.90).rolling(window=2).mean()

        graph_corect = graph.resample('30min').sum()
        graph_corect['list_of_courses'] = pd.to_numeric(graph_corect['list_of_courses']).rolling(window=2).mean()
        graph_corect.loc[:,'list_of_courses'] = graph_corect.loc[:,'list_of_courses'].fillna(0.0)

        graph_corect = graph_corect[['list_of_courses', 'reszta', 'name']]
        graph_corect.columns = ['intensywność m/g',
                                'nadal trzeba wysłać', 'name']

        graph_corect['nadal trzeba wysłać'] =  pd.to_numeric(graph_corect['nadal trzeba wysłać'])
        


        graph_corect.loc[:,'nadal trzeba wysłać'] = pd.to_numeric(nadal_reszta.fillna(0.0))




        graph_corect = graph_corect.reset_index()
        graph_corect = graph_corect.melt('list_of_loads', var_name='series', value_name='Metry')

        chart =  alt.Chart(graph_corect, background='rgba(255, 255, 255, 0.5)').mark_line().encode(
            x= alt.X('list_of_loads:T',axis=alt.Axis(title='time', format='%H:%M')),
            y= alt.Y('Metry:Q', axis=alt.Axis(title='metrs')),
            color=alt.Color('series:N',
                            legend=alt.Legend(
                            title="INTENSYWNOŚĆ PRACY",                # Название легенды
                            titleFontSize=14,             # Размер шрифта заголовка
                            labelFontSize=12,             # Размер шрифта меток
                            orient='top',               # Положение легенды
                            padding=1                   # Внутренний отступ
                        ))
            ).transform_filter(
                alt.FieldOneOfPredicate(field='series', oneOf=['intensywność m/g', 'nadal trzeba wysłać'])
            ).properties(
                width='container',
                height= 150
            ).configure_view(
                strokeWidth=0

            )
 
        html_buffer = io.StringIO()

        chart.save(html_buffer, format='html', embed_options={'actions': False}, fullhtml=False,  output_div=f'chart{count_graph}')
        count_graph +=1
        graph_html = html_buffer.getvalue()
        html_buffer.close()

        counts = graph['pompa_dzwig'].value_counts().reset_index()

        counts['percentage'] = counts['count'] / counts['count'].sum()
        counts["pompa_dzwig"] = counts["pompa_dzwig"].replace({'d': 'Dzwig', 'p': 'Pompa'})

        chart = alt.Chart(counts, background='rgba(255, 255, 255, 0.5)').mark_arc().encode(
                    theta=alt.Theta(field='percentage', type='quantitative'),
                    color=alt.Color(field='pompa_dzwig',
                                    type='nominal',
                                    legend=alt.Legend(title=''))
                                    
                ).encode(
                    text=alt.Text('label:N')  # Задаем метку с названием категории и процентом
                ).properties(
                    width='container',
                    height=100,
                    title='stosunek dzwig/pompa'
                )

        html_buffer = io.StringIO()
        chart.save(html_buffer, format='html', embed_options={'actions': False}, fullhtml=False,  output_div=f'chart{count_graph}')
        count_graph +=1
        graph_html_pie = html_buffer.getvalue()
        html_buffer.close()




    except Exception as err:
        inf(f"Ошибка при формировании rozklad_cours>>>>>>>>>>>>{err} ")
        return "<p>Brak</p>", 0, 0, "<p>Brak</p>", "<p>Brak</p>"

    return html_table, rozklad_curs.shape[0], bud_without_dry["meter"].sum(), graph_html, graph_html_pie


if __name__ == "__main__":
    date_of_request = '17.02.2025'
    df_orders = get_list_construction_place(date_of_request)
    # print(rozklad_curs()[0])
