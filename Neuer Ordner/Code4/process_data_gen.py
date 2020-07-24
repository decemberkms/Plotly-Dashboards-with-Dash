import numpy as np
import pandas as pd
import pymssql
# import pyodbc
from datetime import datetime
import time

total_start_time = time.time()
'''
progress info
'''
conn = pymssql.connect(server='ZNGERP01\\ZNGFINALTEST',
                       user='WebServer',
                       password='W3bS3rv3r',
                       database='ZNGFinalTest')
# pyodbc version
# conn = pyodbc.connect('Driver={SQL Server};'
#                         'Server=ZNGERP01\\ZNGFINALTEST;'
#                         'Database=ZNGFinalTest;'
#                         "uid=WebServer;pwd=W3bS3rv3r;"
#                         "Trusted_Connection=no;")


query1 = "WITH tbl1 AS ( \
SELECT ZNGProduction.catuno.tbl_lots.lot AS a_lot, device, device_group, department, package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date, ZNGProduction.catuno.tbl_products.lead_frame, ZNGProduction.catuno.tbl_products.transistor_type, ZNGProduction.catuno.tbl_products.chip_configuration, ZNGProduction.catuno.tbl_products.soft_solder, ZNGProduction.catuno.tbl_products.bond_wire2, ZNGProduction.catuno.tbl_products.article \
FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') \
), \
tbl2 AS ( \
SELECT lot, STRING_AGG(CAST(wafer_info AS NVARCHAR(MAX)), '; ') AS wafer_info \
FROM \
( \
SELECT lot, wafer_lot + ': ' + CAST(wafer_quantity as VARCHAR(100))  + '(' + probed + ')' AS wafer_info \
FROM ZNGProduction.catuno.tbl_wafers \
WHERE lot NOT LIKE '2%' AND lot NOT LIKE '3%' AND lot NOT LIKE '40%' AND lot NOT LIKE '41%' AND lot NOT LIKE '42%' \
) tbl0 \
GROUP BY lot \
), \
tbl3 AS ( \
SELECT ZNGFinalTest.quality.vw_lots.quality_id, ZNGFinalTest.quality.vw_lots.lot, comment, cause, ZNGFinalTest.quality.vw_lots.wps, ZNGFinalTest.quality.vw_lots.fa, ZNGFinalTest.quality.vw_lots.edit_user,  ZNGFinalTest.quality.vw_last_comments.date, ZNGFinalTest.quality.tbl_classes.class_name, ZNGFinalTest.quality.vw_lots.create_user, ZNGFinalTest.quality.vw_lots.create_date \
FROM ZNGFinalTest.quality.vw_last_comments \
JOIN ZNGFinalTest.quality.vw_lots \
ON ZNGFinalTest.quality.vw_lots.quality_id = ZNGFinalTest.quality.vw_last_comments.quality_id \
JOIN ZNGFinalTest.quality.tbl_classes \
ON ZNGFinalTest.quality.tbl_classes.class_id = ZNGFinalTest.quality.vw_lots.class_id \
), \
tbl4 AS ( \
SELECT DISTINCT ZNGFinalTest.final_test3.tbl_summaries.lot, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.workplace AS NVARCHAR(MAX)), '; ') AS workplace, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.tester AS NVARCHAR(MAX)), '; ') AS tester, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.operator AS NVARCHAR(MAX)), '; ') AS operator  \
FROM ZNGFinalTest.final_test3.tbl_summaries \
GROUP BY ZNGFinalTest.final_test3.tbl_summaries.lot \
), \
tbl5 AS ( \
SELECT DISTINCT ZNGProduction.catuno.tbl_lots.lot, ZNGProduction.catuno.tbl_manufacture.workstep_id, ZNGProduction.catuno.tbl_manufacture.workstep_name, ZNGProduction.catuno.tbl_manufacture.input, ZNGProduction.catuno.tbl_manufacture.reject, ZNGProduction.catuno.tbl_manufacture.output, ZNGProduction.catuno.tbl_manufacture.date AS done_date \
FROM ZNGProduction.catuno.tbl_manufacture \
FULL JOIN ZNGProduction.catuno.tbl_lots \
ON ZNGProduction.catuno.tbl_lots.ba = ZNGProduction.catuno.tbl_manufacture.ba \
) \
SELECT DISTINCT tbl1.a_lot, tbl1.device, tbl5.workstep_id, tbl5.workstep_name, tbl5.input, tbl5.reject, tbl5.output, tbl5.done_date \
FROM tbl1 \
LEFT JOIN tbl2 \
ON tbl2.lot = tbl1.a_lot \
LEFT JOIN tbl3 \
ON tbl3.lot = tbl1.a_lot \
LEFT JOIN tbl4 \
ON tbl4.lot = tbl1.a_lot \
JOIN tbl5 \
ON tbl5.lot = tbl1.a_lot \
WHERE device <> 'FMMT614' AND workstep_id IS NOT NULL \
ORDER BY a_lot DESC, workstep_id, input DESC"

