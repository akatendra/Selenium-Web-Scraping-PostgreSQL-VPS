from datetime import timedelta, datetime

import logging.config

import seaborn as sb
import pandas as pd
import database
# Bugfix for matplotlib==3.6.0
# https://stackoverflow.com/questions/73745245/i-have-error-while-using-matplotlib-has-no-attribute-figurecanvas
# import matplotlib
# matplotlib.use('TkAgg')
# Bugfix for matplotlib==3.6.0
import matplotlib.pyplot as plt


# timestamp = (datetime.now() + timedelta(hours=3)).strftime("%d-%m-%Y %H:%M:%S")


def cm_to_inch(value):
    return value / 2.54


def px_to_inch(px, dpi=72):
    return px / dpi


def show_bar_values(obj, label_type='center'):
    for ax in obj.axes.ravel():
        # add annotations
        for bar_container in ax.containers:
            labels = [bar.get_height() for bar in bar_container]
            ax.bar_label(bar_container,
                         labels=labels,
                         # label_type='edge',
                         label_type=label_type,
                         fontsize=16,
                         # rotation=90,
                         padding=2)
        ax.margins(y=0.2)


def put_timestamp(horizontal='left', vertical='top'):
    # Define axes
    left = 0.01
    width = 0.9
    bottom = 0.01
    height = 0.9
    right = left + width
    top = bottom + height
    ax = plt.gca()

    # Transform axes
    ax.set_transform(ax.transAxes)

    if horizontal == 'left':
        horizontal_v = left
    else:
        horizontal_v = right

    if vertical == 'top':
        vertical_v = top
    else:
        vertical_v = bottom
    timestamp = (datetime.now() + timedelta(hours=3)).strftime(
        "%d-%m-%Y %H:%M:%S")
    # Define timestamp text
    ax.text(horizontal_v,
            vertical_v,
            timestamp,
            horizontalalignment=horizontal,
            verticalalignment=vertical,
            color='red',
            size=12,
            transform=ax.transAxes)


def get_max_y_value(obj):
    # y = 0
    maximum_y = 0
    for ax in obj.axes.ravel():
        # add annotations
        for bar_container in ax.containers:
            y = max([bar.get_height() for bar in bar_container])
            if y >= maximum_y:
                maximum_y = y
    return maximum_y


def event(histogram, date, text, max_y=None):
    # adding a vertical line for the defeat of the Crimean bridge
    plt.axvline(x=date, ymin=0.2, ymax=1, linewidth=4, color='red',
                label=text)

    # adding data label to mean line
    # box = {'boxstyle': 'square',  # стиль области
    #        'pad': 0.9,  # отступы
    #        'facecolor': 'black',  # цвет области
    #        'edgecolor': 'red'  # цвет крайней линии
    #        }
    if max_y is None:
        y = get_max_y_value(histogram)
    else:
        y = max_y
    plt.text(x=date,
             # x-coordinate position of data label, adjusted to be 3 right of the data point
             y=y,
             # y-coordinate position of data label, to take max height
             s='  ' + text,
             # rotation=90,
             fontsize=16,
             # position=(2.5, 200),
             color='red')


