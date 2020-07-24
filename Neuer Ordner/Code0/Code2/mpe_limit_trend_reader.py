#### for Boxcox limit ####
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
import time

#### for Boxcox limit ####
from scipy.stats import anderson
from scipy import stats

# read excel file (already cleaned from SQL)
df = pd.read_excel('D:\\books\\MPE_project\\Statistics\\NY_bin_statistics.xlsx')

# import data file generator
import data_gen as dg
df_all = dg.data_generator(df)

# lambda calculation
limit_iter = 0
mpe_limit_list = []
lot_id_list =[]

while limit_iter < 14:
    df_all = df_all[:-1]
    # create dict for lambdas
    lambda_dict = {}
    for column in df_all.columns[2:]:
        lambda_dict[column] = []

    # lambdas for parameters
    for i in df_all.columns[2:]:
        if len(df_all[df_all[i] != 0][i][177:]) < 50:
            # a = parameter list
            a = df_all[df_all[i] != 0][i][-50:]
            ################### box cox transformation ##################
            boxcox_list_transformed = []

            for k in np.arange(-2, 2.01, 0.01):
                boxcox_indivisual = stats.boxcox((a * 0.01), k)
                boxcox_list_transformed.append(boxcox_indivisual)
            #############################################################

            ################## Normality Check ##########################
            AD_value_list = []

            for t in range(0, 400, 1):
                AD_value_individual, AD_critical_value, AD_significance_level = anderson(boxcox_list_transformed[t])
                AD_value_list.append(AD_value_individual)
            ##############################################################
            ######################## Find lambda ##########################
            minimum_AD_value = min(AD_value_list)

            lambda_index_list = {}
            for index, value in enumerate(AD_value_list):
                lambda_index_list[value] =  index
            lambda_index_list[minimum_AD_value]


            lambda_list = {}
            lambda_ = np.arange(-2, 2.01, 0.01)
            for index, value in enumerate(lambda_):
                lambda_list[index] =  value
            lambda_list[lambda_index_list[minimum_AD_value]]
            ##############################################################
            #apeend data to dictionary
            lambda_dict[i].append(lambda_list[lambda_index_list[minimum_AD_value]])

        elif len(df_all[df_all[i] != 0][i][177:]) > 50:
            # a = parameter list
            a = df_all[df_all[i] != 0][i][177:]
            ################### box cox transformation ##################
            boxcox_list_transformed = []

            for k in np.arange(-2, 2.01, 0.01):
                boxcox_indivisual = stats.boxcox((a * 0.01), k)
                boxcox_list_transformed.append(boxcox_indivisual)
            #############################################################

            ################## Normality Check ##########################
            AD_value_list = []

            for t in range(0, 400, 1):
                AD_value_individual, AD_critical_value, AD_significance_level = anderson(boxcox_list_transformed[t])
                AD_value_list.append(AD_value_individual)
            ##############################################################
            ######################## Find lambda ##########################
            minimum_AD_value = min(AD_value_list)

            lambda_index_list = {}
            for index, value in enumerate(AD_value_list):
                lambda_index_list[value] =  index
            lambda_index_list[minimum_AD_value]


            lambda_list = {}
            lambda_ = np.arange(-2, 2.01, 0.01)
            for index, value in enumerate(lambda_):
                lambda_list[index] =  value
            lambda_list[lambda_index_list[minimum_AD_value]]
            ##############################################################
            # apeend data to dictionary
            lambda_dict[i].append(lambda_list[lambda_index_list[minimum_AD_value]])

    #drop Rth from lambda dict and df_all
    del lambda_dict['Rth']
    df_Rth = df_all.drop(['Rth'], axis = 1)

    # import _bin_limit_calculator function
    import _bin_limit_calculator as bc

    # print bin limit and detailed information about limit calculation
    bin_comparison = bc._bin_limit_calculator(df_all, lambda_dict)

    # make limit lists
    mpe_limit_list.append(bin_comparison)

    #make lot_id lists
    lot_id_list.append(df_all['lot_id'][len(df_all['lot_id']) - 1])

    limit_iter += 1
    if limit_iter == 1:
        print('1st loop')
    elif limit_iter == 2:
        print('2nd loop')
    elif limit_iter == 3:
        print('3rd loop')
    else:
        print(str(limit_iter) + 'th loop')