# read progress info and remove nan
df_process = pd.read_sql(query1, conn)

##### data cleaning process #####
# remove non-named work step & reindex
df_process = df_process[df_process['workstep_name'].notnull()]
df_process.reset_index(inplace=True, drop=True)

# change end steop GURTEN to AUSLIEFERN (old version workstep)
ind_diff_tail  = df_process.groupby('a_lot').tail(1)[df_process['workstep_name'] == 'GURTEN'].index
for ind in ind_diff_tail:
    df_process['workstep_name'].iloc[ind] = 'AUSLIEFERN'

# wrong data - first step GURTEN (drop)
error = df_process.groupby(['a_lot']).head(1)[df_process['workstep_name'] == 'GURTEN'].index[0]
df_process.drop(error,inplace=True)
df_process.reset_index(inplace=True, drop=True)

# replace device name with nan with Unknown
df_process['device'] = df_process['device'].fillna('Unknown')

# fill first empty cells - lots that haven't started yet (mostly)
lst_h_empty = df_process.groupby(['a_lot']).head(1)[df_process.groupby(['a_lot']).head(1)['input'].isnull()].index
for i in lst_h_empty.values:
    df_process.loc[df_process.index == i] = df_process.loc[df_process.index == i].fillna(0)

# total reject amount (except for Sawing) for process 2 calculation
df_reject = df_process[df_process['workstep_name'] != 'SÄGEN'].groupby(['a_lot'], as_index=False)['reject'].sum()
df_reject.sort_values('a_lot', ascending=False, inplace =True)
df_reject.reset_index(inplace=True, drop=True)

# Drop empty rows and reindex
df_process.dropna('index', inplace=True)
df_process.reset_index(inplace=True, drop=True)

print("### Process info data: Loaded and cleaned ###")


'''
progress additional info
'''