def add_events(histogram, max_y=None):
    # Defeat of the Crimean bridge
    event(histogram, '2022-10-08 Sat', 'крымский мост\n  сказал "мяу"',
          max_y=max_y)
    event(histogram, '2022-10-10 Mon', 'Ракетная атака\n по Украине\n 10-11 октября\n 111 ракет',
          max_y=max_y)
    event(histogram, '2022-10-17 Mon',
          'Ракетная атака\n по Украине\n 17-22 октября\n 49 ракет',
          max_y=max_y)
    # Bandera Boat Attack on Sevastopol Bay
    event(histogram, '2022-10-29 Sat',
          'атака\n бандероботами\n на севастопольскую\n бухту', max_y=max_y)
    event(histogram, '2022-10-31 Mon',
          'Ракетная атака\n по Украине\n 50 ракет',
          max_y=max_y)
    event(histogram, '2022-11-09 Wed',
          'шойгу приказал\n оставить Херсон\n строительство\n  укреплений\n на въезде в Крым',
          max_y=max_y)
    event(histogram, '2022-11-11 Fri',
          'ЗСУ звільнили\n  Херсон', max_y=max_y)
    event(histogram, '2022-11-15 Tue',
          'Массированная\n ракетная атака\n по Украине\n 15-17 ноября\n 120 ракет\n Попали ракетами\n в Польшу',
          max_y=max_y)
    event(histogram, '2022-11-23 Wed',
          'Ракетная атака\n по инфраструктуре\n Украины\n 70 ракет\n блэкаут', max_y=max_y)
    event(histogram, '2022-12-05 Mon',
          'Ракетная атака\n по инфраструктуре\n Украины\n 70 ракет', max_y=max_y)
    event(histogram, '2022-12-16 Fri',
          'Ракетная атака\n по инфраструктуре\n Украины\n 76 ракет',
          max_y=max_y)
    event(histogram, '2022-12-20 Tue',
          'Сервер\n остановился', max_y=max_y)
    event(histogram, '2022-12-23 Fri',
          'Сервер\n перезапущен', max_y=max_y)
    event(histogram, '2022-12-29 Thu',
          'Ракетная атака\n по инфраструктуре\n Украины\n 29-31 декабря\n 89 ракет', max_y=max_y)
    event(histogram, '2023-01-14 Sat',
          'Ракетная атака\n по инфраструктуре\n Украины\n 38 ракет',
          max_y=max_y)
    event(histogram, '2023-01-26 Thu',
          'Ракетная атака\n по инфраструктуре\n Украины\n 55 ракет',
          max_y=max_y)
    event(histogram, '2023-02-10 Fri',
          'Ракетная атака\n по инфраструктуре\n Украины\n 71 ракета',
          max_y=max_y)
    event(histogram, '2023-03-09 Thu',
          'Ракетная атака\n по инфраструктуре\n Украины\n 81 ракета',
          max_y=max_y)
    event(histogram, '2023-04-24 Mon',
          'Атака надводными\n дронами по\n Севастополю',
          max_y=max_y)
    event(histogram, '2023-04-29 Sat',
          'Пожар на нефтебазе\n в Казачьей бухте Севастополя\n после удара дроном',
          max_y=max_y)
    event(histogram, '2023-05-03 Wed', 'Атака дронами\n по кремлю', max_y=max_y)


def add_events_2(histogram, max_y=None):
    event(histogram, '2023-06-06 Tue', 'Взорвана\n Каховская ГЭС', max_y=max_y)