# Change limits into DataFrame
df_limit_trend = pd.DataFrame(mpe_limit_list)

## latest lot
# import data file generator 2
import data_gen as dg
df_all = dg.data_generator(df)

# create dict for lambdas
lambda_dict = {}
for column in df_all.columns[2:]:
    lambda_dict[column] = []

# lambdas for parameters
for i in df_all.columns[2:]:
    if len(df_all[df_all[i] != 0][i][177:]) < 50:
        # a = parameter list
        a = df_all[df_all[i] != 0][i][-50:]
        ################### box cox transformation ##################
        boxcox_list_transformed = []

        for k in np.arange(-2, 2.01, 0.01):
            boxcox_indivisual = stats.boxcox((a * 0.01), k)
            boxcox_list_transformed.append(boxcox_indivisual)
        #############################################################

        ################## Normality Check ##########################
        AD_value_list = []

        for t in range(0, 400, 1):
            AD_value_individual, AD_critical_value, AD_significance_level = anderson(boxcox_list_transformed[t])
            AD_value_list.append(AD_value_individual)
        ##############################################################
        ######################## Find lambda ##########################
        minimum_AD_value = min(AD_value_list)

        lambda_index_list = {}
        for index, value in enumerate(AD_value_list):
            lambda_index_list[value] =  index
        lambda_index_list[minimum_AD_value]


        lambda_list = {}
        lambda_ = np.arange(-2, 2.01, 0.01)
        for index, value in enumerate(lambda_):
            lambda_list[index] =  value
        lambda_list[lambda_index_list[minimum_AD_value]]
        ##############################################################
        #apeend data to dictionary
        lambda_dict[i].append(lambda_list[lambda_index_list[minimum_AD_value]])

    elif len(df_all[df_all[i] != 0][i][177:]) > 50:
        # a = parameter list
        a = df_all[df_all[i] != 0][i][177:]
        ################### box cox transformation ##################
        boxcox_list_transformed = []

        for k in np.arange(-2, 2.01, 0.01):
            boxcox_indivisual = stats.boxcox((a * 0.01), k)
            boxcox_list_transformed.append(boxcox_indivisual)
        #############################################################

        ################## Normality Check ##########################
        AD_value_list = []

        for t in range(0, 400, 1):
            AD_value_individual, AD_critical_value, AD_significance_level = anderson(boxcox_list_transformed[t])
            AD_value_list.append(AD_value_individual)
        ##############################################################
        ######################## Find lambda ##########################
        minimum_AD_value = min(AD_value_list)

        lambda_index_list = {}
        for index, value in enumerate(AD_value_list):
            lambda_index_list[value] =  index
        lambda_index_list[minimum_AD_value]


        lambda_list = {}
        lambda_ = np.arange(-2, 2.01, 0.01)
        for index, value in enumerate(lambda_):
            lambda_list[index] =  value
        lambda_list[lambda_index_list[minimum_AD_value]]
        ##############################################################
        # apeend data to dictionary
        lambda_dict[i].append(lambda_list[lambda_index_list[minimum_AD_value]])

#drop Rth from lambda dict and df_all
del lambda_dict['Rth']
df_Rth = df_all.drop(['Rth'], axis = 1)

# import _bin_limit_calculator function
import _bin_limit_calculator as bc

# print bin limit and detailed information about limit calculation
bin_comparison = bc._bin_limit_calculator(df_all, lambda_dict)

# reverse index of data
df_limit_trend_reversed = df_limit_trend[::-1]
lot_id_list_reversecd = lot_id_list[::-1]

# combine the latest data with the previous data
lot_now = df_all['lot_id'][len(df_all) - 1]
df_limit_now = pd.DataFrame(bin_comparison).T
lot_id_list_reversecd.append(lot_now)
df_limit_trend_reversed_2 = pd.concat([df_limit_trend_reversed, df_limit_now], ignore_index =True)

