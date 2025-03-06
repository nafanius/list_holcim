from pandas import Series, DataFrame
import plotly.express as px
import pandas as pd
import numpy as np
from pprint import pprint
import logging
from data_sql import get_newest_list_beton_or_lista
import data_sql
from order import Order
from driver import Driver
import re
import altair as alt
import io
import threading
from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy import text as text_sql_request
from settings import Settings



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
df_for_driver_glob = DataFrame()

def get_list_construction_place(date_order, wenzel):
    """возвращает список словарей словарь заказов на основание класса order его 
    переменные которые достаёт из базы данных на дату

    Args:
        date_order (str, optional): _description_. Defaults to "07.02.2025".
    """
    orders = {}
    count = 1
    df_bud = []

    for item in get_newest_list_beton_or_lista("beton", date_order, wenzel[0]):
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
            "wenz": bud.wenz,
            "it_is_zaprawa": bud.it_is_zaprawa,
            "it_is_concret": bud.it_is_concret,
            "list_of_courses": bud.list_of_courses,
            "pompa_dzwig": bud.pompa_dzwig,
            "reszta": bud.reszta,
            "date_order": bud.date_order,
        })

    return df_bud

def get_list_construction_driver(date_order, wenzel):
    """возвращает список словарей словарь заказов на основание класса order его 
    переменные которые достаёт из базы данных на дату

    Args:
        date_order (str, optional): _description_. Defaults to "07.02.2025".
    """
    drivers = {}
    count = 1
    df_driver = []

    for item in get_newest_list_beton_or_lista("lista", date_order, wenzel[0]):
        drivers[f"{count}dri"] = Driver(date_order, *item)
        count += 1

    for key_bud in drivers.keys():
        dri = drivers[key_bud]

        df_driver.append({
            "time": dri.time_in_list,
            "person": dri.person,
        })

    return df_driver