query2 = "WITH tbl1 AS ( \
SELECT ZNGProduction.catuno.tbl_lots.lot AS a_lot, device, device_group, department, package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date, ZNGProduction.catuno.tbl_products.lead_frame, ZNGProduction.catuno.tbl_products.transistor_type, ZNGProduction.catuno.tbl_products.chip_configuration, ZNGProduction.catuno.tbl_products.soft_solder, ZNGProduction.catuno.tbl_products.bond_wire2, ZNGProduction.catuno.tbl_products.article \
FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') \
), \
tbl2 AS ( \
SELECT lot, STRING_AGG(CAST(wafer_info AS NVARCHAR(MAX)), '; ') AS wafer_info \
FROM \
( \
SELECT lot, wafer_lot + ': ' + CAST(wafer_quantity as VARCHAR(100))  + '(' + probed + ')' AS wafer_info \
FROM ZNGProduction.catuno.tbl_wafers \
WHERE lot NOT LIKE '2%' AND lot NOT LIKE '3%' AND lot NOT LIKE '40%' AND lot NOT LIKE '41%' AND lot NOT LIKE '42%' \
) tbl0 \
GROUP BY lot \
), \
tbl3 AS ( \
SELECT  ZNGFinalTest.quality.vw_lots.release, ZNGFinalTest.quality.vw_lots.scrapped, ZNGFinalTest.quality.vw_lots.quality_id, ZNGFinalTest.quality.vw_lots.lot, comment, cause, ZNGFinalTest.quality.vw_lots.wps, ZNGFinalTest.quality.vw_lots.fa, ZNGFinalTest.quality.vw_lots.edit_user,  ZNGFinalTest.quality.vw_last_comments.date, ZNGFinalTest.quality.tbl_classes.class_name, ZNGFinalTest.quality.vw_lots.create_user, ZNGFinalTest.quality.vw_lots.create_date \
FROM ZNGFinalTest.quality.vw_last_comments \
JOIN ZNGFinalTest.quality.vw_lots \
ON ZNGFinalTest.quality.vw_lots.quality_id = ZNGFinalTest.quality.vw_last_comments.quality_id \
JOIN ZNGFinalTest.quality.tbl_classes \
ON ZNGFinalTest.quality.tbl_classes.class_id = ZNGFinalTest.quality.vw_lots.class_id \
), \
tbl4 AS ( \
SELECT DISTINCT ZNGFinalTest.final_test3.tbl_summaries.lot, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.workplace AS NVARCHAR(MAX)), '; ') AS workplace, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.tester AS NVARCHAR(MAX)), '; ') AS tester, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.operator AS NVARCHAR(MAX)), '; ') AS operator  \
FROM ZNGFinalTest.final_test3.tbl_summaries \
GROUP BY ZNGFinalTest.final_test3.tbl_summaries.lot \
), \
tbl5 AS ( \
SELECT DISTINCT ZNGProduction.catuno.tbl_lots.lot, ZNGProduction.catuno.tbl_manufacture.workstep_id, ZNGProduction.catuno.tbl_manufacture.workstep_name, ZNGProduction.catuno.tbl_manufacture.input, ZNGProduction.catuno.tbl_manufacture.reject, ZNGProduction.catuno.tbl_manufacture.output, ZNGProduction.catuno.tbl_manufacture.date AS done_date \
FROM ZNGProduction.catuno.tbl_manufacture \
FULL JOIN ZNGProduction.catuno.tbl_lots \
ON ZNGProduction.catuno.tbl_lots.ba = ZNGProduction.catuno.tbl_manufacture.ba \
) \
SELECT DISTINCT tbl1.a_lot, tbl1.device, tbl2.wafer_info, tbl1.device_group, tbl1.package, tbl1.bond_wire, tbl1.ship_package, tbl1.final_test_output, ROUND(100*tbl1.final_test_yield,2) AS final_test_yield, tbl1.delivery_date, CASE WHEN tbl3.quality_id IS NULL THEN '0' ELSE tbl3.quality_id END AS quality_id, tbl3.release, tbl3.scrapped, tbl1.transistor_type, tbl1.chip_configuration, tbl1.lead_frame, tbl1.soft_solder \
FROM tbl1 \
LEFT JOIN tbl2 \
ON tbl2.lot = tbl1.a_lot \
LEFT JOIN tbl3 \
ON tbl3.lot = tbl1.a_lot \
LEFT JOIN tbl4 \
ON tbl4.lot = tbl1.a_lot \
JOIN tbl5 \
ON tbl5.lot = tbl1.a_lot \
WHERE device <> 'FMMT614' \
ORDER BY a_lot DESC, final_test_yield"

df_add_info = pd.read_sql(query2, conn)

# remove duplicated nan rows (keeping the last row (sorted order in SQL query))
df_add_info_new = df_add_info.drop_duplicates(subset=['a_lot'], keep='last')

# reindex
df_add_info_new.reset_index(inplace=True, drop=True)

# reindex 2 for loop (in order to have an index column)
df_add_info_new.reset_index(inplace=True)

print("### Process addtional info data: Loaded and cleaned ###")

'''
Combine two data frames
'''
# making lists for new data frame
ongoing_process = list(df_process.groupby(['a_lot']).tail(1)['workstep_name'].values)
ongoing_input = list(df_process.groupby(['a_lot']).tail(1)['input'].values)
ongoing_reject = list(df_process.groupby(['a_lot']).tail(1)['reject'].values)
ongoing_output = list(df_process.groupby(['a_lot']).tail(1)['output'].values)
ongoing_done_date = list(df_process.groupby(['a_lot']).tail(1)['done_date'].values)

beginning_process = list(df_process.groupby(['a_lot']).head(1)['workstep_name'].values)
beginning_input = list(df_process.groupby(['a_lot']).head(1)['input'].values)
beginning_reject = list(df_process.groupby(['a_lot']).head(1)['reject'].values)
beginning_output = list(df_process.groupby(['a_lot']).head(1)['output'].values)
beginning_done_date = list(df_process.groupby(['a_lot']).head(1)['done_date'].values)