print(lot_id_list_reversecd)
print(df_limit_trend_reversed_2)


## yield now
# create dict for yield
lambda_dict_yield = {}
lambda_dict_yield['yield'] = []

# lambda for yield
for i in df_all.columns[1:2]:
    if len(df_all[df_all[i] != 0][i][177:]) < 50:
        a = df_all[df_all[i] != 0][i][-50:]
        ################### box cox transformation ##################
        boxcox_list_transformed = []

        for k in np.arange(-2, 2.01, 0.01):
            boxcox_indivisual = stats.boxcox((1-(a * 0.01)), k)
            boxcox_list_transformed.append(boxcox_indivisual)
        #############################################################

        ################## Normality Check ##########################
        AD_value_list = []

        for t in range(0, 400, 1):
            AD_value_individual, AD_critical_value, AD_significance_level = anderson(boxcox_list_transformed[t])
            AD_value_list.append(AD_value_individual)
        ##############################################################
        ######################## Find lambda ##########################
        minimum_AD_value = min(AD_value_list)

        lambda_index_list = {}
        for index, value in enumerate(AD_value_list):
            lambda_index_list[value] =  index
        lambda_index_list[minimum_AD_value]


        lambda_list = {}
        lambda_ = np.arange(-2, 2.01, 0.01)
        for index, value in enumerate(lambda_):
            lambda_list[index] =  value
        lambda_list[lambda_index_list[minimum_AD_value]]
        ##############################################################
        #apeend data to dictionary
        lambda_dict_yield[i].append(lambda_list[lambda_index_list[minimum_AD_value]])

    elif len(df_all[df_all[i] != 0][i][177:]) > 50:
        a = df_all[df_all[i] != 0][i][177:]
        ################### box cox transformation ##################
        boxcox_list_transformed = []

        for k in np.arange(-2, 2.01, 0.01):
            boxcox_indivisual = stats.boxcox((1-(a * 0.01)), k)
            boxcox_list_transformed.append(boxcox_indivisual)
        #############################################################

        ################## Normality Check ##########################
        AD_value_list = []

        for t in range(0, 400, 1):
            AD_value_individual, AD_critical_value, AD_significance_level = anderson(boxcox_list_transformed[t])
            AD_value_list.append(AD_value_individual)
        ##############################################################
        ######################## Find lambda ##########################
        minimum_AD_value = min(AD_value_list)

        lambda_index_list = {}
        for index, value in enumerate(AD_value_list):
            lambda_index_list[value] =  index
        lambda_index_list[minimum_AD_value]


        lambda_list = {}
        lambda_ = np.arange(-2, 2.01, 0.01)
        for index, value in enumerate(lambda_):
            lambda_list[index] =  value
        lambda_list[lambda_index_list[minimum_AD_value]]
        ##############################################################
        # apeend data to dictionary
        lambda_dict_yield[i].append(lambda_list[lambda_index_list[minimum_AD_value]])

# import _yield_limit_calculator function
import _yield_limit_calculator as yc

# print yield limit and detailed information about limit calculation
yield_comparison = yc._yield_limit_calculator(df_all, lambda_dict_yield)

# yield limit dict
yield_limit_list = {}
yield_limit_list[df_all['lot_id'][len(df_all['lot_id']) - 1]] = [yield_comparison]


# yield limit previous
yield_itter = 0

