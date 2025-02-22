from pandas import Series, DataFrame
import plotly.express as px
import pandas as pd
import numpy as np
from pprint import pprint
import logging
from data_sql import get_newest_list_beton_or_lista
import data_sql
from order import Order
import re
import altair as alt
import io
import threading
from datetime import datetime
from sqlalchemy import inspect



db_lock = threading.Lock()

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
        })

    return df_bud


def rozklad_curs(date_of_request="18.02.2025"):

    df_orders = get_list_construction_place(date_of_request)

    try:
        global count_graph
        bud = DataFrame(df_orders)

        # УБЕРАЕМ СУХОЙ БЕТОН
        bud_without_dry = bud[bud["it_is_zaprawa"] | bud["it_is_concret"]]

        bud_without_dry = bud_without_dry.copy()
        bud_without_dry.loc[:,"namber_cours"] = bud_without_dry.loc[:,"list_of_courses"].apply(
            lambda x: list(range(1, len(x) + 1))).values

        # оставляем название курсы метров и курсы выселки
        rozklad_curs = bud_without_dry[['list_of_loads', 'list_of_courses', 'name', 'reszta', 'it_is_zaprawa', 'pompa_dzwig', 'namber_cours']].explode(
            ['list_of_loads', 'list_of_courses', 'reszta', 'namber_cours'])

        rozklad_curs["it_is_zaprawa"] = rozklad_curs["it_is_zaprawa"].replace(
            {True: 'z', False: 'b'})
        rozklad_curs["pompa_dzwig"] = rozklad_curs["pompa_dzwig"].replace(
            {True: 'p', False: 'd'})

        # todo тут встовляем проверку есть ли изменения которые прислали с бота
        # with db_lock:
        #     df_changes = pd.read_sql_table('changes', con=data_sql.engine)

        # graph = rozklad_curs

        rozklad_curs.sort_values("list_of_loads", inplace=True)

        rozklad_curs = rozklad_curs.reset_index()
        rozklad_curs.index = rozklad_curs.index+1

        rozklad_curs.columns = ['id', 'time', 'm3',
                                'budowa', 'res', 'mat', 'p/d', 'k']
        rozklad_curs = rozklad_curs.reindex(
            ['id', 'time', 'm3', 'k', 'budowa', 'res', 'mat', 'p/d'], axis=1)


        today = datetime.today()
        today_string = today.strftime('%d.%m.%Y')
        inspector = inspect(data_sql.engine)

        if date_of_request == today_string:

            with db_lock:
                rozklad_curs.to_sql(
                    'actual', con=data_sql.engine, if_exists='replace', index=True)
            
            if 'corrects' in inspector.get_table_names():
                query = 'SELECT * FROM corrects;'
                with db_lock:
                    df_corrects = pd.read_sql_query(query, con=data_sql.engine)
        
                                
                df_corrects['new_time'] = pd.to_datetime(df_corrects['new_time'])
                df_corrects = df_corrects[df_corrects['new_time'].dt.date == today.date()]
                df_corrects.drop_duplicates(subset=['id', 'budowa'], keep='last', inplace=True)
                
                
                df_corrects['id'] = df_corrects['id'].astype(int)
                df_corrects['k'] = df_corrects['k'].astype(int)
                df_corrects['budowa'] = df_corrects['budowa'].astype(str)
                df_corrects['res'] = df_corrects['res'].astype(float)
                df_corrects['mat'] = df_corrects['mat'].astype(str)
                df_corrects['p/d'] = df_corrects['p/d'].astype(str)

                rozklad_curs['k'] = rozklad_curs['k'].astype(int)
                rozklad_curs['budowa'] = rozklad_curs['budowa'].astype(str)
                rozklad_curs['res'] = rozklad_curs['res'].astype(float)
                rozklad_curs['mat'] = rozklad_curs['mat'].astype(str)
                rozklad_curs['p/d'] = rozklad_curs['p/d'].astype(str)
                
    

                
                inf("corrects befor")
                inf(df_corrects)
                
                
               
                merged_df = df_corrects.merge(rozklad_curs[['k', 'budowa', 'res', 'mat', 'p/d', 'time']],
                              on=['k', 'budowa', 'res', 'mat', 'p/d'],
                              how='inner',
                              suffixes=('', '_from_rosklad'))
                              
                inf("It's merge df")
                inf(merged_df)
                
                df_corrects.update(merged_df[['time_from_rosklad']].rename(columns={'time_from_rosklad': 'time'}))
                
                
                # df_corrects.loc[:,'time'] = rozklad_curs.merge(df_corrects[['k','budowa','res','mat','p/d']], on=['k','budowa','res','mat','p/d'], how='inner')['time'].values  

                df_corrects[["time", "new_time"]] = df_corrects[["time", "new_time"]].apply(pd.to_datetime)
                
                
                inf("corrects after")
                inf(df_corrects)

                if not df_corrects.empty:
                    df_corrects['delta'] = df_corrects['new_time'] - df_corrects['time']

                
                with db_lock:
                    df_corrects[['index','id','time','m3','k','budowa','res','mat','p/d','new_time','user']].to_sql('corrects', con=data_sql.engine, if_exists='replace', index=False)

                for _, row in df_corrects.iterrows():
                    rozklad_curs.loc[(rozklad_curs['id'] == row['id'])&(rozklad_curs['budowa'] == row['budowa']), 'time'] += row['delta']


                rozklad_curs.sort_values("time", inplace=True)
                rozklad_curs.reset_index(drop=True, inplace=True)
                rozklad_curs.index=rozklad_curs.index+1

            with db_lock:
                rozklad_curs.to_sql(
                    'actual_after', con=data_sql.engine, if_exists='replace', index=True)

        graph = rozklad_curs.copy()

        rozklad_curs['time'] = rozklad_curs['time'].dt.time
        rozklad_curs['time'] = rozklad_curs['time'].apply(
            lambda x: x.strftime('%H:%M'))

        html_table = rozklad_curs[['time', 'm3', 'k', 'budowa', 'res', 'mat', 'p/d']
                                  ].to_html(index=True, table_id="rozklad_curs", classes='rozklad_curs_tab', border=0, justify='center')


        graph.set_index('time', inplace=True)



        nadal_reszta = pd.to_numeric(graph['res']).resample(
            '30min').quantile(0.90).rolling(window=2).mean()

        graph_corect = graph.resample('30min').sum()
        graph_corect['m3'] = pd.to_numeric(graph_corect['m3']).rolling(window=2).mean()
        graph_corect.loc[:, 'm3'] = graph_corect.loc[:,'m3'].fillna(0.0)

        graph_corect = graph_corect[['m3', 'res', 'budowa']]
        graph_corect.columns = ['intensywność m/g',
                                'nadal trzeba wysłać', 'budowa']

        graph_corect['nadal trzeba wysłać'] = pd.to_numeric(
            graph_corect['nadal trzeba wysłać'])

        graph_corect.loc[:, 'nadal trzeba wysłać'] = pd.to_numeric(
            nadal_reszta.fillna(0.0))

        graph_corect = graph_corect.reset_index()
        graph_corect = graph_corect.melt(
            'time', var_name='series', value_name='Metry')

        chart = alt.Chart(graph_corect, background='rgba(255, 255, 255, 0.5)').mark_line().encode(
            x=alt.X('time:T', axis=alt.Axis(
                title='time', format='%H:%M')),
            y=alt.Y('Metry:Q', axis=alt.Axis(title='metrs')),
            color=alt.Color('series:N',
                            legend=alt.Legend(
                                title="INTENSYWNOŚĆ PRACY",                # Название легенды
                                titleFontSize=14,             # Размер шрифта заголовка
                                labelFontSize=12,             # Размер шрифта меток
                                orient='top',               # Положение легенды
                                padding=1                   # Внутренний отступ
                            ))
        ).transform_filter(
            alt.FieldOneOfPredicate(field='series', oneOf=[
                'intensywność m/g', 'nadal trzeba wysłać'])
        ).properties(
            width='container',
            height=150
        ).configure_view(
            strokeWidth=0

        )

        html_buffer = io.StringIO()

        chart.save(html_buffer, format='html', embed_options={
                   'actions': False}, fullhtml=False,  output_div=f'chart{count_graph}')
        count_graph += 1
        graph_html = html_buffer.getvalue()
        html_buffer.close()

        counts = graph['p/d'].value_counts().reset_index()

        counts['percentage'] = counts['count'] / counts['count'].sum()
        counts["p/d"] = counts["p/d"].replace(
            {'d': 'Dzwig', 'p': 'Pompa'})

        chart = alt.Chart(counts, background='rgba(255, 255, 255, 0.5)').mark_arc().encode(
            theta=alt.Theta(field='percentage', type='quantitative'),
            color=alt.Color(field='p/d',
                            type='nominal',
                            legend=alt.Legend(title=''))

        ).encode(
            # Задаем метку с названием категории и процентом
            text=alt.Text('label:N')
        ).properties(
            width='container',
            height=100,
            title='stosunek dzwig/pompa'
        )

        html_buffer = io.StringIO()
        chart.save(html_buffer, format='html', embed_options={
                   'actions': False}, fullhtml=False,  output_div=f'chart{count_graph}')
        count_graph += 1
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