# create new columns using lists above
df_add_info_new['ongoing_process'] = ongoing_process
df_add_info_new['ongoing_input'] = ongoing_input
df_add_info_new['ongoing_reject'] = ongoing_reject
df_add_info_new['ongoing_output'] = ongoing_output
df_add_info_new['ongoing_done_date'] = ongoing_done_date

df_add_info_new['beginning_process'] = beginning_process
df_add_info_new['beginning_input'] = beginning_input
df_add_info_new['beginning_reject'] = beginning_reject
df_add_info_new['beginning_output'] = beginning_output
df_add_info_new['beginning_done_date'] = beginning_done_date

# progress (beginning output value / ending output value)
df_add_info_new['progress'] = df_add_info_new['ongoing_output'] / df_add_info_new['beginning_output']

# progress2 (ongoing output value / {beginning output value - total rejects}) - only for tracking progress (how many chips have been through the current process)
df_add_info_new['progress2'] = df_add_info_new['ongoing_output'] / (df_add_info_new['beginning_output'] - df_reject['reject'])

print("### Lists for complete dataframe: Created ###")

'''
Data creation
'''

process_board = {}
i = 0
while i < len(df_add_info_new):
    process_board[i] = []
    i += 1

start_time = time.time()

for i in range(len(df_add_info_new)):
    # no data
    if (df_add_info_new.iloc[i]['ongoing_output'] == 0) & (df_add_info_new.iloc[i]['beginning_output'] == 0):
        if (pd.notnull(df_add_info_new.iloc[i]['delivery_date'])) :
            process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
            process_board[i].append('Ausgeliefert')
        elif pd.isnull(df_add_info_new.iloc[i]['delivery_date']):
            if df_add_info_new.iloc[i]['quality_id'] != 0:
                if df_add_info_new.iloc[i]['scrapped']:
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('Verschotten')
                elif (df_add_info_new.iloc[i]['release'] == True):
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('Wird bald ausgeliefert')
                else:
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('Qualitätsproblem')
            else:
                if (df_add_info_new.iloc[i]['index'] >= 500):
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('Gesperrt')
                elif (df_add_info_new.iloc[i]['index'] < 500):
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('Vorbereitungen für den Start')
                else:
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('Kategorie 1_1') # no delivery date
#         else:
#             process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
#             process_board[i].append('Kategorie 1')

    # only beginning data
    elif (df_add_info_new.iloc[i]['ongoing_output'] == 0) & (df_add_info_new.iloc[i]['beginning_output'] != 0):
        if (pd.notnull(df_add_info_new.iloc[i]['delivery_date'])):
            process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
            process_board[i].append('Ausgeliefert')
        elif pd.isnull(df_add_info_new.iloc[i]['delivery_date']):
            if (df_add_info_new.iloc[i]['quality_id'] != 0):
                if df_add_info_new.iloc[i]['scrapped']:
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('Verschotten')
                elif(df_add_info_new.iloc[i]['release'] == True):
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('Wird bald ausgeliefert')
                else:
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('Qualitätsproblem')
            else:
                process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                process_board[i].append('{one} Tage nach Vorbereitung von {two}'.format(one=str(((datetime.today() - df_add_info_new.iloc[i]['ongoing_done_date']).days)), two=df_add_info_new['ongoing_process'].iloc[i]))

