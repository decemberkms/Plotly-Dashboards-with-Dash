# basic packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
import time

def data_generator(df):
    # data cleaning for analysis - new column for lot id and remove empty and contact failure
    df['lot_ID'] = df['lot'].map(str) + '_' + df['sub_lot'].map(str)
    df = df[df['bin_name'] != 'Leer']
    df = df[df['bin_name'] != 'Kelvin']

    # percentage calculation
    df_indivisual_count = df.groupby(['lot_ID','bin_number', 'bin_name']).agg({'count': sum})
    df_percentage = df_indivisual_count.groupby(level = 0).apply(lambda x : 100 * x / float(x.sum()))

    # index reset for order
    df_percentage = df_percentage.reset_index()

    # change name
    df_percentage = df_percentage.rename(columns = {'count':'percentage'})

    # extract unique lot ID
    unique_lot_ID = list(set(df_percentage['lot_ID']))
    unique_lot_ID = sorted(unique_lot_ID)

    df_percentage_1 = df_percentage[:33] # # of tests 11
    df_percentage_2 = df_percentage[33:585] # # of tests 12
    df_percentage_3 = df_percentage[585:] # # of tests 14

    # current date
    ww = time.strftime("%W")
    yy = time.strftime("%Y")


    # open the format for MPE report
    MPE = openpyxl.load_workbook(filename='D:\\books\\MPE_project\\MPE_FMMT614-7-55_format.xlsx')

    # grab a sheet in the excel file
    ws1 = MPE["Tabelle1"]

    # dictionary for data DataFrame
    dict_1 = {}
    dict_2 = {}
    dict_3 = {}

    # dict_1 keys
    dict_1['lot_id'] = []
    dict_1['yield'] = []
    dict_1['open'] = []
    dict_1['short'] = []
    dict_1['ICBO'] = []
    dict_1['ICES'] = []
    dict_1['IEBO'] = []
    dict_1['VCEsat'] = []
    dict_1['VBEsat'] = []
    dict_1['Rth'] = []

    # first three lots without Rth
    li_1 = 0
    for i in range(1, int(len(df_percentage_1)/11) + 1):
        c1 = 0 # lot id and yield cycle
        c2 = 4 # open -
        c3 = 5 # short -
        c4 = 6 # ICBO -
        c5 = 7 # ICES -
        c6 = 8 # IEBO -
        c7 = 9 # VCEsat -
        c8 = 10 # VBEsat -
        dict_1['lot_id'].append(df_percentage_1.iloc[c1 + (i-1)*11][0]) # 1 lot id
        dict_1['yield'].append(df_percentage_1.iloc[c1 + (i-1)*11][3]) # 3 yield
        dict_1['open'].append(df_percentage_1.iloc[c2 + (i-1)*11][3]) # 4 open
        dict_1['short'].append(df_percentage_1.iloc[c3 + (i-1)*11][3]) # 5 short
        dict_1['ICBO'].append(df_percentage_1.iloc[c4 + (i-1)*11][3]) # 6 ICBO
        dict_1['ICES'].append(df_percentage_1.iloc[c5 + (i-1)*11][3]) # 7 ICES
        dict_1['IEBO'].append(df_percentage_1.iloc[c6 + (i-1)*11][3]) # 8 IEBO
        dict_1['VCEsat'].append(df_percentage_1.iloc[c7 + (i-1)*11][3]) # 9 VCEsat
        dict_1['VBEsat'].append(df_percentage_1.iloc[c8 + (i-1)*11][3]) # 10 VBEsat
        dict_1['Rth'].append(0) # 10 VBEsat
        li_1 = li_1 + 1

    # make data frame for dict_1
    df1 = pd.DataFrame(dict_1)

    # dict_2 keys
    dict_2['lot_id'] = []
    dict_2['yield'] = []
    dict_2['open'] = []
    dict_2['short'] = []
    dict_2['ICBO'] = []
    dict_2['ICES'] = []
    dict_2['IEBO'] = []
    dict_2['VCEsat'] = []
    dict_2['VBEsat'] = []
    dict_2['Rth'] = []


    # second 46 lots with Rth
    li_2 = 0
    for i in range(1, int(len(df_percentage_2)/12) + 1):
        c1 = 0 # lot id and yield cycle
        c2 = 4 # open -
        c3 = 5 # short -
        c4 = 6 # ICBO -
        c5 = 7 # ICES -
        c6 = 8 # IEBO -
        c7 = 9 # VCEsat -
        c8 = 10 # VBEsat -
        c9 = 11 # Rth -
        dict_2['lot_id'].append(df_percentage_2.iloc[c1 + (i-1)*12][0]) # 1 lot id
        dict_2['yield'].append(df_percentage_2.iloc[c1 + (i-1)*12][3]) # 3 yield
        dict_2['open'].append(df_percentage_2.iloc[c2 + (i-1)*12][3]) # 4 open
        dict_2['short'].append(df_percentage_2.iloc[c3 + (i-1)*12][3]) # 5 short
        dict_2['ICBO'].append(df_percentage_2.iloc[c4 + (i-1)*12][3]) # 6 ICBO
        dict_2['ICES'].append(df_percentage_2.iloc[c5 + (i-1)*12][3]) # 7 ICES
        dict_2['IEBO'].append(df_percentage_2.iloc[c6 + (i-1)*12][3]) # 8 IEBO
        dict_2['VCEsat'].append(df_percentage_2.iloc[c7 + (i-1)*12][3]) # 9 VCEsat
        dict_2['VBEsat'].append(df_percentage_2.iloc[c8 + (i-1)*12][3]) # 10 VBEsat
        dict_2['Rth'].append(0.01*df_percentage_2.iloc[c9 + (i-1)*12][3]) # 12 Rth
        li_2 = li_2 + 1

    # make data frame for dict_2
    df2 = pd.DataFrame(dict_2)

    # dict_3 keys
    dict_3['lot_id'] = []
    dict_3['yield'] = []
    dict_3['open'] = []
    dict_3['short'] = []
    dict_3['ICBO'] = []
    dict_3['ICES'] = []
    dict_3['IEBO'] = []
    dict_3['VCEsat'] = []
    dict_3['VBEsat'] = []
    dict_3['Rth'] = []

    # current third lots
    li_3 = 0
    for i in range(1, int(len(df_percentage_3)/14) + 1):
        c1 = 0 # lot id and yield cycle 1
        c2 = 1 #  yield cycle 2
        c3 = 2 #  yield cycle 3
        c4 = 6 # open -
        c5 = 7 # short -
        c6 = 8 # ICBO -
        c7 = 9 # ICES -
        c8 = 10 # IEBO -
        c9 = 11 # VCEsat -
        c10 = 12 # VBEsat -
        c11 = 13 # Rth -
        dict_3['lot_id'].append(df_percentage_3.iloc[c1 + (i-1)*14][0]) # 1 lot id
        dict_3['yield'].append(df_percentage_3.iloc[c1 + (i-1)*14][3] + df_percentage_3.iloc[c2 + (i-1)*14][3] + df_percentage_3.iloc[c3 + (i-1)*14][3]) # 1,2,3 yield
        dict_3['open'].append(df_percentage_3.iloc[c4 + (i-1)*14][3]) # 4 open
        dict_3['short'].append(df_percentage_3.iloc[c5 + (i-1)*14][3]) # 5 short
        dict_3['ICBO'].append(df_percentage_3.iloc[c6 + (i-1)*14][3]) # 6 ICBO
        dict_3['ICES'].append(df_percentage_3.iloc[c7 + (i-1)*14][3]) # 7 ICES
        dict_3['IEBO'].append(df_percentage_3.iloc[c8 + (i-1)*14][3]) # 8 IEBO
        dict_3['VCEsat'].append(df_percentage_3.iloc[c9 + (i-1)*14][3]) # 9 VCEsat
        dict_3['VBEsat'].append(df_percentage_3.iloc[c10 + (i-1)*14][3]) # 10 VBEsat
        dict_3['Rth'].append(0.01*df_percentage_3.iloc[c11 + (i-1)*14][3]) # 12 Rth
        li_3 = li_3 + 1

    # make data frame for dict_2
    df3 = pd.DataFrame(dict_3)

    df = df1.append(df2, ignore_index = True)
    df = df.append(df3, ignore_index = True)

    # separate df into two parts
    df_old = df[:132]
    df_2020Q1 = df[132:206]
    df_2020Q2= df[206:238]
    df_2020Q3 = df[238:]

    ### 2019 ###
    # labelling mistake from df_old
    df_old = df_old[(df_old['lot_id'] != '537910_1') & (df_old['lot_id'] != '537910_2') & (df_old['lot_id'] != '537910_3') & (df_old['lot_id'] != '537910_4')]

    # Not delivered products
    df_old = df_old = df_old[(df_old['lot_id'] != '484157_3') & (df_old['lot_id'] != '484157_4') & (df_old['lot_id'] != '484157_6') & (df_old['lot_id'] != '484157_8') & (df_old['lot_id'] != '484158_2') & (df_old['lot_id'] != '484158_3')]

    # apply the old limits to df_old (exception 481405_1 - don't know the reason)
    df_old_limit = df_old[(df_old['lot_id'] == '481405_1') | (df_old["yield"] > 95.48) & (df_old["open"] < 0.1) & (df_old["short"] < 0.1) & (df_old["ICBO"] < 0.33) & (df_old["ICES"] < 0.48) & (df_old["IEBO"] < 0.19) & (df_old["VCEsat"] < 0.10) & (df_old["VBEsat"] < 0.10)]
    ### -- ###

    ### 2020 Q1 ###
    # remove blocked lots due to pressed down wires
    df_2020Q1 = df_2020Q1[(df_2020Q1['lot_id'] != '566710_4') & (df_2020Q1['lot_id'] != '569602_1') & (df_2020Q1['lot_id'] != '569602_2') & (df_2020Q1['lot_id'] != '569602_3') & (df_2020Q1['lot_id'] != '569602_4')& (df_2020Q1['lot_id'] != '569602_5') & (df_2020Q1['lot_id'] != '569603_1') & (df_2020Q1['lot_id'] != '569603_2') & (df_2020Q1['lot_id'] != '569603_3') & (df_2020Q1['lot_id'] != '569603_4')]

    # labelling mistake from df_2020Q1
    df_2020Q1 = df_2020Q1[(df_2020Q1['lot_id'] != '574133_1') & (df_2020Q1['lot_id'] != '574133_2') & (df_2020Q1['lot_id'] != '574133_3') & (df_2020Q1['lot_id'] != '574133_4') & (df_2020Q1['lot_id'] != '574133_5') & (df_2020Q1['lot_id'] != '574133_6') & (df_2020Q1['lot_id'] != '574133_7') & (df_2020Q1['lot_id'] != '574133_8') & (df_2020Q1['lot_id'] != '574133_9')]

    # labelling mistake and molding problems from df_2020Q
    df_2020Q1 = df_2020Q1[(df_2020Q1['lot_id'] != '574134_1') & (df_2020Q1['lot_id'] != '574134_2') & (df_2020Q1['lot_id'] != '574134_3') & (df_2020Q1['lot_id'] != '574134_4') & (df_2020Q1['lot_id'] != '574134_5') & (df_2020Q1['lot_id'] != '574134_6')]

    # apply the limits to df_2020Q1
    df_2020Q1_limit = df_2020Q1[(df_2020Q1["yield"] > 98.75) & (df_2020Q1["open"] < 0.1) & (df_2020Q1["short"] < 0.1) & (df_2020Q1["ICBO"] < 0.30) & (df_2020Q1["ICES"] < 0.39) & (df_2020Q1["IEBO"] < 0.20) & (df_2020Q1["VCEsat"] < 0.17) & (df_2020Q1["VBEsat"] < 0.10)]
    ### -- ###

    ### 2020 Q2 ###
    # Marking problem
    df_2020Q2 = df_2020Q2[df_2020Q2['lot_id'] != '575663_1']

    # apply the limits to  df_2020Q2
    df_2020Q2_limit = df_2020Q2[(df_2020Q2["yield"] > 99.09) & (df_2020Q2["open"] < 0.1) & (df_2020Q2["short"] < 0.1) & (df_2020Q2["ICBO"] < 0.7) & (df_2020Q2["ICES"] < 0.79) & (df_2020Q2["IEBO"] < 0.49) & (df_2020Q2["VCEsat"] < 0.14) & (df_2020Q2["VBEsat"] < 0.1)]
    ### -- ###

    ### New limit ###
    # Grab the currently calculated limits
    limit_calculated_currently = pd.read_excel(r'D:\books\MPE_project\MPE_FMMT614-7-55_format.xlsx', skiprows = [0,1,2,3,4,5,6,7,8,9], header = 1)

    # apply the limits to df_new
    df_new_limit = df_2020Q3[(df_2020Q3["yield"] > limit_calculated_currently['Yield'][0]) & (df_2020Q3["open"] < limit_calculated_currently['OPEN'][0]) & (df_2020Q3["short"] < limit_calculated_currently['SHORT'][0]) & (df_2020Q3["ICBO"] < limit_calculated_currently['ICBO'][0]) & (df_2020Q3["ICES"] < limit_calculated_currently['ICES'][0]) & (df_2020Q3["IEBO"] < limit_calculated_currently['IEB'][0]) & (df_2020Q3["VCEsat"] < limit_calculated_currently['VCESAT'][0]) & (df_2020Q3["VBEsat"] < limit_calculated_currently['VBESAT'][0])]
    ### -- ###

    # combine dfs
    df_old_limit = df_old_limit.append(df_2020Q1_limit)
    df_old_limit = df_old_limit.append(df_2020Q2_limit)
    df_all = df_old_limit.append(df_new_limit)

    # reset index
    df_all.reset_index(drop = True, inplace = True);
    return df_all

    # proved data with the former data made by Xiao (manually)
    # data file
    df_all.to_excel("data_file.xlsx")


if __name__ == '__main__':
    df_t = pd.read_excel('D:\\books\\MPE_project\\Statistics\\NY_bin_statistics.xlsx')
    df_all_ = data_generator(df_t)
    df_all_.to_excel("data_file.xlsx")
    print(df_t)
