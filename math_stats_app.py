import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
with st.echo(code_location='below'):
    ### Подготавливаем данные
    df = pd.read_csv('results.csv')
    df.drop('Unnamed: 0', axis = 1, inplace = True)
    mean_res = df[['grade', 'year', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8']].groupby(['grade', 'year']).mean()
    problems = mean_res.melt(ignore_index = False).reset_index().rename(columns = {'variable' : 'problem', 'value' :'mean_score'}).sort_values(by = 'mean_score')
    results_data = df[['year', 'status', 'grade']].groupby(['year', 'status'], as_index = False).count().rename(columns = {'grade' : 'number of persons'})
    ### Пишем вводную информацию
    st.title('Анализ Всероссийской олимпиады школьников по математике')
    st.header('О проекте')
    st.write('''Всероссийская олимпиада школьников по математике, ВСОШ или просто всерос - главная олимпиада по математике в 
    России. Победители и призеры ВСОШ имеют право поступления в любой университет соответсвующего профиля без вступительных испытаний, а из
    лучших среди победителей ВСОШ (и других олимпиад) затем формируется команда на международную олимпиаду школьников по математике. Формат олимпиады не 
    менялся уже долгие годы - участникам предлагается решить 8 задач, по 4 в день, каждая из которых оценивается по 7-балльной шкале. В этом проекте,
    выполненном в 2022 году в рамках курса "Наука о данных" на совместном бакалавриате НИУ ВШЭ и РЭШ, я создал наглядную и интерактивную визуализацию статистики этой олимпиады.
    Надеюсь, вы получите удовольствие от просмотра, а может быть это даже вдохновит вас уделить больше своего внимания прекраснейшей из наук - математике.
             ''')
    st.header('Технические детали')
    st.write('Поскольку некоторые графики достаточно сложные, их загрузка может занять некоторое время. Пожалуйста, дождитесь пока в правом верхнем углу не пропадет надпись "Running". Рекомендуется выполнять просмотр с компьютера, а не с телефона.')
    st.header('Анализ по регионам')
    ### График отображения информации на карте
    st.subheader('Уровень участия регионов во Всероссийской олимпиаде школьников по годам')
    year = st.slider( "Выберите год" , 2009 , 2019, 2019)
    all_part = pd.DataFrame(df[df['year'] == year].groupby('region', as_index = False)['grade'].count()).rename(columns = {'grade' : 'participants'})
    with_diploma = pd.DataFrame(df[df['year'] == year].query("status in ['победитель', 'призер']").groupby('region', as_index = False)['grade'].count()).rename(columns = {'grade' : 'with_diploma'})
    winners = pd.DataFrame(df[df['year'] == year].query("status in ['победитель']").groupby('region', as_index = False)['grade'].count()).rename(columns = {'grade' : 'winners'})
    data_by_id = all_part.merge(with_diploma, on = 'region', how = 'left').merge(winners, on = 'region', how = 'left').fillna(0)
    data_by_id['participants'] = data_by_id['participants'].astype(int)
    data_by_id['with_diploma'] = data_by_id['with_diploma'].astype(int)
    data_by_id['winners'] = data_by_id['winners'].astype(int)
    dict_by_id = data_by_id.set_index('region').to_dict('index')
    dict_by_id.update({'0' : {'participants': 0, 'with_diploma': 0, 'winners': 0}})
    dict_by_id['г. Москва'] = dict_by_id['Москва']
    dict_by_id['г. Санкт-Петербург'] = dict_by_id['Санкт-Петербург']
    if 'Cевастополь' in dict_by_id.keys():
        dict_by_id['г. Севастополь'] = dict_by_id['Севастополь']
    all_regions = ['Республика Бурятия',
     'Карачаево-Черкесская Республика',
     'Сахалинская область',
     'Воронежская область',
     'Томская область',
     'Новосибирская область',
     'Ненецкий автономный округ',
     'Приморский край',
     'Ставропольский край',
     'Алтайский край',
     'г. Москва',
     'Республика Тыва',
     'Тамбовская область',
     'Свердловская область',
     'Ханты-Мансийский автономный округ - Югра',
     'Чукотский автономный округ',
     'Тюменская область',
     'Владимирская область',
     'Московская область',
     'Волгоградская область',
     'Оренбургская область',
     'Самарская область',
     'Астраханская область',
     'Республика Адыгея',
     'Республика Калмыкия',
     'Краснодарский край',
     'Ростовская область',
     'Мурманская область',
     'Псковская область',
     'г. Санкт-Петербург',
     'Республика Мордовия',
     'Кировская область',
     'Костромская область',
     'Тверская область',
     'Тульская область',
     'Калужская область',
     'Республика Марий Эл',
     'Смоленская область',
     'Ивановская область',
     'Республика Северная Осетия - Алания',
     'Брянская область',
     'Пензенская область',
     'Белгородская область',
     'Липецкая область',
     'Нижегородская область',
     'Курганская область',
     'Курская область',
     'Забайкальский край',
     'Республика Алтай',
     'Рязанская область',
     'Республика Дагестан',
     'Омская область',
     'Республика Коми',
     'Чеченская Республика',
     'Кабардино-Балкарская Республика',
     'Саратовская область',
     'Калининградская область',
     'Орловская область',
     'Республика Карелия',
     'Иркутская область',
     'Амурская область',
     'Еврейская автономная область',
     'Хабаровский край',
     'Кемеровская область',
     'Республика Хакасия',
     'Ярославская область',
     'Вологодская область',
     'Республика Ингушетия',
     'Челябинская область',
     'Республика Башкортостан',
     'Архангельская область',
     'Новгородская область',
     'Ленинградская область',
     'Пермский край',
     'Удмуртская Республика',
     'Республика Татарстан',
     'Ульяновская область',
     'Чувашская Республика',
     'Ямало-Ненецкий автономный округ',
     'Красноярский край',
     'Магаданская область',
     'Камчатский край',
     'Республика Саха (Якутия)',
     'г. Севастополь',
     'Республика Крым']
    for i in all_regions:
        if i not in dict_by_id.keys():
            dict_by_id[i] = {'participants': 0, 'with_diploma': 0, 'winners': 0}
    data_from_id = pd.DataFrame.from_dict(dict_by_id, orient = 'index').reset_index().rename(columns = {'index' : 'reg_name'})
    data_from_id['log_participants'] = np.log(data_from_id['participants'] + 1)

    ### INSPIRED BY https://altair-viz.github.io/altair-tutorial/notebooks/09-Geographic-plots.html
    url = "https://raw.githubusercontent.com/amdest/russia-map/main/Russia.topojson"
    source = alt.topo_feature(url, 'Russia')
    maps = alt.Chart(source).mark_geoshape(stroke='gray').encode(
            color = alt.Color('log_participants:Q', title = 'Уровень участия'),
            tooltip=[alt.Tooltip('properties.NL_NAME_1:N', title = 'Регион'), alt.Tooltip('participants:Q', title = 'Число участников'), alt.Tooltip('with_diploma:Q', title = 'Число победителей и призеров'), alt.Tooltip('winners:Q', title = 'Число победителей')],
        ).transform_lookup(
        lookup='properties.NL_NAME_1',
        from_=alt.LookupData(data_from_id, 'reg_name', ['participants', 'with_diploma', 'winners', 'log_participants']
    )).properties(
            title = 'Уровень участия регионов во Всероссийской олимпиаде школьников',
            width=900,
            height=500,
        ).project(
            type='orthographic', scale=500, rotate = [-70, -70, -30], center = [8, 20]
        )
    ### END
    data_from_id.drop(data_from_id[data_from_id['reg_name'] == 'Москва'].index, inplace = True)
    data_from_id.drop(data_from_id[data_from_id['reg_name'] == 'Санкт-Петербург'].index, inplace = True)
    data_from_id.drop(data_from_id[data_from_id['reg_name'] == 'Севастополь'].index, inplace = True)
    mean_data = pd.DataFrame(data_from_id.mean()).T
    mean_data['reg_name'] = 'В среднем по всем регионам'
    city_data = pd.concat([data_from_id[data_from_id['reg_name'] == 'г. Москва'], data_from_id[data_from_id['reg_name'] == 'г. Санкт-Петербург'], mean_data])
    chart_avg = alt.Chart(city_data).mark_bar().encode(x = alt.X('participants', title = 'Число участников'), y = alt.Y('reg_name', title = '', axis = alt.Axis(orient = 'right')), color = alt.Color('log_participants:Q', title = 'Уровень участия'),
                                                      tooltip=[alt.Tooltip('reg_name:N', title = 'Регион'), alt.Tooltip('participants:Q', title = 'Число участников'), alt.Tooltip('with_diploma:Q', title = 'Число победителей и призеров'), alt.Tooltip('winners:Q', title = 'Число победителей')]).properties(
            width=900,
            height=100
        )
    st.altair_chart(alt.vconcat(maps, chart_avg))
    st.write('Данный график позволяет наглядно сравнить по годам уровень участия регионов в заключительном этапе ВСОШ, который высчитывается здесь по формуле $\ln(1 + k)$, где $k$ - число участников от региона.')
    ### Анимация для сравнения числа победителей и призеров по регионам
    st.subheader('Динамика количества призеров и победителей по регионам')
    classes_ = st.multiselect('Классы: ', [9, 10, 11], default = [9, 10, 11], key = 52)
    selected_reg = st.selectbox('Подсветить дополнительно регион: ', sorted(df['region'].dropna().unique()), index = sorted(df['region'].dropna().unique()).index('Республика Татарстан'))
    if len(classes_) == 0:
        st.write('Пожалуйста, выберите хотя бы один класс.')
    else:
        by_reg_data_all = pd.DataFrame(df.query('grade in @classes_').groupby(['year', 'region']).count()[['grade']]).rename(columns = {'grade' : 'Всего участников'})
        by_reg_data_priz = pd.DataFrame(df.query('grade in @classes_ and status == "призер" ').groupby(['year', 'region']).count()[['grade']]).rename(columns = {'grade' : 'Призеры'})
        by_reg_data_win = pd.DataFrame(df.query('grade in @classes_ and status == "победитель" ').groupby(['year', 'region']).count()[['grade']]).rename(columns = {'grade' : 'Победители'})
        by_reg_all_data = by_reg_data_all.merge(by_reg_data_priz, how = 'left', left_index = True, right_index = True).merge(by_reg_data_win, how = 'left', left_index = True, right_index = True).fillna(0).reset_index()
        by_reg_all_data['Призеры'] = by_reg_all_data['Призеры'].astype(int)
        by_reg_all_data['Победители'] = by_reg_all_data['Победители'].astype(int)
        by_reg_all_data.rename(columns = {'year' : 'Год', 'region' : 'Регион'}, inplace = True)
        dictionary = {selected_reg : 'Выбранный регион', 'Москва' : 'Москва', 'Санкт-Петербург': 'Санкт-Петербург'}
        by_reg_all_data['Тип'] = by_reg_all_data['Регион'].map(dictionary)
        by_reg_all_data['Тип'].fillna('Регион', inplace = True)
        ### INSPIRED BY https://plotly.com/python/animations/
        scatter_graph = px.scatter(by_reg_all_data, x="Призеры", y="Победители", animation_frame="Год", animation_group="Регион",
                   size="Всего участников", color="Тип", hover_name="Регион",
                    size_max=55, range_x=[0,60], range_y=[0,10])
        st.plotly_chart(scatter_graph)
        ### END
    st.write('Этот график показывает динамику числа призеров и победителей от разных регионов по годам.  Размер точки соответствует общему числу участников от региона. График инетрактивный и вы можете увеличить любую область!')
    ### Stacked barplot для числа победителей, призеров и участников по годам
    st.subheader('Сравнение количества выданных дипломов по годам')
    results_data_sorted = results_data.sort_values('status', key = lambda x: x.apply(
        lambda y: {'победитель' : 4, 'призер' : 3, 'похвальная грамота' : 2, 'участник' : 1}[y]))
    if st.checkbox('Отобразить простую картинку', key = 4435):
        sub_data = results_data_sorted.groupby(['year', 'status'], as_index=False).sum()
        fig, ax = plt.subplots()
        sns.barplot(
            data=sub_data.query('status in ["победитель", "призер", "похвальная грамота", "участник"]').groupby(['year'],
                                                                                                                as_index=False).sum(),
            x='year', y='number of persons', color='red', ax=ax, ci=None)
        sns.barplot(data=sub_data.query('status in ["призер", "похвальная грамота", "участник"]').groupby(['year'],
                                                                                                          as_index=False).sum(),
                    x='year', y='number of persons', color='orange', ax=ax, ci=None)
        sns.barplot(
            data=sub_data.query('status in ["похвальная грамота", "участник"]').groupby(['year'], as_index=False).sum(),
            x='year', y='number of persons', color='yellow', ax=ax, ci=None)
        sns.barplot(data=sub_data.query('status in ["участник"]').groupby(['year'], as_index=False).sum(), x='year',
                    y='number of persons', color='green', ax=ax, ci=None)
        part = mpatches.Patch(color='green', label='участник')
        gram = mpatches.Patch(color='yellow', label='похвальная грамота')
        priz = mpatches.Patch(color='orange', label='призер')
        win = mpatches.Patch(color='red', label='победитель')
        plt.legend(handles=[part, gram, priz, win])
        ax.set_xlabel('Год')
        ax.set_ylabel('Количество человек')
        ax.set_title('Сравнение количества выданных дипломов по годам')
        st.pyplot(fig)
    else:
        graph = alt.Chart(results_data_sorted).mark_bar().encode(
            x = alt.X('year:O', title = 'Год'),
            y = alt.Y('sum(number of persons)', title = 'Количество человек'),
            color= alt.Color('status', sort = ['победитель', 'призер', 'похвальная грамота', 'участник'], title = 'Результат'),
            order = 'order:Q',
            tooltip = [alt.Tooltip("status:N", title='Результат'), alt.Tooltip("number of persons", title='Количество человек')]
        ).properties(
                title = 'Сравнение количества выданных дипломов по годам',
                width=900,
                height=500,
            )
        st.altair_chart(graph)
    ### Lineplot для сравнения выбранных регионов
    st.subheader('Сравнение 2 выбранных регионов')
    region1 = st.selectbox('Регион 1: ', sorted(df['region'].dropna().unique()), index = sorted(df['region'].dropna().unique()).index('Москва'))
    region2 = st.selectbox('Регион 2: ', sorted(df['region'].dropna().unique()), index = sorted(df['region'].dropna().unique()).index('Санкт-Петербург'))
    grades = st.multiselect('Классы: ', [9, 10, 11], default = [9, 10, 11])
    status = st.multiselect('Результат: ', df.status.unique(), default = df.status.unique())
    if len(grades) == 0 or len(status) == 0:
        st.write('Пожалуйста, выберите хотя бы один вариант')
    else:
        df_reg = df.query('region in [@region1, @region2] and grade in @grades and status in @status')[
            ['year', 'region', 'status']].groupby(['year', 'region'], as_index=False).count().rename(
            columns={'status': 'number of persons'})
        if st.checkbox('Отобразить простую картинку', key = 32523):
            fig, ax = plt.subplots()
            sns.lineplot(data=df_reg, x='year', y='number of persons', hue='region', ax = ax)
            ax.set_xlabel('Год заключительного этапа ВСОШ')
            ax.set_ylabel('Количество человек')
            ax.set_title('Сравнение результатов ВСОШ по математике по выбранным регионам')
            st.pyplot(fig)
        else:
            ### CODE FROM https://matthewkudija.com/blog/2018/06/22/altair-interactive/
            ### (Скопирован код, который отрисовывает  красивую линейнку рядом с указателем мыши)
            nearest1 = alt.selection(type='single', nearest=True, on='mouseover',
                                    fields=['year'], empty='none')

            line1 = alt.Chart().mark_line().encode(
                alt.X('year:O', axis=alt.Axis(title='Год заключительного этапа ВСОШ')),
                alt.Y('number of persons:Q', axis=alt.Axis(title='Количество человек')),
                alt.Color('region:N', title='Регион')
            )

            selectors1 = alt.Chart().mark_point().encode(
                x='year:O',
                opacity=alt.value(0),
            ).add_selection(
                nearest1
            )

            points1 = line1.mark_point().encode(
                opacity=alt.condition(nearest1, alt.value(1), alt.value(0))
            )

            text1 = line1.mark_text(align='left', dx=5, dy=-5).encode(
                text=alt.condition(nearest1, 'number of persons:Q', alt.value(' '))
            )

            rules1= alt.Chart().mark_rule(color='gray').encode(
                x='year:O',
            ).transform_filter(
                nearest1
            )
            graph1 = alt.layer(line1, selectors1, points1, rules1, text1,
                              data=df_reg,
                              width=900, height=450, title='Сравнение результатов ВСОШ по математике по выбранным регионам')
            # END FROM
            st.altair_chart(graph1)
    ### Таблица рейтинга школ
    st.subheader('Топ школ по результатам ВСОШ')
    statuses = st.multiselect('Результат: ', df.status.unique(), default = df.status.unique(), key = 123)
    year_ = st.slider( "Выберите год" , 2009 , 2019, 2019, key = 456)
    if len(statuses) > 0:
        best_schools = \
        df.query('status in @statuses and year == @year_').groupby(['region', 'school'], as_index=False).count()[
            ['region', 'school', 'grade']].sort_values('grade', ascending=False)
        top_5_grades = best_schools.reset_index().drop('index', axis=1).iloc[5]['grade']
        best_schools.rename(columns={'region': 'Регион', 'school': 'Школа', 'grade': 'Количество человек'}, inplace=True)
        st.table(best_schools[best_schools['Количество человек'] >= top_5_grades].reset_index().drop('index', axis = 1))
    else:
        st.write('Пожалуйста, выберите хотя бы одно.')
    st.header('Анализ по задачам')
    st.write('Будем оценивать сложность каждой задачи по среднему баллу участников за эту задачу.')
    ### Самая сложная и самая легкая задача. Формально, для их поиска использовался запрос ниже,
    ### но поскольку он нужен всего один раз для поиска, он закоментирован, чтобы не перегружать код.
    ### problems = mean_res.melt(ignore_index = False).reset_index().rename(columns = {'variable' : 'problem', 'value' :'mean_score'}).sort_values(by = 'mean_score')
    ### problems.head()
    ### problems.tail()
    st.subheader('Самая сложная задача')
    st.write('Неожиданно для меня, звание самой сложной задачи получила задача не для 11, а для 10 класса, которую предлагали участникам под номером 4 задачи в 2012 году. Тогда баллов за эту задачу не удалось получить никому, и средний балл по ней оказался равен 0. Отмечу, что это единственная такая задача в рассматриваемый период времени. Вы можете попробовать свои силы, попытавшись решить эту задачу ниже.')
    st.write(r'''
    Изначально на доске были написаны $n + 1$ одночленов 1, $x$, $x^2$, $x^3$ ... $x^n$. Договорившись заранее,
    $k$ мальчиков каждую минуту одновременно вычисляли сумму каких-то двух многочленов, написанных на доске, и результат
    дописывали на доску. Через $m$ минут на доске были написаны, среди прочих, многочлены $S_1 = 1+ x$, $S_2 = 
    1 + x + x^2$, $S_3 = 1+ x^2 + x^3$, ... $S_n = 1+ x + x^2 + x^3 + \dots + x^n$. Докажите, что $m\geq\frac{2n}{k+1}$.
    (А. Шаповалов)
    ''')
    if st.checkbox('Показать решение'):
        st.write(r'''
        Рассмотрим конечную ситуацию на доске. Если
        многочлен P появился как сумма многочленов Q и R, то проведём стрелки из P в Q и R. Далее, если из многочлена F ведут
        (ориентированный!) путь в G, будем говорить, что G участвует
        в F (в частности, сам F участвует в F ). Нетрудно видеть в этом
        случае, что все коэициенты многочлена F - G неотрицательны.
        Можно считать, что каждый многочлен на доске сумма
        различных степеней x; действительно, если какой-то коэициент многочлена не меньше 2, то и у всех, в которых он участвует, соответствующий коэффициент также будет не меньше 2.
        Значит, он не участвует в суммах вида $S_i$
        .
        Мы собираемся оценить общее количество многочленов на
        доске. Каждый из многочленов $S_1$, . . . , $S_n$ назовём финальным.
        Каждый из многочленов, участвующих в $S_n$ (то есть в сумме
        всех исходных одночленов), назовём существенным. Ясно, что
        есть n финальных многочленов.
        Покажем индукцией по p, что в многочлене с p ненулевыми
        коэффициентами участвуют ровно 2p - 1 многочленов (из которых p одночленов); отсюда будет следовать, что количество существенных многочленов равно 2n+ 1. База при p = 1 очевидна.
        Пусть теперь многочлен P был получен на некотором шаге как
        сумма Q и R, и количества ненулевых коэффициентов в P , Q
        и R равны p, q и r соответственно; тогда p = q +r. По предположению индукции, в Q и R участвуют 2q - 1 и 2p - 1 многочленов, среди которых нет совпадающих (поскольку в Q и R нет
        общих одночленов). Тогда в P , с учётом самого P , участвуют
        (2q - 1) + (2r -1) + 1 = 2p - 1 многочленов.
        
        Покажем, наконец, что в каждую минуту на доске появлялось не более одного финального существенного многочлена.
        Действительно, пусть в некоторую минуту появились одновременно существенные многочлены $S_p$ и $S_q$ (p < q). Рассмотрим
        первый момент, когда на доске появился многочлен P , в котором одновременно участвуют и $S_p$, и $S_q$ ; тогда он появился как
        сумма двух многочленов, каждый из которых содержит одночлен $x^p$
        . Но тогда коэффициент при $x^p$ в P не меньше 2, что
        невозможно.
        Итак, на доске есть n финальных и 2n + 1 существенных
        многочленов, при этом не больше m из них являются и теми,
        и другими. Значит, общее количество многочленов на доске не
        меньше, чем n + (2n + 1) - m. С другой стороны, исходно на
        доске было n + 1 многочленов, а добавилось не больше, чем mk.
        Значит, (n + 1) + mk > n + (2n + 1) - m, или m(k + 1) > 2n, что
        и требовалось доказать.
        
        Замечание. Если зафиксировать натуральное k, то при
        всех достаточно больших n оценка в задаче точна.
        ''')
    st.subheader('Самая легкая задача')
    st.write('Самой легкой оказалась задача 1 для 9 класса в 2014 году, средний балл по которой составил 6.86 баллов из 7. Вы можете попробовать свои силы, решив ее ниже.')
    st.write('''
     По кругу расставлены 99 натуральных чисел. Известно, что
    любые два соседних числа отличаются или на 1, или на 2,
    или в два раза. Докажите, что хотя бы одно из этих чисел
    делится на 3. (С. Берлов)
    ''')
    if st.checkbox('Показать решение', key = 432):
        st.write('''
        Пусть ни одно из чисел не делится на 3. Тогда
        каждое число даёт остаток 1 или 2 при делении на 3. Но числа,
        дающие одинаковые ненулевые остатки при делении на 3, не могут отличаться на 1 или на 2; не могут они и отличаться в два
        раза. Значит, соседние числа дают различные остатки при делении на 3, то есть остатки 1 и 2 чередуются. Но тогда общее количество чисел должно быть чётным, что не так. Противоречие.
        ''')
    ### График рейтинга задач по сложности
    st.subheader('Рейтинг задач по сложности')
    grades_ = st.multiselect('Классы: ', [9, 10, 11], default = [9, 10, 11], key = 542)
    if len(grades_) == 0:
        st.write('Пожалуйста, выберите хотя бы один класс.')
    else:
        problems_hardness = df.query('grade in @grades_').groupby('year').mean()[[
            'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8']]
        problems_hardness_melted = problems_hardness.melt(ignore_index=False).reset_index()
        problems_hardness_melted['variable'] = problems_hardness_melted['variable'].str[1:]
        ### INSPIRED BY https://altair-viz.github.io/gallery/bump_chart.html
        rait = alt.Chart(problems_hardness_melted).mark_line(point=True).encode(
            x=alt.X("year:O", title="Год"),
            y=alt.Y("rank:O", title='Номер задачи в рейтинге'),
            color=alt.Color("variable:N", title='Задача'),
            tooltip=[alt.Tooltip("variable:N", title='Задача'), alt.Tooltip("rank:O", title='Номер задачи в рейтинге')]
        ).transform_window(
            rank="rank()",
            sort=[alt.SortField("value", order="ascending")],
            groupby=["year"],
        ).properties(
            title="Рейтинг задач по сложности",
            width=900,
            height=400,
        )
        st.altair_chart(rait)
        ### END
    st.write('Этот график показывает рейтинг задач, отсортированных по сложности от самой сложной (первая в рейтинге) до самой простой (последняя в рейтинге). Глядя на этот график, мы можем, например, сделать вывод, что составители ни разу не ошиблись в сортировке задач по сложности внутри одного дня по средним показателям за все классы.')
    ### Box plot и график распределения баллов для выбранного варианта
    st.subheader('Сложность выбранного варианта')
    year_ = st.slider( "Выберите год" , 2009 , 2019, 2019, key = 3214)
    sgrade = st.selectbox('Выберите класс', [9, 10, 11], 2, key = 432)
    probs = df.query('grade == @sgrade and year == @year_')[['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8']].melt().rename(columns = {'variable' : 'Задача', 'value': 'Баллы'})
    probs['Задача'] = probs['Задача'].str[1:]
    if st.checkbox('Отобразить простую картинку', key = 43253):
        fig, ax = plt.subplots()
        sns.boxplot(data=probs, x="Задача", y="Баллы", ax = ax)
        st.pyplot(fig)
    else:
        bar_plt_ex = px.box(probs, x="Задача", y="Баллы")
        st.plotly_chart(bar_plt_ex)
    st.write('Это так называемая диаграмма размаха (или просто ящик с усами). Она показывает медиану, квартили и выбросы по баллам для каждой из задач выбранного варианта. Для знакомых с теорией вероятности и понятием рапределения случайной величины, ниже также предлагается график распределения выставленных за задачу баллов для того же варианта. (Понятно, что само число баллов дискретно, но по имеющейся выборке можно построить непрерывное приближение, которое и используется здесь).')
    alt.data_transformers.disable_max_rows()
    ### INSPIRED BY https://altair-viz.github.io/user_guide/transform/density.html
    nepr = alt.Chart(probs).encode(tooltip = [alt.Tooltip('Задача'), alt.Tooltip('Баллы'), alt.Tooltip('Распределение:Q')]).transform_density(
        'Баллы',
        as_=['Баллы', 'Распределение'],
        groupby=['Задача'],
        extent=[0, 7],
    ).mark_area(fillOpacity=0.3,).encode(
        x='Баллы',
        y='Распределение:Q',
        color='Задача',
        stroke='Задача',
    ).properties(
            title="Распределение баллов за задачи",
            width=900,
            height=400,
        )
    st.altair_chart(nepr)
    ### END
    ### Heatmap для матрица корелляций
    st.write('Теперь посмотрим, есть ли корелляция в баллах, полученных за различные задачи (по всем годам)')
    probl = df[['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8']]
    if st.checkbox('Отобразить простую картинку', key = 5425):
        fig, ax = plt.subplots()
        sns.heatmap(probl.corr(), cmap = 'Blues', ax = ax, cbar_kws={'label': 'Коэффициент корелляции'})
        ax.set_xlabel('Задача 1')
        ax.set_ylabel('Задача 2')
        ax.set_title('Матрица корелляций между баллами за задачи')
        st.pyplot(fig)
    else:
        x, y = np.meshgrid(range(1, 9), range(1, 9))
        z = np.array(probl.corr())
        mat_data = pd.DataFrame({'x': x.ravel(),
                               'y': y.ravel(),
                               'z': z.ravel()})
        mat = alt.Chart(mat_data).mark_rect().encode(
            x= alt.X('x:O', title = 'Первая задача'),
            y= alt.Y('y:O', title = 'Вторая задача'),
            color=alt.Color('z:Q', title='Коэффициент корелляции'),
            tooltip=[alt.Tooltip('x:O', title='Задача 1'), alt.Tooltip('y:O', title='Задача 2'),
                     alt.Tooltip('z:O', title='Коэффициент корелляции')]
        ).properties(
            title="Матрица корелляций между баллами за задачи",
            width=650,
            height=450,
        )
        st.altair_chart(mat)
    st.write('Как мы видим, особой корелляции в баллах за разные задачи нет, но все же наблюдается слабая корелляция между любыми двумя простыми задачами или между любыми двумя сложными.')
    ### Графики проекций для алгоритма понижения размерности данных
    st.write('Хотелось бы как-то найти в полученных данных аномалии, например победителей, которые решили очень сложную задачу, но при этом не справились с легкой. Если бы всего задач было 2 или 3, найти таких участников визуально нам помогла бы обычная диаграмма рассеивания (scatter plot). Но всего задач 8, а это слишком большая размерность пространства, чтобы его можно было изобразить наглядно. Однако, используя методы машинного обучения мы можем рассмотреть не сами данные, а их проекцию в пространство меньшей размерности.')
    pca = PCA(n_components=2, random_state = 14)
    pca_res = pca.fit_transform(np.array(probl))
    df2d = pd.DataFrame(pca_res).rename(columns = {0 : 'x', 1 : 'y'})
    data2d = pd.concat([df, df2d], axis = 1).reset_index()
    scat2d = px.scatter(data2d, x='x', y='y',
                        color='status', hover_name="index", title = 'Проекция данных на 2-мерное пространство')
    st.plotly_chart(scat2d)
    st.write('Теперь построим проекцию в 3-мерное пространство.')
    pca3d = PCA(n_components=3, random_state = 14)
    pca_res3d = pca3d.fit_transform(np.array(probl))
    df3d = pd.DataFrame(pca_res3d).rename(columns = {0 : 'x', 1 : 'y', 2: 'z'})
    data3d = pd.concat([df, df3d], axis = 1).reset_index()
    scat3d = px.scatter_3d(data3d, x='x', y='y', z='z',
                        color='status', hover_name="index", title = 'Проекция данных на 3-мерное пространство')
    st.plotly_chart(scat3d)
    ### Таблица для запросов по индексу
    st.write('Здесь вы можете выбрать индекс интересующего вас наблюдения, чтобы затем получить по нему полную информацию. Например, посмотрим на победителя под индексом 2713, который достаточно сильно визуально выделяется среди остальных точек победителей.')
    indx = st.number_input('Индекс', min_value=0, max_value=3466, value=2713, step=1)
    st.table(pd.DataFrame(df.iloc[indx]).T.drop('region_id', axis = 1))
    ### Заключительная информация
    st.header('Проверяющим')
    st.write('Поскольку проект получился достаточно объемным, позволю себе перечислить здесь некоторые критерии, требуемые от проекта для облегчения проверки. В проекте используются в основном библиотеки визуализации altair и plotly.express. Я считаю, что этого было бы достаточно, поскольку они позволяют строить все основные графики, обладают интерактивностью и красиво выглядят. Однако, чтобы формально соблюсти требование о 3 и более библиотеках, я добавил к некоторым графикам возможность отображения их простой неинтерактивной версии средствами seaborn и matplotlib. Почти все визуализации интерактивны. Кроме того, есть анимированная визуализация динамики числа призеров и победителей по регионам. О красоте и прочих критериях предлагаю судить вам самим). В конце страницы, а также в приложенном архиве можно найти весь код. Прямое копирование чужого кода оформляется как ### FROM URL, а использование демо - графиков различных библиотек как основы или источника для вдохновения как ### INSPIRED BY URL. Надеюсь, вы получили удовольствие от просмотра проекта.')
    st.header('Источники')
    st.write('Данные взяты из датасета на [Kaggle](https://www.kaggle.com/datasets/kirillpupkov/allrussian-math-olympiad-results-20092021?resource=download). Для составления карты использовалась разметка topojson [отсюда](https://github.com/amdest/russia-map/blob/main/Russia.topojson). Текст задач и решения взяты [здесь](https://olimpiada.ru/activity/72/tasks). В качестве источников вдохновения использовались демо-графики библиотек altair и plotly.express, а также чай и печеньки.')
    st.header('Исходный код')