#         else:
#             process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
#             process_board[i].append('Kategorie 2')

    # only ending data
    elif (df_add_info_new.iloc[i]['ongoing_output'] != 0) & (df_add_info_new.iloc[i]['beginning_output'] == 0):
        if (pd.notnull(df_add_info_new.iloc[i]['delivery_date'])):
            process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
            process_board[i].append('Ausgeliefert')
        else:
            if df_add_info_new.iloc[i]['scrapped']:
                process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                process_board[i].append('Verschotten')
            elif (df_add_info_new.iloc[i]['release'] == True):
                process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                process_board[i].append('Wird bald ausgeliefert')
            else:
                process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                process_board[i].append('Kategorie 3')

    # both beginning and ending data
    elif (df_add_info_new.iloc[i]['ongoing_output'] != 0) & (df_add_info_new.iloc[i]['beginning_output'] != 0):
        if (pd.notnull(df_add_info_new.iloc[i]['delivery_date'])):
            process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
            process_board[i].append('Ausgeliefert')
        elif pd.isnull(df_add_info_new.iloc[i]['delivery_date']):
            if df_add_info_new.iloc[i]['quality_id'] != 0:
                if df_add_info_new.iloc[i]['scrapped']:
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('Verschotten')
                elif (df_add_info_new.iloc[i]['release'] == True):
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('Wird bald ausgeliefert')
                else:
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('Qualitätsproblem')
            elif df_add_info_new.iloc[i]['quality_id'] == 0:
                if df_add_info_new.iloc[i]['ongoing_process'] == 'AUSLIEFERN':
                    if (pd.notnull(df_add_info_new.iloc[i]['final_test_yield'])):
                        if ((datetime.today() - df_add_info_new.iloc[i]['ongoing_done_date']).days < 5):
                            process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                            process_board[i].append('Vor Auslieferung nach Endmessung')
                        else:
                            process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                            process_board[i].append('{} Tage vergehen nach Auslieferung'.format(str(((datetime.today() - df_add_info_new.iloc[i]['ongoing_done_date']).days))))
                    else:
                        process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                        process_board[i].append('Vor Scanning nach Endmessung')

                else:
                    process_board[i].append(df_add_info_new['ongoing_process'].iloc[i])
                    process_board[i].append('{one} Tage vergehen nach {two}'.format(one=str(((datetime.today() - df_add_info_new.iloc[i]['ongoing_done_date']).days)), two=df_add_info_new['ongoing_process'].iloc[i]))
    else:
        process_board[i].append('?')
        process_board[i].append('?')

print("### Loop for data sorting: Completed ###")
print("Loop timer: --- %s seconds ---" % (time.time() - start_time))

'''
Create complete dataframe
'''
start_time = time.time()

#making dataFrame from the loop data
process_state_board = pd.DataFrame([k for k in process_board.items()], columns = ['index', 'step'])

# seperate step from above dataFrame
process_state_board = pd.concat([process_state_board, process_state_board['step'].apply(pd.Series)], axis = 1)

print("### Dataframe: Concatenated ###")
print("Dataframe timer: --- %s seconds ---" % (time.time() - start_time))

# concat dataframes and removing redundant data
bigdata = pd.concat([df_add_info_new, process_state_board], axis=1)
bigdata.drop(['step','index'], axis=1, inplace=True)
bigdata.rename(columns={0:'current_step'}, inplace=True)
bigdata.rename(columns={1:'comment_for_lot_step'}, inplace=True)
bigdata.reset_index(inplace=True)
## replace 0 with -0.01 in progress
bigdata['progress'].fillna(-0.01, inplace=True)

# data for stack histogram
progress2_comment = []
# filling empty cells in progress2_comment
for i in bigdata.index:
    if bigdata.iloc[i]['comment_for_lot_step'] == 'Qualitätsproblem':
        progress2_comment.append('Qualitätsproblem')
    else:
        if pd.isnull(bigdata.iloc[i]['progress2']):
            progress2_comment.append('Vor Produktionsbeginn')
        elif bigdata.iloc[i]['progress2'] <= 0:
            progress2_comment.append('Vor dem Beginn des Schritts')
        elif 0 < bigdata.iloc[i]['progress2'] <= 0.93:
            progress2_comment.append('Läuft')
        elif 0.93 < bigdata.iloc[i]['progress2']:
            progress2_comment.append('Erledigt')
        else:
            progress2_comment.append('?')

progress2_comment = pd.DataFrame(progress2_comment, columns =['progress2_comment_2'])

bigdata = pd.concat([bigdata, progress2_comment], axis=1)

'''
Excel file creation
'''
start_time = time.time()
#bigdata.to_excel("output2.xlsx")
bigdata.to_csv("output2.txt",index=False)
print("### Excel file (output2.xlsx): Created ###")
print("Excel file timer: --- %s seconds ---" % (time.time() - start_time))

print("Total timer: --- %s seconds ---" % (time.time() - total_start_time))