def rozklad_curs(wenzel, date_of_request="18.02.2025"):

    df_orders = get_list_construction_place(date_of_request, wenzel=wenzel)

    try:
        global count_graph
        global df_for_driver_glob
        bud = DataFrame(df_orders)

        # УБЕРАЕМ СУХОЙ БЕТОН
        bud_without_dry = bud[bud["it_is_zaprawa"] | bud["it_is_concret"]]

        bud_without_dry = bud_without_dry.copy()
        bud_without_dry.loc[:,"namber_cours"] = bud_without_dry.loc[:,"list_of_courses"].apply(
            lambda x: list(range(1, len(x) + 1))).values

        # оставляем название курсы метров и курсы выселки
        rozklad_curs = bud_without_dry[['list_of_loads', 'list_of_courses', 'name', 'reszta', 'wenz', 'it_is_zaprawa', 'pompa_dzwig', 'namber_cours']].explode(
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
                                'budowa', 'res', 'wenz', 'mat', 'p/d', 'k']
        rozklad_curs = rozklad_curs.reindex(
            ['id', 'time', 'm3', 'k', 'budowa', 'res', 'wenz' ,'mat', 'p/d'], axis=1)


        rozklad_curs['m3'] = rozklad_curs['m3'].astype(float).round(1)
        rozklad_curs['res'] = rozklad_curs['res'].astype(float).round(1)
        rozklad_curs.sort_values("time", inplace=True)
        rozklad_curs.reset_index(drop=True, inplace=True)
        rozklad_curs.index=rozklad_curs.index+1

        today = datetime.today()
        today_string = today.strftime('%d.%m.%Y')
        inspector = inspect(data_sql.engine)

        if today.weekday() == 6:
            delete_query = text_sql_request("DELETE FROM actual_after")

            with db_lock:  
                with data_sql.engine.connect() as connection:
                    connection.execute(delete_query)
                    connection.commit()  


        if date_of_request == today_string and wenzel[0] == "zawod":

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
                df_corrects['m3'] = df_corrects['m3'].astype(float).round(1)
                df_corrects['k'] = df_corrects['k'].astype(int)
                df_corrects['budowa'] = df_corrects['budowa'].astype(str)
                df_corrects['res'] = df_corrects['res'].astype(float)
                df_corrects['wenz'] = df_corrects['wenz'].astype(str)
                df_corrects['mat'] = df_corrects['mat'].astype(str)
                df_corrects['p/d'] = df_corrects['p/d'].astype(str)

                rozklad_curs['id'] = rozklad_curs['id'].astype(int)
                rozklad_curs['k'] = rozklad_curs['k'].astype(int)
                rozklad_curs['m3'] = rozklad_curs['m3'].astype(float).round(1)
                rozklad_curs['budowa'] = rozklad_curs['budowa'].astype(str)
                rozklad_curs['wenz'] = rozklad_curs['wenz'].astype(str)
                rozklad_curs['mat'] = rozklad_curs['mat'].astype(str)
                rozklad_curs['p/d'] = rozklad_curs['p/d'].astype(str)
                
                
                inf("corrects befor")
                inf(df_corrects)
                
               
                merged_df = df_corrects.merge(rozklad_curs[['m3', 'k', 'budowa', 'res', 'wenz', 'mat', 'p/d', 'time']],
                              on=['m3', 'k', 'budowa', 'res', 'wenz', 'mat', 'p/d'],
                              how='inner',
                              suffixes=('', '_from_rosklad'))
                

                merged_df.drop_duplicates(subset=['m3', 'k', 'budowa', 'res', 'wenz', 'mat', 'p/d'], keep='last', inplace=True)


                merged_df.reset_index(drop=True, inplace=True)              
                inf("It's merge df")
                inf(merged_df)

                
                df_corrects.reset_index(drop=True, inplace=True)
                df_corrects.update(merged_df[['time_from_rosklad']].rename(columns={'time_from_rosklad': 'time'}))
                
                # df_corrects.loc[:,'time'] = rozklad_curs.merge(df_corrects[['k','budowa','res','mat','p/d']], on=['k','budowa','res','mat','p/d'], how='inner')['time'].values  

                df_corrects[["time", "new_time"]] = df_corrects[["time", "new_time"]].apply(pd.to_datetime)
                
                
                inf("corrects after")
                inf(df_corrects)

                if not df_corrects.empty:
                    df_corrects['delta'] = df_corrects['new_time'] - df_corrects['time']
                    df_corrects['delete'] = df_corrects['new_time'].dt.time == pd.to_datetime('00:00:00').time()


                with db_lock:
                    df_corrects[['index','id','time','m3','k','budowa','res', 'wenz', 'mat','p/d','new_time','user']].to_sql('corrects', con=data_sql.engine, if_exists='replace', index=False)

                rozklad_curs["delete"] = False

                for _, row in df_corrects.iterrows():
                    rozklad_curs.loc[(rozklad_curs['id'] == row['id'])&(rozklad_curs['budowa'] == row['budowa']), 'time'] += row['delta']
                    rozklad_curs.loc[(rozklad_curs['id'] == row['id'])&(rozklad_curs['budowa'] == row['budowa']), 'delete'] = row['delete']

                rozklad_curs = rozklad_curs[rozklad_curs['delete'] == False].reset_index(drop=True)
                rozklad_curs.drop(columns='delete', inplace=True)

                rozklad_curs.sort_values("time", inplace=True)
                rozklad_curs.reset_index(drop=True, inplace=True)
                rozklad_curs.index=rozklad_curs.index+1

            with db_lock:
                rozklad_curs.to_sql(
                    'actual_after', con=data_sql.engine, if_exists='replace', index=True)
  
        # for marking targets dowload
        target_time = pd.Timestamp.now()
        # target_time = target_time - pd.Timedelta(hours=9) # для смещения времени
        end_time = target_time + pd.Timedelta(minutes=40)

        graph = rozklad_curs.copy()
        df_for_driver_glob = rozklad_curs.copy()

        rozklad_curs['target'] = (rozklad_curs['time'] >= target_time) & (rozklad_curs['time'] <= end_time)

        
        rozklad_curs['time'] = rozklad_curs['time'].apply(
            lambda x: x.strftime('%H:%M'))
        
        
        rozklad_curs.rename(columns ={'wenz':'w'}, inplace=True)
        
        rozklad_curs[['time', 'm3', 'k', 'budowa', 'res', 'w', 'p/d']] = rozklad_curs[
            ['time', 'm3', 'k', 'budowa', 'res', 'w', 'p/d']].astype(str)
        
        rozklad_curs.loc[rozklad_curs['target'] == True, ['time', 'm3', 'k', 'budowa', 'res', 'w', 'p/d']] = (
            rozklad_curs.loc[rozklad_curs['target'] == True,['time', 'm3', 'k', 'budowa', 'res', 'w', 'p/d']]
            .map(lambda x: f'<span style="font-weight: bold; color:rgb(226, 124, 0);">{str(x)}</span>'))

        html_table = rozklad_curs[['time', 'm3', 'k', 'budowa', 'res', 'w', 'p/d']
                                  ].to_html(index=True,
                                            table_id="rozklad_curs",
                                            classes='rozklad_curs_tab',
                                            border=0,
                                            justify='center',
                                            escape=False )


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