while yield_itter < 14:
    df_all = df_all[:-1]
    # create dict for yield
    lambda_dict_yield = {}
    lambda_dict_yield['yield'] = []

    # lambda for yield
    for i in df_all.columns[1:2]:
        if len(df_all[df_all[i] != 0][i][177:]) < 50:
            a = df_all[df_all[i] != 0][i][-50:]
            ################### box cox transformation ##################
            boxcox_list_transformed = []

            for k in np.arange(-2, 2.01, 0.01):
                boxcox_indivisual = stats.boxcox((1-(a * 0.01)), k)
                boxcox_list_transformed.append(boxcox_indivisual)
            #############################################################

            ################## Normality Check ##########################
            AD_value_list = []

            for t in range(0, 400, 1):
                AD_value_individual, AD_critical_value, AD_significance_level = anderson(boxcox_list_transformed[t])
                AD_value_list.append(AD_value_individual)
            ##############################################################
            ######################## Find lambda ##########################
            minimum_AD_value = min(AD_value_list)

            lambda_index_list = {}
            for index, value in enumerate(AD_value_list):
                lambda_index_list[value] =  index
            lambda_index_list[minimum_AD_value]


            lambda_list = {}
            lambda_ = np.arange(-2, 2.01, 0.01)
            for index, value in enumerate(lambda_):
                lambda_list[index] =  value
            lambda_list[lambda_index_list[minimum_AD_value]]
            ##############################################################
            #apeend data to dictionary
            lambda_dict_yield[i].append(lambda_list[lambda_index_list[minimum_AD_value]])

        elif len(df_all[df_all[i] != 0][i][177:]) > 50:
            a = df_all[df_all[i] != 0][i][177:]
            ################### box cox transformation ##################
            boxcox_list_transformed = []

            for k in np.arange(-2, 2.01, 0.01):
                boxcox_indivisual = stats.boxcox((1-(a * 0.01)), k)
                boxcox_list_transformed.append(boxcox_indivisual)
            #############################################################

            ################## Normality Check ##########################
            AD_value_list = []

            for t in range(0, 400, 1):
                AD_value_individual, AD_critical_value, AD_significance_level = anderson(boxcox_list_transformed[t])
                AD_value_list.append(AD_value_individual)
            ##############################################################
            ######################## Find lambda ##########################
            minimum_AD_value = min(AD_value_list)

            lambda_index_list = {}
            for index, value in enumerate(AD_value_list):
                lambda_index_list[value] =  index
            lambda_index_list[minimum_AD_value]


            lambda_list = {}
            lambda_ = np.arange(-2, 2.01, 0.01)
            for index, value in enumerate(lambda_):
                lambda_list[index] =  value
            lambda_list[lambda_index_list[minimum_AD_value]]
            ##############################################################
            # apeend data to dictionary
            lambda_dict_yield[i].append(lambda_list[lambda_index_list[minimum_AD_value]])

    # import _yield_limit_calculator function
    import _yield_limit_calculator as yc

    # print yield limit and detailed information about limit calculation
    yield_comparison = yc._yield_limit_calculator(df_all, lambda_dict_yield)

    # Add dictionary
    yield_limit_list[df_all['lot_id'][len(df_all['lot_id']) - 1]] = [yield_comparison]

    yield_itter += 1
    if yield_itter == 1:
        print('1st loop')
    elif yield_itter == 2:
        print('2nd loop')
    elif yield_itter == 3:
        print('3rd loop')
    else:
        print(str(yield_itter) + 'th loop')

df_yield_trend = pd.DataFrame(yield_limit_list).T
df_yield_trend = df_yield_trend[::-1]

# Grab the currently calculated limits
limit_calculated_currently = pd.read_excel(r'D:\books\MPE_project\MPE_FMMT614-7-55_format.xlsx', skiprows = [0,1,2,3,4,5,6,7,8,9], header = 1)

# print(lambda_dict)
# import Plotly package
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as py

# outline subplots
fig = make_subplots(rows=2, cols=4, print_grid=True,
                    subplot_titles=('Open', 'Short', 'ICBO', 'ICES', 'IEBO', 'VCEsat', 'VBEsat', 'Yield'),
                    specs= [[{'type': 'xy'},{'type': 'xy'},{'type': 'xy'},{'type': 'xy'}],
                            [{'type': 'xy'},{'type': 'xy'},{'type': 'xy'},{'type': 'xy'}] ])

# plot info
trace1 = go.Scatter(x = lot_id_list_reversecd,
                    y = df_limit_trend_reversed_2[0],
                    hoverinfo = 'x+y',
                    marker = dict(line = dict(width = 1), size = 8),
                    line = dict(color = '#EC7063', width = 1.5))