def kvartiry_vtorichka_split_visualization(date_start, date_end, file_name, event=1, max_y=None):
    # 1. Количество новых объявлений по дням квартиры-вторичка
    # Количество дней в БД, чтоб знать какой длины делать картинку.
    days_count = database.get_days_count_4_period('kvartiry_vtorichka', date_start, date_end)

    # Aspect ratio
    aspect = int(days_count[0][0] // 4)
    logger.debug(f'aspect {aspect}')

    data1 = database.get_item_count_per_day2_4_period('kvartiry_vtorichka', date_start, date_end)
    df1 = pd.DataFrame(data1, columns=['Дата'])
    df1.sort_values(by=['Дата'],
                    axis=0,
                    inplace=True,
                    ascending=True)
    logger.debug(f'{df1}')
    histogram = sb.displot(data=df1,
                           x='Дата',
                           kind='hist',
                           kde=True,
                           height=6,
                           aspect=aspect)
    histogram.set(ylabel='Кол-во новых объявлений в день')
    histogram.set(title='Кол-во новых объявлений по дням | Квартиры-вторичка')
    if max_y is not None:
        histogram.set(ylim=(0, max_y))

    show_bar_values(histogram)

    put_timestamp()
    if event == 1:
        add_events(histogram)
    else:
        add_events_2(histogram, max_y=max_y)
    # Fix problem seaborn function 'displot' does not show up a part of the title
    # https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
    plt.tight_layout()

    # Fix problem Saving a figure after invoking pyplot.show() results in an empty file
    # https://stackoverflow.com/questions/21875356/saving-a-figure-after-invoking-pyplot-show-results-in-an-empty-file
    fig = plt.gcf()
    fig.savefig(f'image_out/{file_name}.png', format='png', dpi=72)

    plt.show()

def kvartiry_novostroyka_split_visualization(date_start, date_end, file_name, event=1, max_y=None):
    # 1.2 Количество новых объявлений по дням квартиры-новострой
    # Количество дней в БД, чтоб знать какой длины делать картинку.
    days_count = database.get_days_count_4_period('kvartiry_novostroyka', date_start, date_end)

    # Aspect ratio
    aspect = int(days_count[0][0] // 4)
    logger.debug(f'aspect {aspect}')

    data12 = database.get_item_count_per_day2_4_period('kvartiry_novostroyka', date_start, date_end)
    df12 = pd.DataFrame(data12, columns=['Дата'])
    df12.sort_values(by=['Дата'],
                     axis=0,
                     inplace=True,
                     ascending=True)
    logger.debug(f'{df12}')
    histogram = sb.displot(data=df12,
                           x='Дата',
                           kind='hist',
                           kde=True,
                           height=6,
                           aspect=aspect)
    histogram.set(ylabel='Кол-во новых объявлений в день')
    histogram.set(title='Кол-во новых объявлений по дням | Квартиры-новострой')
    if max_y is not None:
        histogram.set(ylim=(0, max_y))

    show_bar_values(histogram)
    put_timestamp()
    if event == 1:
        add_events(histogram)
    else:
        add_events_2(histogram, max_y=max_y)
    # Fix problem seaborn function 'displot' does not show up a part of the title
    # https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
    plt.tight_layout()

    # Fix problem Saving a figure after invoking pyplot.show() results in an empty file
    # https://stackoverflow.com/questions/21875356/saving-a-figure-after-invoking-pyplot-show-results-in-an-empty-file
    fig = plt.gcf()
    fig.savefig(f'image_out/{file_name}.png', format='png', dpi=72)

    plt.show()

def doma_dachi_kottedzhi_split_visualization(date_start, date_end, file_name, event=1, max_y=None):
    # 1.3 Количество новых объявлений по дням дома, дачи и коттеджи
    # Количество дней в БД, чтоб знать какой длины делать картинку.
    days_count = database.get_days_count_4_period('doma_dachi_kottedzhi', date_start, date_end)

    # Aspect ratio
    aspect = int(days_count[0][0] // 4)
    logger.debug(f'aspect {aspect}')

    data1_3 = database.get_item_count_per_day2_4_period('doma_dachi_kottedzhi', date_start, date_end)
    df1_3 = pd.DataFrame(data1_3, columns=['Дата'])
    df1_3.sort_values(by=['Дата'],
                      axis=0,
                      inplace=True,
                      ascending=True)
    logger.debug(f'{df1_3}')
    histogram = sb.displot(data=df1_3,
                           x='Дата',
                           kind='hist',
                           kde=True,
                           height=6,
                           aspect=aspect)
    histogram.set(ylabel='Кол-во новых объявлений в день')
    histogram.set(title='Кол-во новых объявлений по дням | Дома, дачи и коттеджи')
    if max_y is not None:
        histogram.set(ylim=(0, max_y))

    show_bar_values(histogram)
    put_timestamp()
    if event == 1:
        add_events(histogram)
    else:
        add_events_2(histogram, max_y=max_y)
    # Fix problem seaborn function 'displot' does not show up a part of the title
    # https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
    plt.tight_layout()

    # Fix problem Saving a figure after invoking pyplot.show() results in an empty file
    # https://stackoverflow.com/questions/21875356/saving-a-figure-after-invoking-pyplot-show-results-in-an-empty-file
    fig = plt.gcf()
    fig.savefig(f'image_out/{file_name}.png', format='png', dpi=72)

    plt.show()


def price_area_average_split_visualization(date_start, date_end, file_name, event=1, max_y_external=None):
    # 2. Средняя стоимость квадратного метра по дням вся недвижимость
    # Количество дней в БД, чтоб знать какой длины делать картинку.
    days_count = database.get_days_count_4_period('kvartiry_vtorichka', date_start, date_end)

    # Aspect ratio
    aspect = int(days_count[0][0] // 4)
    logger.debug(f'aspect {aspect}')

    data2 = database.get_item_date_price_area_average_union_4_period(date_start, date_end)
    df2 = pd.DataFrame(data2, columns=['Дата', 'Средняя стоимость за м2, руб.',
                                       'Тип недвижимости'])

    df2.sort_values(by=['Дата'],
                    axis=0,
                    inplace=True,
                    ascending=True)

    logger.debug(f'{df2}')

    color_palette = {'квартиры-вторичка': '#2ca02c',
                     'Дома, дачи и коттеджи': '#ff7f0e',
                     'квартиры-новострой': '#1f77b4'
                     }

    av_price = sb.relplot(data=df2,
                          x='Дата',
                          y='Средняя стоимость за м2, руб.',
                          kind="line",
                          hue='Тип недвижимости',
                          height=6,
                          aspect=aspect,
                          palette=color_palette)
    av_price.set(title='Средняя стоимость квартир за м2, руб. по дням')
    if max_y_external is not None:
        av_price.set(ylim=(0, max_y_external))

    # Shift legend to another position
    # https://stackoverflow.com/questions/39803385/what-does-a-4-element-tuple-argument-for-bbox-to-anchor-mean-in-matplotlib/39806180#39806180
    legend = av_price._legend
    legend.set_bbox_to_anchor([1, 0.9])
    #  Add annotations with average price
    max_y = 0

    for x, y, item_type in zip(df2['Дата'],
                               df2['Средняя стоимость за м2, руб.'],
                               df2['Тип недвижимости']):
        if y >= max_y:
            max_y = y
        # the position of the data label relative to the data point can be
        # adjusted by adding/subtracting a value from the x / y coordinates

        # Simple text
        # plt.text(x=x,  # x-coordinate position of data label
        #          # y-coordinate position of data label, adjusted to be 150 below the data point
        #          y=y + 150,
        #          s='{:.0f}'.format(y),  # data label, formatted to ignore decimals
        #          color='#1f77b4')  # set colour of line

        # text with background
        plt.text(x, y - 150, '{:.0f}'.format(y), color='white').set_backgroundcolor(color_palette.get(item_type))
        """
        if item_type == 'квартиры-вторичка':
            plt.text(x, y - 150, '{:.0f}'.format(y),
                     color='white').set_backgroundcolor(
                '#2ca02c')
        elif item_type == 'Дома, дачи и коттеджи':
            plt.text(x, y - 150, '{:.0f}'.format(y),
                     color='white').set_backgroundcolor(
                '#ff7f0e')
        else:
            plt.text(x, y - 150, '{:.0f}'.format(y),
                     color='white').set_backgroundcolor(
                '#1f77b4')
        """
    put_timestamp()
    if event == 1:
        add_events(av_price, max_y)
    else:
        add_events_2(av_price, max_y)

    # Fix problem seaborn function 'displot' does not show up a part of the title
    # https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
    plt.tight_layout()

    # Fix problem Saving a figure after invoking pyplot.show() results in an empty file
    # https://stackoverflow.com/questions/21875356/saving-a-figure-after-invoking-pyplot-show-results-in-an-empty-file
    fig = plt.gcf()
    fig.savefig(f'image_out/{file_name}.png', format='png', dpi=72)

    plt.show()


def kvartiry_vtorichka_sevastopol_split_visualization(date_start, date_end, file_name, event=1, max_y=None):
    # 4. Количество новых объявлений по Севастополю по дням
    # Количество дней в БД, чтоб знать какой длины делать картинку.
    days_count = database.get_days_count_4_period('kvartiry_vtorichka',
                                                  date_start, date_end)

    # Aspect ratio
    aspect = int(days_count[0][0] // 4)
    logger.debug(f'aspect {aspect}')

    data2 = database.get_item_date_price_area_average_union_4_period(
        date_start, date_end)
    data4 = database.get_item_count_sevastopol_4_period('kvartiry_vtorichka', date_start, date_end)
    df4 = pd.DataFrame(data4, columns=['Дата'])
    df4.sort_values(by=['Дата'],
                    axis=0,
                    inplace=True,
                    ascending=True)

    logger.debug(f'{df4}')

    histogram_sevastopol = sb.displot(data=df4,
                                      x='Дата',
                                      kind='hist',
                                      kde=True,
                                      height=6,
                                      aspect=aspect
                                      )
    histogram_sevastopol.set(ylabel='Кол-во объявлений')
    histogram_sevastopol.set(title='Количество новых объявлений по Севастополю по дням')
    if max_y is not None:
        histogram_sevastopol.set(ylim=(0, max_y))

    show_bar_values(histogram_sevastopol)
    put_timestamp()
    if event == 1:
        add_events(histogram_sevastopol)
    else:
        add_events_2(histogram_sevastopol, max_y=max_y)

    # Fix problem seaborn function 'displot' does not show up a part of the title
    # https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
    plt.tight_layout()

    # Fix problem Saving a figure after invoking pyplot.show() results in an empty file
    # https://stackoverflow.com/questions/21875356/saving-a-figure-after-invoking-pyplot-show-results-in-an-empty-file
    fig = plt.gcf()
    fig.savefig(f'image_out/{file_name}.png', format='png', dpi=72)
    plt.show()


def get_visualization():
    ########################### New Version ###################################
    # Plot style
    sb.set_style("whitegrid",
                 {"grid.color": ".6",
                  "grid.linestyle": ":"
                  })

    # sb.set(rc={"figure.figsize": (aspect, 6)}) #width=30, #height=6

    today = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    kvartiry_vtorichka_split_visualization(date_start='2022-01-01', date_end='2023-06-01', file_name='histogram_vtorichka_1')
    kvartiry_vtorichka_split_visualization(date_start='2023-06-01', date_end=today, file_name='histogram_vtorichka_2', event=2, max_y=1200)

    kvartiry_novostroyka_split_visualization(date_start='2022-01-01', date_end='2023-06-01', file_name='histogram_vtorichka_novostroy_1')
    kvartiry_novostroyka_split_visualization(date_start='2023-06-01', date_end=today, file_name='histogram_vtorichka_novostroy_2', event=2, max_y=1000)

    doma_dachi_kottedzhi_split_visualization(date_start='2022-01-01', date_end='2023-06-01', file_name='histogram_doma_dachi_kottedzhi_1')
    doma_dachi_kottedzhi_split_visualization(date_start='2023-06-01', date_end=today, file_name='histogram_doma_dachi_kottedzhi_2', event=2, max_y=2000)

    price_area_average_split_visualization(date_start='2022-01-01',
                                             date_end='2023-06-01',
                                             file_name='av_price_1')
    price_area_average_split_visualization(date_start='2023-06-01',
                                             date_end=today,
                                             file_name='av_price_2',
                                             event=2)

    kvartiry_vtorichka_sevastopol_split_visualization(date_start='2022-01-01',
                                           date_end='2023-06-01',
                                           file_name='histogram_sevastopol_1')
    kvartiry_vtorichka_sevastopol_split_visualization(date_start='2023-06-01',
                                           date_end=today,
                                           file_name='histogram_sevastopol_2',
                                           event=2, max_y=350)
    ########################### End New Version ###############################

    # 2. Средняя стоимость квадратного метра по дням вся недвижимость
    # Количество дней в БД, чтоб знать какой длины делать картинку.
    days_count = database.get_days_count('kvartiry_vtorichka')

    # Aspect ratio
    aspect = int(days_count[0][0] // 4)
    logger.debug(f'aspect {aspect}')
    data2 = database.get_item_date_price_area_average_union()
    df2 = pd.DataFrame(data2, columns=['Дата', 'Средняя стоимость за м2, руб.',
                                       'Тип недвижимости'])
    logger.debug(f'{df2}')
    # df2.sort_values(by=['Дата'],
    #                 axis=0,
    #                 inplace=True,
    #                 ascending=True)
    # logger.debug(f'{df2}')
    av_price = sb.relplot(data=df2,
                          x='Дата',
                          y='Средняя стоимость за м2, руб.',
                          kind="line",
                          hue='Тип недвижимости',
                          height=6,
                          aspect=aspect)
    av_price.set(title='Средняя стоимость квартир за м2, руб. по дням')

    # Shift legend to another position
    # https://stackoverflow.com/questions/39803385/what-does-a-4-element-tuple-argument-for-bbox-to-anchor-mean-in-matplotlib/39806180#39806180
    legend = av_price._legend
    legend.set_bbox_to_anchor([1, 0.9])
    #  Add annotations with average price
    max_y = 0
    for x, y, item_type in zip(df2['Дата'],
                               df2['Средняя стоимость за м2, руб.'],
                               df2['Тип недвижимости']):
        if y >= max_y:
            max_y = y
        # the position of the data label relative to the data point can be
        # adjusted by adding/subtracting a value from the x / y coordinates

        # Simple text
        # plt.text(x=x,  # x-coordinate position of data label
        #          # y-coordinate position of data label, adjusted to be 150 below the data point
        #          y=y + 150,
        #          s='{:.0f}'.format(y),  # data label, formatted to ignore decimals
        #          color='#1f77b4')  # set colour of line

        # text with background
        if item_type == 'квартиры-вторичка':
            plt.text(x, y - 150, '{:.0f}'.format(y),
                     color='white').set_backgroundcolor(
                '#2ca02c')
        elif item_type == 'Дома, дачи и коттеджи':
            plt.text(x, y - 150, '{:.0f}'.format(y),
                     color='white').set_backgroundcolor(
                '#ff7f0e')
        else:
            plt.text(x, y - 150, '{:.0f}'.format(y),
                     color='white').set_backgroundcolor(
                '#1f77b4')

    put_timestamp()
    add_events(av_price, max_y)
    add_events_2(av_price, max_y)

    # Fix problem seaborn function 'displot' does not show up a part of the title
    # https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
    plt.tight_layout()

    # Fix problem Saving a figure after invoking pyplot.show() results in an empty file
    # https://stackoverflow.com/questions/21875356/saving-a-figure-after-invoking-pyplot-show-results-in-an-empty-file
    fig = plt.gcf()
    fig.savefig(f'image_out/av_price.png',
                format='png', dpi=72)

    plt.show()

    # 3. Количество новых объявлений по городам из ТОП10 ГОРОДОВ по количеству объявлений
    data3 = database.get_top10_cities('kvartiry_vtorichka')
    order_vector = data3[0]
    logger.debug(f'order_vector {order_vector}')
    df3 = pd.DataFrame(data3[1], columns=['Города'])
    df3['Города'] = pd.Categorical(df3['Города'], categories=order_vector)
    logger.debug(f'{df3}')

    histogram_city = sb.displot(data=df3,
                                x='Города',
                                kind='hist',
                                kde=True,
                                height=6,
                                aspect=3
                                )
    histogram_city.set(ylabel='Кол-во объявлений за все время')
    histogram_city.set(
        title='Количество новых объявлений по городам из ТОП10 ГОРОДОВ по количеству объявлений c 27-07-2022 г.')

    # sb.set(rc={"figure.figsize": (30, 6)}) #width=30, #height=6
    show_bar_values(histogram_city)
    put_timestamp()

    # Fix problem seaborn function 'displot' does not show up a part of the title
    # https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
    plt.tight_layout()

    # Fix problem Saving a figure after invoking pyplot.show() results in an empty file
    # https://stackoverflow.com/questions/21875356/saving-a-figure-after-invoking-pyplot-show-results-in-an-empty-file
    fig = plt.gcf()
    fig.savefig(f'image_out/histogram_cities.png',
                format='png', dpi=72)

    plt.show()

    logger.info(f'Visualization complete!')


 # Set up logging
logging.config.fileConfig("logging_visualisation.ini",
                          disable_existing_loggers=False)
logger = logging.getLogger(__name__)
# Remove matplotlib.font_manager from logging
# logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
# Remove all matplotlib from logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)

if __name__ == '__main__':
    get_visualization()