def forecast_driver(wenzel, date_of_request="18.02.2025"):
    try:
        global df_for_driver_glob
        df_for_driver = df_for_driver_glob[["time","m3","mat","p/d"]]


        df_for_driver = df_for_driver.copy()
        df_for_driver['m3'] = df_for_driver['m3'].astype(float)

        def get_end_time(row):
            additional_hour = pd.Timedelta(hours=1)
            if row['p/d'] == 'p':
                time_in_minutes = pd.to_timedelta(row['m3']*3, unit='m')
            else:
                time_in_minutes = pd.to_timedelta(row['m3']*8, unit='m')
            return row['time'] + time_in_minutes + additional_hour
        
        df_for_driver.loc[:,'end_time'] = df_for_driver.apply(get_end_time, axis=1)

        formatted_date_start = pd.to_datetime(date_of_request, format='%d.%m.%Y').strftime('%Y-%m-%d') + ' 04:00:00'
        formatted_date_finish = pd.to_datetime(date_of_request, format='%d.%m.%Y').strftime('%Y-%m-%d') + ' 23:00:00'

        time_index = pd.date_range(start=formatted_date_start, end=formatted_date_finish, freq='min')

        df_full_day =  pd.DataFrame(index=time_index)


        for i in range(1,len(df_for_driver)+1):
            mask = (df_full_day.index >= df_for_driver.loc[i, 'time']) & (df_full_day.index <= df_for_driver.loc[i, 'end_time'])
            df_full_day.loc[mask, i] = df_for_driver.loc[i, 'mat']
        
        df_full_day = df_full_day.fillna(0)

        df_driver_list = DataFrame(get_list_construction_driver(date_of_request, wenzel=wenzel))

        if df_driver_list.empty:
            driver_dict = {}
            free_exict_list =  [f'Kierowca_{i}' for i in range(1, wenzel[2])]
        else:
            date_as_datetime = pd.to_datetime(date_of_request, format='%d.%m.%Y')
            df_driver_list.loc[:,'time'] = df_driver_list.loc[:,'time'].apply(lambda t: datetime.combine(date_as_datetime.date(), t))
            driver_dict = df_driver_list.set_index('person')['time'].to_dict()
            free_exict_list = []



        df=df_full_day.copy()

        # executor_availability = {executor str: timestep d.Timedelta, ...}
        executor_availability = driver_dict
        # executor_availability = {}
        # Добавление столбцов для исполнителей
        df['Executors'] = None
        df['Free Executors'] = None
        df['Missing Executors'] = None

        # Отслеживание свободных исполнителей
        free_executors = free_exict_list
        # free_executors = list(df_driver_list['person'])

        # Текущие назначения исполнителей к заказам в виде словаря {order: (executor, order)}
        current_assignments = {}

        # Словарь для отслеживания периодов работы BRAK исполнителей
        brak_intervals = {}

        # Счетчик для недостатка исполнителей
        brak_counter = 1

        used_executors=[]
        df['First'] = ''

        # Для каждого временного шага
        for current_time in df.index:
            start_executers = []
            # Обновляем список доступных исполнителей, учитывая начальное время готовности
            for executor, available_time in executor_availability.items():
                if available_time <= current_time and executor not in free_executors:
                    if all(executor != assigned_exec for assigned_exec, _ in current_assignments.values()):
                            start_executers.append(executor)

                
            # Сначала освобождаем исполнителей от завершенных заданий
            completed_orders = [order for order, (executor, _) in current_assignments.items() if df[order].loc[current_time] == 0]
            for order in completed_orders:
                free_executor, _ = current_assignments.pop(order)
                if not free_executor.startswith('BRAK_KIEROWCA'):
                    if df[order].shift(1).loc[current_time] == 'z':
                        free_executors.insert(0, free_executor)
                        while free_executor in used_executors:
                            used_executors.remove(free_executor)
                    else:
                        free_executors.append(free_executor)
                else:
                    # Заканчиваем интервал работы текущего BRAK исполнителя
                    brak_intervals[free_executor]['end'] = current_time

            # сортировка исполнителей 
            inserted = False

            if free_executors:
                for i, execu in enumerate(free_executors):
                    if execu in used_executors:
                        free_executors = free_executors[:i]+ start_executers + free_executors[i:]
                        inserted = True
                        break
                if not inserted:
                    free_executors = free_executors + start_executers
            else:             
                free_executors = start_executers + free_executors        
            
            # Обрабатываем существующие заказы с исполнителями BRAKx
            for order, (executor, assigned_order) in current_assignments.items():
                if executor.startswith('BRAK_KIEROWCA') and free_executors:
                    new_executor = free_executors.pop(0)
                    current_assignments[order] = (new_executor, assigned_order)
                    df.at[current_time, 'First'] = new_executor + f"::{str(df.at[current_time, 'First'])}"
                    # Заканчиваем интервал работы текущего BRAK исполнителя
                    brak_intervals[executor]['end'] = current_time
                    brak_intervals[executor]['new driver'] = new_executor
            
            # Назначение исполнителей на начинающиеся заказы
            missing_executors = []
            for order in df.columns[:-4]:  # исключаем столбцы 'Executors', 'Free Executors' и 'Missing Executors'
                if df[order].loc[current_time] != 0 and order not in current_assignments:
                    if free_executors:
                        current_executor = free_executors.pop(0)
                    else:
                        # Если нет свободных исполнителей, создаем нового с именем BRAKx
                        current_executor = f'BRAK_KIEROWCA{brak_counter}'
                        brak_counter += 1
                        missing_executors.append((current_executor, order))
                        # Начинаем интервал работы нового BRAK_KEROWCA исполнителя
                        brak_intervals[current_executor] = {'start': current_time, 'end': None}
                        brak_intervals[current_executor]['order'] = order

                    if current_executor not in used_executors:
                        df.at[current_time, 'First'] = current_executor + f"::{str(df.at[current_time, 'First'])}"
                    used_executors.append(current_executor)
                    
                    current_assignments[order] = (current_executor, order)

            # Обновляем недостающих исполнителей в столбце Missing Executors
            missing_executors = [
                (executor, order) for order, (executor, _) in current_assignments.items()
                if executor.startswith('BRAK_KIEROWCA')
            ]
            
            # Запись исполнителей и выполняемых заказов в формате (Executor, Order)
            # executor_assignments = ', '.join(f"({executor}, {assigned_order})" for assigned_order, (executor, order) in current_assignments.items())
            str_current_assignment = str([(executor, assigned_order) for assigned_order, (executor, order) in current_assignments.items()])
            df.at[current_time, 'Executors'] = str_current_assignment

            # Запись списка свободных исполнителей
            str_free_executors = str(free_executors)
            df.at[current_time, 'Free Executors'] = str_free_executors
            
            # Запись списка недостающих исполнителей в новый столбец
            # missing_assignments = ', '.join(f"({executor}, {assigned_order})" for executor, assigned_order in missing_executors)
            missing_executors = str(missing_executors)
            df.at[current_time, 'Missing Executors'] = missing_executors

        # Завершаем все интервалы, где end остался None
        for brak_key, interval in brak_intervals.items():
            if interval['end'] is None:
                brak_intervals[brak_key]['end'] = df.index[-1]


        df.replace('[]',np.nan, inplace=True)
        df.replace('',np.nan, inplace=True)

        # формируем df старт работы для водителей
        list_starts = df["First"][df["First"].notna()]
        list_starts = list_starts.str.split("::")
        list_starts = list_starts.explode()
        list_starts.replace('',np.nan, inplace=True)
        list_starts = list_starts.dropna()
        list_starts= list_starts.reset_index()
        list_starts.rename(columns={'index':'time', 'First':'person'}, inplace=True)


        # формируем список курсов у водителя
        def str_to_list(s):
            return eval(s)
        
        df_executors =  df['Executors'].dropna()

        df_executors  = df_executors.apply(str_to_list)
        expanded_rows = df_executors.explode()
        expanded_rows = expanded_rows.drop_duplicates()
        expanded_df = pd.DataFrame(expanded_rows.tolist(), columns=['person', 'N% kursów'])
        expanded_df_rezult = expanded_df.groupby('person')['N% kursów'].apply(list).reset_index()

        result_df_end = pd.merge(list_starts, expanded_df_rezult, on='person', how='left')
        result_df_end = result_df_end.drop_duplicates(subset='person')
        result_df_end['N% kursów_first'] = result_df_end["N% kursów"].apply(lambda x: x[0])
        result_df_end.sort_values(by=["time", "N% kursów_first"], inplace=True)
        result_df_end.drop(columns='N% kursów_first', inplace=True)
        result_df_end.reset_index(drop=True, inplace=True)
        result_df_end.index=result_df_end.index+1
        result_df_end['time'] = result_df_end['time'].apply(lambda x: x.strftime('%H:%M'))
        result_df_end.rename({'person':'Kierowca','N% kursów':'kursy'}, axis=1, inplace=True)

        result_df_end['Kierowca'] = result_df_end['Kierowca'].apply(lambda x: f'<span style="font-weight: bold; color:rgb(255, 0, 0);">{str(x)}</span>' if x.startswith('BRAK_KIEROWCA') else x)

        html_table_kerowca = result_df_end.to_html(index=True,table_id="rozklad_kierowca",classes='rozklad_kierowca_tab', border=0, justify='center', escape=False)

        # brack kierowców
        html_table_brak = ''
        if brak_intervals:
            df_brak = DataFrame(brak_intervals)
            df_brak = df_brak.T
            df_brak["oczekiwanie"] = df_brak["end"] - df_brak["start"]
            df_brak.rename({'new driver':'dostępny kierowca','order':'kurs'}, axis=1, inplace=True)
            df_brak['start'] = pd.to_datetime(df_brak['start'])
            df_brak['end'] = pd.to_datetime(df_brak['end'])
            df_brak[['start','end']] = df_brak[['start','end']].apply(lambda x: x.dt.strftime('%H:%M'))
            
            def format_timedelta(td):
                """formater time_delta to str"""
                td = pd.to_timedelta(td)
                total_seconds = int(td.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                return f'{hours:02}:{minutes:02}'
            
            df_brak.loc[:,'oczekiwanie'] = df_brak.loc[:,'oczekiwanie'].apply(format_timedelta)
            df_brak = df_brak[['kurs', 'start', 'end', 'oczekiwanie', 'dostępny kierowca']]
            new_index  = [f'BRAK KIER_{i}' for i in range(1, len(df_brak) + 1)]
            df_brak.index = pd.Index(new_index)

            html_table_brak = df_brak.to_html(index=True,table_id="brak_kerowca",classes='rozklad_kerowca_brak', border=0, justify='center', escape=False)
        
        
    except Exception as err:
        inf(f"Ошибка при формировании forecast_driver>>>>>>>>>>>>{err} ")
        return "<p>Brak</p>", "<p>Brak</p>"
    
                    
    return  html_table_kerowca, html_table_brak


if __name__ == "__main__":
    date_of_request = '07.03.2025'
    df_orders = get_list_construction_place(date_of_request, Settings.wenzels[0])
    df_driver  = get_list_construction_driver(date_of_request, Settings.wenzels[0])
    # print(rozklad_curs()[0])
    # print(rozklad_curs(Settings.wenzels[0], date_of_request))
    # print("*"*10)
    # print(forecast_driver(Settings.wenzels[0], date_of_request))