trace2 = go.Scatter(x = lot_id_list_reversecd,
                    y = df_limit_trend_reversed_2[1],
                    hoverinfo = 'x+y',
                    marker = dict(line = dict(width = 1), size = 8),
                    line = dict(color = '#9B59B6', width = 1.5))
trace3 = go.Scatter(x = lot_id_list_reversecd,
                    y = df_limit_trend_reversed_2[2],
                    hoverinfo = 'x+y',
                    marker = dict(line = dict(width = 1), size = 8),
                    line = dict(color = '#5DADE2 ', width = 1.5))
trace4 = go.Scatter(x = lot_id_list_reversecd,
                    y = df_limit_trend_reversed_2[3],
                    hoverinfo = 'x+y',
                    marker = dict(line = dict(width = 1), size = 8),
                    line = dict(color = '#48C9B0', width = 1.5))
trace5 = go.Scatter(x = lot_id_list_reversecd,
                    y = df_limit_trend_reversed_2[4],
                    hoverinfo = 'x+y',
                    marker = dict(line = dict(width = 1), size = 8),
                    line = dict(color = '#1E8449', width = 1.5))
trace6 = go.Scatter(x = lot_id_list_reversecd,
                    y = df_limit_trend_reversed_2[5],
                    hoverinfo = 'x+y',
                    marker = dict(line = dict(width = 1), size = 8),
                    line = dict(color = '#F1C40F', width = 1.5))
trace7 = go.Scatter(x = lot_id_list_reversecd,
                    y = df_limit_trend_reversed_2[6],
                    hoverinfo = 'x+y',
                    marker = dict(line = dict(width = 1), size = 8),
                    line = dict(color = '#EB984E', width = 1.5))
trace8 = go.Scatter(x = lot_id_list_reversecd,
                    y = df_yield_trend[0],
                    hoverinfo = 'x+y',
                    marker = dict(line = dict(width = 1), size = 8),
                    line = dict(color = '#616A6B', width = 1.5))

#assign plots into outline
fig.add_trace(trace1, 1, 1);
fig.add_trace(trace2, 1, 2);
fig.add_trace(trace3, 1, 3);
fig.add_trace(trace4, 1, 4);
fig.add_trace(trace5, 2, 1);
fig.add_trace(trace6, 2, 2);
fig.add_trace(trace7, 2, 3);
fig.add_trace(trace8, 2, 4);

# layout
fig.layout.update(title = "MPE limit trend",
                  autosize = False,
                  width = 1400,
                  height = 900,
                  hovermode = 'x',
                  # legend_title='<b> Lot </b>',
                  showlegend = False)
                  # legend_orientation="h",
                  # legend=dict(x=0.2, y=0.55))
