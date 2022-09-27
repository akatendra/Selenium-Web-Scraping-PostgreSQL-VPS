from datetime import timedelta, datetime

import seaborn as sb
import pandas as pd
import database
# Bugfix for matplotlib==3.6.0
# https://stackoverflow.com/questions/73745245/i-have-error-while-using-matplotlib-has-no-attribute-figurecanvas
# import matplotlib
# matplotlib.use('TkAgg')
# Bugfix for matplotlib==3.6.0
import matplotlib.pyplot as plt

import logging.config

timestamp = (datetime.now() + timedelta(hours=3)).strftime("%d-%m-%Y %H:%M:%S")


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
    global timestamp
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

    # Define timestamp text
    ax.text(horizontal_v,
            vertical_v,
            timestamp,
            horizontalalignment=horizontal,
            verticalalignment=vertical,
            color='r',
            size=12,
            transform=ax.transAxes)


def get_visualization():
    # Set up logging
    logging.config.fileConfig("logging_visualisation.ini", disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    # Remove matplotlib.font_manager from logging
    # logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
    # Remove all matplotlib from logging
    logging.getLogger('matplotlib').setLevel(logging.WARNING)

    output_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Plot style
    sb.set_style("whitegrid",
                 {"grid.color": ".6",
                  "grid.linestyle": ":"
                  })

    # 1. Количество новых объявлений по дням квартиры-вторичка
    # Количество дней в БД
    days_count = database.get_days_count('kvartiry_vtorichka')
    logger.debug(f'days_count {days_count}')
    # Aspect ratio
    aspect = int(days_count[0][0] // 5)
    logger.debug(f'aspect {aspect}')

    data1 = database.get_item_count_per_day2('kvartiry_vtorichka')
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

    show_bar_values(histogram)

    put_timestamp()

    # Fix problem seaborn function 'displot' does not show up a part of the title
    # https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
    plt.tight_layout()

    # Fix problem Saving a figure after invoking pyplot.show() results in an empty file
    # https://stackoverflow.com/questions/21875356/saving-a-figure-after-invoking-pyplot-show-results-in-an-empty-file
    fig = plt.gcf()
    fig.savefig(f'image_out/histogram_vtorichka.png',
                format='png', dpi=72)

    plt.show()

    # 1.1 Количество новых объявлений по дням вся недвижимость наложение одного на другое
    data11 = database.get_item_count_per_day3()
    df11 = pd.DataFrame(data11, columns=['Дата', 'Тип недвижимости'])
    # Ordering
    df11.sort_values(by=['Дата'],
                     axis=0,
                     inplace=True,
                     ascending=True)
    logger.debug(f'{df11}')
    histogram = sb.displot(data=df11,
                           x='Дата',
                           kind='hist',
                           kde=True,
                           hue='Тип недвижимости',
                           # col='Тип недвижимости',
                           multiple='dodge',
                           height=6,
                           aspect=aspect)
    histogram.set(ylabel='Кол-во новых объявлений в день')
    # histogram.set(title='Кол-во новых объявлений по дням')

    show_bar_values(histogram)

    put_timestamp()
    # Fix problem seaborn function 'displot' does not show up a part of the title
    # https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
    plt.tight_layout()

    # Fix problem Saving a figure after invoking pyplot.show() results in an empty file
    # https://stackoverflow.com/questions/21875356/saving-a-figure-after-invoking-pyplot-show-results-in-an-empty-file
    fig = plt.gcf()
    fig.savefig(f'image_out/histogram_vtorichka_novostroy.png',
                format='png', dpi=72)

    plt.show()

    # 1.2 Количество новых объявлений по дням квартиры-новострой
    data12 = database.get_item_count_per_day2('kvartiry_novostroyka')
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

    show_bar_values(histogram)
    put_timestamp()
    # Fix problem seaborn function 'displot' does not show up a part of the title
    # https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
    plt.tight_layout()

    # Fix problem Saving a figure after invoking pyplot.show() results in an empty file
    # https://stackoverflow.com/questions/21875356/saving-a-figure-after-invoking-pyplot-show-results-in-an-empty-file
    fig = plt.gcf()
    fig.savefig(f'image_out/histogram_novostroy.png',
                format='png', dpi=72)

    plt.show()

    # 1.3 Количество новых объявлений по дням дома, дачи и коттеджи
    data1_3 = database.get_item_count_per_day2('doma_dachi_kottedzhi')
    df1_3 = pd.DataFrame(data1_3, columns=['Дата'])
    df1_3.sort_values(by=['Дата'],
                      axis=0,
                      inplace=True,
                      ascending=True)
    logger.debug(f'{df12}')
    histogram = sb.displot(data=df1_3,
                           x='Дата',
                           kind='hist',
                           kde=True,
                           height=6,
                           aspect=aspect)
    histogram.set(ylabel='Кол-во новых объявлений в день')
    histogram.set(
        title='Кол-во новых объявлений по дням | Дома, дачи и коттеджи')

    show_bar_values(histogram)
    put_timestamp()
    # Fix problem seaborn function 'displot' does not show up a part of the title
    # https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
    plt.tight_layout()

    # Fix problem Saving a figure after invoking pyplot.show() results in an empty file
    # https://stackoverflow.com/questions/21875356/saving-a-figure-after-invoking-pyplot-show-results-in-an-empty-file
    fig = plt.gcf()
    fig.savefig(f'image_out/histogram_doma_dachi_kottedzhi.png',
                format='png', dpi=72)

    plt.show()

    # 2. Средняя стоимость квадратного метра по дням вся недвижимость
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
    for x, y, item_type in zip(df2['Дата'],
                               df2['Средняя стоимость за м2, руб.'],
                               df2['Тип недвижимости']):
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
        title='Количество новых объявлений по городам из ТОП10 ГОРОДОВ по количеству объявлений')

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

    # 4. Количество новых объявлений по Севастополю по дням
    data4 = database.get_item_count_sevastopol_simple('kvartiry_vtorichka')
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
    histogram_sevastopol.set(
        title='Количество новых объявлений по Севастополю по дням')

    show_bar_values(histogram_sevastopol)
    put_timestamp()

    # Fix problem seaborn function 'displot' does not show up a part of the title
    # https://stackoverflow.com/questions/69386785/python-seaborn-function-displot-does-not-show-up-a-part-of-the-title
    plt.tight_layout()

    # Fix problem Saving a figure after invoking pyplot.show() results in an empty file
    # https://stackoverflow.com/questions/21875356/saving-a-figure-after-invoking-pyplot-show-results-in-an-empty-file
    fig = plt.gcf()
    fig.savefig(f'image_out/histogram_sevastopol.png',
                format='png', dpi=72)
    plt.show()

    logger.info(f'Visualization complete!')

if __name__ == '__main__':
    get_visualization()