# limit line
fig.layout.update(shapes=[{'type': 'line',
                            'x0': lot_id_list_reversecd[0],
                            'y0': limit_calculated_currently['OPEN'].iloc[0],
                            'x1': lot_id_list_reversecd[-1],
                            'y1': limit_calculated_currently['OPEN'].iloc[0],
                            'xref':'x1','yref':'y1',
                            'line': {'color': 'red','width': 1.5, 'dash':"dashdot"}},

                            {'type': 'line',
                            'x0': lot_id_list_reversecd[0],
                            'y0': limit_calculated_currently['SHORT'].iloc[0],
                            'x1': lot_id_list_reversecd[-1],
                            'y1': limit_calculated_currently['SHORT'].iloc[0],
                            'xref':'x2','yref':'y2',
                            'line': {'color': 'red','width': 1.5, 'dash':"dashdot"}},

                            {'type': 'line',
                            'x0': lot_id_list_reversecd[0],
                            'y0': limit_calculated_currently['ICBO'].iloc[0],
                            'x1': lot_id_list_reversecd[-1],
                            'y1': limit_calculated_currently['ICBO'].iloc[0],
                            'xref':'x3','yref':'y3',
                            'line': {'color': 'red','width': 1.5, 'dash':"dashdot"}},

                           {'type': 'line',
                           'x0': lot_id_list_reversecd[0],
                           'y0': limit_calculated_currently['ICES'].iloc[0],
                           'x1': lot_id_list_reversecd[-1],
                           'y1': limit_calculated_currently['ICES'].iloc[0],
                           'xref':'x4','yref':'y4',
                           'line': {'color': 'red','width': 1.5, 'dash':"dashdot"}},

                           {'type': 'line',
                           'x0': lot_id_list_reversecd[0],
                           'y0': limit_calculated_currently['IEB'].iloc[0],
                           'x1': lot_id_list_reversecd[-1],
                           'y1': limit_calculated_currently['IEB'].iloc[0],
                           'xref':'x5','yref':'y5',
                           'line': {'color': 'red','width': 1.5, 'dash':"dashdot"}},

                           {'type': 'line',
                           'x0': lot_id_list_reversecd[0],
                           'y0': limit_calculated_currently['VCESAT'].iloc[0],
                           'x1': lot_id_list_reversecd[-1],
                           'y1': limit_calculated_currently['VCESAT'].iloc[0],
                           'xref':'x6','yref':'y6',
                           'line': {'color': 'red','width': 1.5, 'dash':"dashdot"}},

                            {'type': 'line',
                            'x0': lot_id_list_reversecd[0],
                            'y0': limit_calculated_currently['VBESAT'].iloc[0],
                            'x1': lot_id_list_reversecd[-1],
                            'y1': limit_calculated_currently['VBESAT'].iloc[0],
                            'xref':'x7','yref':'y7',
                            'line': {'color': 'red','width': 1.5, 'dash':"dashdot"}},

                            {'type': 'line',
                            'x0': lot_id_list_reversecd[0],
                            'y0': limit_calculated_currently['Yield'].iloc[0],
                            'x1': lot_id_list_reversecd[-1],
                            'y1': limit_calculated_currently['Yield'].iloc[0],
                            'xref':'x8','yref':'y8',
                            'line': {'color': 'red','width': 1.5, 'dash':"dashdot"}}
                            ])

py.plot(fig, filename='MPE_limit_trend.html')

#
# # import matplotlib
# import matplotlib.pyplot as plt
#
# fig, ax = plt.subplots(2, 4, figsize=(40,40))
# ax[0, 0].plot(lot_id_list_reversecd, df_limit_trend_reversed_2[0],linestyle='--', marker='o', color='b')
# ax[0, 1].plot(lot_id_list_reversecd, df_limit_trend_reversed_2[1],linestyle='--', marker='o', color='y')
# ax[0, 2].plot(lot_id_list_reversecd, df_limit_trend_reversed_2[2],linestyle='--', marker='o', color='g')
# ax[0, 3].plot(lot_id_list_reversecd, df_limit_trend_reversed_2[3],linestyle='--', marker='o', color='c')
# ax[1, 0].plot(lot_id_list_reversecd, df_limit_trend_reversed_2[4],linestyle='--', marker='o', color='r')
# ax[1, 1].plot(lot_id_list_reversecd, df_limit_trend_reversed_2[5],linestyle='--', marker='o', color='k')
# ax[1, 2].plot(lot_id_list_reversecd, df_limit_trend_reversed_2[6],linestyle='--', marker='o', color='m')
# ax[1, 3].plot(lot_id_list_reversecd, df_yield_trend[0],linestyle='--', marker='o')
# ax[0,0].title.set_text('Open')
# ax[0,1].title.set_text('Short')
# ax[0,2].title.set_text('ICBO')
# ax[0,3].title.set_text('ICES')
# ax[1,0].title.set_text('IEBO')
# ax[1,1].title.set_text('VCEsat')
# ax[1,2].title.set_text('VBEsat')
# ax[1,3].title.set_text('Yield')
#
# for i in list(range(0,2)):
#     for j in list(range(0,4)):
#         ax[i,j].grid(True)
#
# for i in list(range(0,2)):
#     for j in list(range(0,4)):
#         ax[i,j].xaxis.set_tick_params(labelsize=5)
#         ax[i,j].yaxis.set_tick_params(labelsize=7)
#
# plt.show()
